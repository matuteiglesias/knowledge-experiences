from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from .canonical import sha256_file
from .models import SourceSpec, ValidationError, validate_item


@dataclass(frozen=True)
class LoadedSource:
    items: tuple[dict[str, Any], ...]
    sha256: str
    path: str


class SourceAdapter(Protocol):
    name: str

    def load(self, source: SourceSpec, *, base_dir: Path) -> LoadedSource:
        ...


def _load_jsonl(path: Path, source_path: str) -> list[tuple[int, dict[str, Any]]]:
    rows: list[tuple[int, dict[str, Any]]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{source_path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(raw, dict):
            raise ValidationError(f"{source_path}:{lineno}: record must be an object")
        rows.append((lineno, raw))
    return rows


class JsonlSourceAdapter:
    name = "jsonl"

    def load(self, source: SourceSpec, *, base_dir: Path) -> LoadedSource:
        path = (base_dir / source.path).resolve()
        if not path.is_file():
            raise ValidationError(f"source file does not exist: {source.path}")
        items: list[dict[str, Any]] = []
        seen: set[str] = set()
        for lineno, raw in _load_jsonl(path, source.path):
            item = validate_item(raw)
            item_id = item["item_id"]
            if item_id in seen:
                raise ValidationError(f"{source.path}:{lineno}: duplicate item_id {item_id!r}")
            seen.add(item_id)
            items.append(item)
        return LoadedSource(items=tuple(items), sha256=sha256_file(path), path=source.path)


def _paper_catalog_item(raw: dict[str, Any], *, source: SourceSpec, lineno: int) -> dict[str, Any]:
    prefix = f"{source.path}:{lineno}"
    if raw.get("schema_id") != "paper.catalog-record" or raw.get("schema_version") != 1:
        raise ValidationError(f"{prefix}: expected paper.catalog-record@1")
    paper_uid = raw.get("paper_uid")
    title = raw.get("title")
    authors = raw.get("authors")
    if not isinstance(paper_uid, str) or not paper_uid.strip():
        raise ValidationError(f"{prefix}: paper_uid must be a non-empty string")
    if not isinstance(title, str) or not title.strip():
        raise ValidationError(f"{prefix}: title must be a non-empty string")
    if not isinstance(authors, list) or any(not isinstance(x, str) or not x.strip() for x in authors):
        raise ValidationError(f"{prefix}: authors must be an array of non-empty strings")

    year = raw.get("year")
    if year is not None and (not isinstance(year, int) or isinstance(year, bool)):
        raise ValidationError(f"{prefix}: year must be an integer or null")
    for field in ("abstract", "date", "venue", "source_url"):
        value = raw.get(field)
        if value is not None and not isinstance(value, str):
            raise ValidationError(f"{prefix}: {field} must be a string or null")
    tags = raw.get("tags", [])
    if not isinstance(tags, list) or any(not isinstance(x, str) or not x.strip() for x in tags):
        raise ValidationError(f"{prefix}: tags must be an array of non-empty strings")

    facets: dict[str, Any] = {"author": list(authors)}
    if year is not None:
        facets["year"] = year
    venue = raw.get("venue")
    if isinstance(venue, str) and venue.strip():
        facets["venue"] = venue.strip()

    item: dict[str, Any] = {
        "item_id": paper_uid.strip(),
        "kind": "paper",
        "title": title.strip(),
        "contributors": [x.strip() for x in authors],
        "tags": [x.strip() for x in tags],
        "facets": facets,
        "source_ref": {"authority": source.authority, "object_id": paper_uid.strip()},
    }
    abstract = raw.get("abstract")
    if isinstance(abstract, str) and abstract.strip():
        item["summary"] = abstract.strip()
    date = raw.get("date")
    if isinstance(date, str) and date.strip():
        item["date"] = date.strip()
    if isinstance(venue, str) and venue.strip():
        item["subtitle"] = venue.strip()
    source_url = raw.get("source_url")
    if isinstance(source_url, str) and source_url.strip():
        item["canonical_url"] = source_url.strip()
        item["source_ref"]["url"] = source_url.strip()
    return validate_item(item)


class PaperCatalogSourceAdapter:
    name = "paper-catalog-jsonl"

    def load(self, source: SourceSpec, *, base_dir: Path) -> LoadedSource:
        path = (base_dir / source.path).resolve()
        if not path.is_file():
            raise ValidationError(f"source file does not exist: {source.path}")
        items: list[dict[str, Any]] = []
        seen: set[str] = set()
        for lineno, raw in _load_jsonl(path, source.path):
            item = _paper_catalog_item(raw, source=source, lineno=lineno)
            item_id = item["item_id"]
            if item_id in seen:
                raise ValidationError(f"{source.path}:{lineno}: duplicate paper_uid {item_id!r}")
            seen.add(item_id)
            items.append(item)
        return LoadedSource(items=tuple(items), sha256=sha256_file(path), path=source.path)


def _paper_review_item(raw: dict[str, Any], *, source: SourceSpec, lineno: int) -> dict[str, Any]:
    prefix = f"{source.path}:{lineno}"
    if raw.get("schema_id") != "paper.review-record" or raw.get("schema_version") != 1:
        raise ValidationError(f"{prefix}: expected paper.review-record@1")
    paper_uid = raw.get("paper_uid")
    title = raw.get("title")
    if not isinstance(paper_uid, str) or not paper_uid.strip():
        raise ValidationError(f"{prefix}: paper_uid must be a non-empty string")
    if not isinstance(title, str) or not title.strip():
        raise ValidationError(f"{prefix}: title must be a non-empty string")
    for field in ("abstract", "date", "venue", "source_url"):
        value = raw.get(field)
        if value is not None and not isinstance(value, str):
            raise ValidationError(f"{prefix}: {field} must be a string or null")
    year = raw.get("year")
    if year is not None and (not isinstance(year, int) or isinstance(year, bool)):
        raise ValidationError(f"{prefix}: year must be an integer or null")
    for field in ("tags", "badges"):
        values = raw.get(field, []) or []
        if not isinstance(values, list) or any(not isinstance(x, str) for x in values):
            raise ValidationError(f"{prefix}: {field} must be an array of strings")

    tags = [x.strip() for x in (raw.get("tags") or []) if x.strip()]
    badges = [x.strip() for x in (raw.get("badges") or []) if x.strip()]
    facets: dict[str, Any] = {}
    if year is not None:
        facets["year"] = year
    venue = raw.get("venue")
    if isinstance(venue, str) and venue.strip():
        facets["venue"] = venue.strip()
    if badges:
        facets["badge"] = badges

    item: dict[str, Any] = {
        "item_id": paper_uid.strip(),
        "kind": "paper",
        "title": title.strip(),
        "contributors": [],
        "tags": tags,
        "facets": facets,
        "source_ref": {"authority": source.authority, "object_id": paper_uid.strip()},
    }
    abstract = raw.get("abstract")
    if isinstance(abstract, str) and abstract.strip():
        item["summary"] = abstract.strip()
    date = raw.get("date")
    if isinstance(date, str) and date.strip():
        item["date"] = date.strip()
    if isinstance(venue, str) and venue.strip():
        item["subtitle"] = venue.strip()
    source_url = raw.get("source_url")
    if isinstance(source_url, str) and source_url.strip():
        item["canonical_url"] = source_url.strip()
        item["source_ref"]["url"] = source_url.strip()
    return validate_item(item)


class PaperReviewSourceAdapter:
    name = "paper-review-jsonl"

    def load(self, source: SourceSpec, *, base_dir: Path) -> LoadedSource:
        path = (base_dir / source.path).resolve()
        if not path.is_file():
            raise ValidationError(f"source file does not exist: {source.path}")
        items: list[dict[str, Any]] = []
        seen: set[str] = set()
        for lineno, raw in _load_jsonl(path, source.path):
            item = _paper_review_item(raw, source=source, lineno=lineno)
            item_id = item["item_id"]
            if item_id in seen:
                raise ValidationError(f"{source.path}:{lineno}: duplicate paper_uid {item_id!r}")
            seen.add(item_id)
            items.append(item)
        return LoadedSource(items=tuple(items), sha256=sha256_file(path), path=source.path)


_ADAPTERS: dict[str, SourceAdapter] = {
    "jsonl": JsonlSourceAdapter(),
    "paper-catalog-jsonl": PaperCatalogSourceAdapter(),
    "paper-review-jsonl": PaperReviewSourceAdapter(),
}


def get_source_adapter(name: str) -> SourceAdapter:
    try:
        return _ADAPTERS[name]
    except KeyError as exc:
        raise ValidationError(f"unsupported source adapter: {name!r}") from exc
