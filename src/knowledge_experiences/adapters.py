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


class JsonlSourceAdapter:
    name = "jsonl"

    def load(self, source: SourceSpec, *, base_dir: Path) -> LoadedSource:
        path = (base_dir / source.path).resolve()
        if not path.is_file():
            raise ValidationError(f"source file does not exist: {source.path}")
        items: list[dict[str, Any]] = []
        seen: set[str] = set()
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValidationError(f"{source.path}:{lineno}: invalid JSON: {exc}") from exc
            item = validate_item(raw)
            item_id = item["item_id"]
            if item_id in seen:
                raise ValidationError(f"{source.path}:{lineno}: duplicate item_id {item_id!r}")
            seen.add(item_id)
            items.append(item)
        return LoadedSource(items=tuple(items), sha256=sha256_file(path), path=source.path)


_ADAPTERS: dict[str, SourceAdapter] = {"jsonl": JsonlSourceAdapter()}


def get_source_adapter(name: str) -> SourceAdapter:
    try:
        return _ADAPTERS[name]
    except KeyError as exc:
        raise ValidationError(f"unsupported source adapter: {name!r}") from exc
