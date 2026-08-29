from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlparse

from .canonical import sha256_value


class ValidationError(ValueError):
    pass


def _expect_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValidationError(f"{label} must be an object")
    return dict(value)


def _required_str(data: Mapping[str, Any], key: str, label: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label}.{key} must be a non-empty string")
    return value.strip()


def _optional_str(data: Mapping[str, Any], key: str, label: str) -> str | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError(f"{label}.{key} must be a string or null")
    value = value.strip()
    return value or None


def _optional_url(data: Mapping[str, Any], key: str, label: str) -> str | None:
    value = _optional_str(data, key, label)
    if value is None:
        return None
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise ValidationError(f"{label}.{key} must use http or https")
    return value


def _string_list(value: Any, label: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValidationError(f"{label} must be an array")
    out: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValidationError(f"{label} items must be non-empty strings")
        out.append(item.strip())
    if len(out) != len(set(out)):
        raise ValidationError(f"{label} must not contain duplicates")
    return tuple(out)


def _facet_selector_mapping(value: Any, label: str) -> tuple[tuple[str, str | int | float | bool], ...]:
    data = _expect_mapping(value, label)
    out: list[tuple[str, str | int | float | bool]] = []
    for key, wanted in sorted(data.items()):
        if not isinstance(key, str) or not key.strip():
            raise ValidationError(f"{label} keys must be non-empty strings")
        if isinstance(wanted, bool):
            normalized: str | int | float | bool = wanted
        elif isinstance(wanted, (str, int, float)):
            normalized = wanted.strip() if isinstance(wanted, str) else wanted
            if isinstance(normalized, str) and not normalized:
                raise ValidationError(f"{label}.{key} must be non-empty")
        else:
            raise ValidationError(f"{label}.{key} must be a string, number, or boolean")
        out.append((key.strip(), normalized))
    if not out:
        raise ValidationError(f"{label} must be non-empty")
    return tuple(out)


@dataclass(frozen=True)
class SourceSpec:
    adapter: str
    path: str
    authority: str
    release_id: str | None = None

    @classmethod
    def from_dict(cls, raw: Any) -> "SourceSpec":
        data = _expect_mapping(raw, "source")
        allowed = {"adapter", "path", "authority", "release_id"}
        extra = set(data) - allowed
        if extra:
            raise ValidationError(f"source has unknown fields: {sorted(extra)}")
        return cls(
            adapter=_required_str(data, "adapter", "source"),
            path=_required_str(data, "path", "source"),
            authority=_required_str(data, "authority", "source"),
            release_id=_optional_str(data, "release_id", "source"),
        )

    def to_dict(self) -> dict[str, Any]:
        out = {"adapter": self.adapter, "path": self.path, "authority": self.authority}
        if self.release_id is not None:
            out["release_id"] = self.release_id
        return out


@dataclass(frozen=True)
class SelectionSpec:
    mode: str = "all"
    item_ids: tuple[str, ...] = ()
    facets: tuple[tuple[str, str | int | float | bool], ...] = ()

    @classmethod
    def from_dict(cls, raw: Any) -> "SelectionSpec":
        if raw is None:
            return cls()
        data = _expect_mapping(raw, "selection")
        allowed = {"mode", "item_ids", "facets"}
        extra = set(data) - allowed
        if extra:
            raise ValidationError(f"selection has unknown fields: {sorted(extra)}")
        mode = data.get("mode", "all")
        if mode not in {"all", "ids", "facets"}:
            raise ValidationError("selection.mode must be 'all', 'ids', or 'facets'")
        ids = _string_list(data.get("item_ids"), "selection.item_ids")
        facets = _facet_selector_mapping(data.get("facets"), "selection.facets") if mode == "facets" else ()
        if mode == "ids" and not ids:
            raise ValidationError("selection.item_ids must be non-empty when mode='ids'")
        if mode != "ids" and ids:
            raise ValidationError("selection.item_ids is only valid when mode='ids'")
        if mode != "facets" and data.get("facets") not in (None, {}):
            raise ValidationError("selection.facets is only valid when mode='facets'")
        return cls(mode=mode, item_ids=ids, facets=facets)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"mode": self.mode}
        if self.mode == "ids":
            out["item_ids"] = list(self.item_ids)
        if self.mode == "facets":
            out["facets"] = {key: value for key, value in self.facets}
        return out


@dataclass(frozen=True)
class CollectionSpec:
    collection_id: str
    title: str
    source: SourceSpec
    description: str | None = None
    selection: SelectionSpec = SelectionSpec()

    schema_id = "knowledge.collection-spec"
    schema_version = 1

    @classmethod
    def from_dict(cls, raw: Any) -> "CollectionSpec":
        data = _expect_mapping(raw, "CollectionSpec")
        allowed = {"schema_id", "schema_version", "collection_id", "title", "description", "source", "selection"}
        extra = set(data) - allowed
        if extra:
            raise ValidationError(f"CollectionSpec has unknown fields: {sorted(extra)}")
        if data.get("schema_id") != cls.schema_id or data.get("schema_version") != cls.schema_version:
            raise ValidationError("CollectionSpec schema_id/schema_version mismatch")
        return cls(
            collection_id=_required_str(data, "collection_id", "CollectionSpec"),
            title=_required_str(data, "title", "CollectionSpec"),
            description=_optional_str(data, "description", "CollectionSpec"),
            source=SourceSpec.from_dict(data.get("source")),
            selection=SelectionSpec.from_dict(data.get("selection")),
        )

    def to_dict(self) -> dict[str, Any]:
        out = {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "collection_id": self.collection_id,
            "title": self.title,
            "source": self.source.to_dict(),
            "selection": self.selection.to_dict(),
        }
        if self.description is not None:
            out["description"] = self.description
        return out


@dataclass(frozen=True)
class ExperienceSpec:
    experience_id: str
    collection_spec: str
    renderer: str
    title: str | None = None
    visibility: str = "private"
    facets: tuple[str, ...] = ()
    search: bool = True
    default_sort: str = "title"

    schema_id = "knowledge.experience-spec"
    schema_version = 1

    @classmethod
    def from_dict(cls, raw: Any) -> "ExperienceSpec":
        data = _expect_mapping(raw, "ExperienceSpec")
        allowed = {"schema_id", "schema_version", "experience_id", "title", "collection_spec", "renderer", "visibility", "capabilities", "navigation"}
        extra = set(data) - allowed
        if extra:
            raise ValidationError(f"ExperienceSpec has unknown fields: {sorted(extra)}")
        if data.get("schema_id") != cls.schema_id or data.get("schema_version") != cls.schema_version:
            raise ValidationError("ExperienceSpec schema_id/schema_version mismatch")
        visibility = data.get("visibility", "private")
        if visibility not in {"private", "public"}:
            raise ValidationError("ExperienceSpec.visibility must be 'private' or 'public'")
        capabilities = _expect_mapping(data.get("capabilities", {}), "capabilities")
        cap_extra = set(capabilities) - {"search", "facets"}
        if cap_extra:
            raise ValidationError(f"capabilities has unknown fields: {sorted(cap_extra)}")
        search = capabilities.get("search", True)
        if not isinstance(search, bool):
            raise ValidationError("capabilities.search must be boolean")
        facets = _string_list(capabilities.get("facets"), "capabilities.facets")
        navigation = _expect_mapping(data.get("navigation", {}), "navigation")
        nav_extra = set(navigation) - {"default_sort"}
        if nav_extra:
            raise ValidationError(f"navigation has unknown fields: {sorted(nav_extra)}")
        default_sort = navigation.get("default_sort", "title")
        if default_sort not in {"title", "date", "source"}:
            raise ValidationError("navigation.default_sort must be title, date, or source")
        return cls(
            experience_id=_required_str(data, "experience_id", "ExperienceSpec"),
            title=_optional_str(data, "title", "ExperienceSpec"),
            collection_spec=_required_str(data, "collection_spec", "ExperienceSpec"),
            renderer=_required_str(data, "renderer", "ExperienceSpec"),
            visibility=visibility,
            facets=facets,
            search=search,
            default_sort=default_sort,
        )

    def to_dict(self) -> dict[str, Any]:
        out = {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "experience_id": self.experience_id,
            "collection_spec": self.collection_spec,
            "renderer": self.renderer,
            "visibility": self.visibility,
            "capabilities": {"search": self.search, "facets": list(self.facets)},
            "navigation": {"default_sort": self.default_sort},
        }
        if self.title is not None:
            out["title"] = self.title
        return out


def validate_item(raw: Any) -> dict[str, Any]:
    data = _expect_mapping(raw, "item")
    allowed = {"item_id", "kind", "title", "subtitle", "summary", "date", "contributors", "tags", "facets", "canonical_url", "source_ref"}
    extra = set(data) - allowed
    if extra:
        raise ValidationError(f"item has unknown fields: {sorted(extra)}")
    out: dict[str, Any] = {
        "item_id": _required_str(data, "item_id", "item"),
        "kind": _required_str(data, "kind", "item"),
        "title": _required_str(data, "title", "item"),
        "contributors": list(_string_list(data.get("contributors"), "item.contributors")),
        "tags": list(_string_list(data.get("tags"), "item.tags")),
    }
    for key in ("subtitle", "summary", "date"):
        value = _optional_str(data, key, "item")
        if value is not None:
            out[key] = value
    canonical_url = _optional_url(data, "canonical_url", "item")
    if canonical_url is not None:
        out["canonical_url"] = canonical_url
    facets = _expect_mapping(data.get("facets", {}), "item.facets")
    normalized_facets: dict[str, Any] = {}
    for key, value in facets.items():
        if not isinstance(key, str) or not key.strip():
            raise ValidationError("item.facets keys must be non-empty strings")
        if isinstance(value, (str, int, float, bool)) or value is None:
            normalized_facets[key] = value
        elif isinstance(value, list) and all(isinstance(x, (str, int, float, bool)) or x is None for x in value):
            normalized_facets[key] = value
        else:
            raise ValidationError(f"item.facets.{key} must be scalar, null, or scalar array")
    out["facets"] = normalized_facets
    source_ref = data.get("source_ref")
    if source_ref is not None:
        sr = _expect_mapping(source_ref, "item.source_ref")
        if set(sr) - {"authority", "object_id", "url"}:
            raise ValidationError("item.source_ref has unknown fields")
        normalized = {"authority": _required_str(sr, "authority", "item.source_ref"), "object_id": _required_str(sr, "object_id", "item.source_ref")}
        url = _optional_url(sr, "url", "item.source_ref")
        if url is not None:
            normalized["url"] = url
        out["source_ref"] = normalized
    return out


def validate_release(raw: Any) -> dict[str, Any]:
    data = _expect_mapping(raw, "release")
    schema_id = data.get("schema_id")
    if schema_id == "knowledge.collection-release":
        required = {"schema_id", "schema_version", "collection_id", "release_id", "title", "source", "items"}
    elif schema_id == "knowledge.experience-release":
        required = {"schema_id", "schema_version", "experience_id", "release_id", "collection", "renderer", "artifacts"}
    else:
        raise ValidationError(f"unsupported release schema_id: {schema_id!r}")
    missing = required - set(data)
    if missing:
        raise ValidationError(f"{schema_id}: missing fields: {sorted(missing)}")
    if data.get("schema_version") != 1:
        raise ValidationError(f"{schema_id}: schema_version must be 1")
    digest = data.get("payload_sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ValidationError(f"{schema_id}: payload_sha256 must be a 64-character digest")
    payload = {k: v for k, v in data.items() if k not in {"release_id", "payload_sha256"}}
    expected = sha256_value(payload)
    if digest != expected:
        raise ValidationError(f"{schema_id}: payload_sha256 does not match canonical payload")
    if data.get("release_id") != f"sha256:{expected[:16]}":
        raise ValidationError(f"{schema_id}: release_id does not match canonical payload")
    return data


def validate_document(raw: Any) -> Any:
    data = _expect_mapping(raw, "document")
    schema_id = data.get("schema_id")
    if schema_id == CollectionSpec.schema_id:
        return CollectionSpec.from_dict(data)
    if schema_id == ExperienceSpec.schema_id:
        return ExperienceSpec.from_dict(data)
    if schema_id in {"knowledge.collection-release", "knowledge.experience-release"}:
        return validate_release(data)
    raise ValidationError(f"unsupported schema_id: {schema_id!r}")
