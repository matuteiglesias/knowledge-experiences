from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .adapters import get_source_adapter
from .canonical import sha256_file, sha256_value, write_canonical_json
from .models import CollectionSpec, ExperienceSpec, ValidationError, validate_document
from .renderers import get_renderer


def read_json(path: Path) -> dict[str, Any]:
    path = Path(path)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValidationError(f"{path}: root must be an object")
    return raw


def read_typed(path: Path) -> Any:
    return validate_document(read_json(path))


def _select_items(spec: CollectionSpec, items: tuple[dict[str, Any], ...]) -> list[dict[str, Any]]:
    if spec.selection.mode == "all":
        selected = list(items)
    else:
        by_id = {item["item_id"]: item for item in items}
        missing = [item_id for item_id in spec.selection.item_ids if item_id not in by_id]
        if missing:
            raise ValidationError(f"collection selection references missing item_ids: {missing}")
        selected = [by_id[item_id] for item_id in spec.selection.item_ids]
    return sorted(selected, key=lambda item: item["item_id"])


def compile_collection(spec_path: Path, out_path: Path | None = None) -> dict[str, Any]:
    spec_path = Path(spec_path).resolve()
    spec = read_typed(spec_path)
    if not isinstance(spec, CollectionSpec):
        raise ValidationError(f"{spec_path}: expected {CollectionSpec.schema_id}")

    adapter = get_source_adapter(spec.source.adapter)
    loaded = adapter.load(spec.source, base_dir=spec_path.parent)
    selected = _select_items(spec, loaded.items)

    source_provenance: dict[str, Any] = {
        "authority": spec.source.authority,
        "adapter": spec.source.adapter,
        "path": spec.source.path,
        "sha256": loaded.sha256,
    }
    if spec.source.release_id is not None:
        source_provenance["release_id"] = spec.source.release_id

    payload: dict[str, Any] = {
        "schema_id": "knowledge.collection-release",
        "schema_version": 1,
        "collection_id": spec.collection_id,
        "title": spec.title,
        "source": source_provenance,
        "spec_sha256": sha256_file(spec_path),
        "items": selected,
    }
    if spec.description is not None:
        payload["description"] = spec.description

    release_hash = sha256_value(payload)
    release = dict(payload)
    release["release_id"] = f"sha256:{release_hash[:16]}"
    release["payload_sha256"] = release_hash

    if out_path is not None:
        write_canonical_json(Path(out_path), release)
    return release


def build_experience(spec_path: Path, out_dir: Path) -> dict[str, Any]:
    spec_path = Path(spec_path).resolve()
    spec = read_typed(spec_path)
    if not isinstance(spec, ExperienceSpec):
        raise ValidationError(f"{spec_path}: expected {ExperienceSpec.schema_id}")

    collection_spec_path = (spec_path.parent / spec.collection_spec).resolve()
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    collection_release_path = out_dir / "collection.release.json"
    collection_release = compile_collection(collection_spec_path, collection_release_path)

    renderer = get_renderer(spec.renderer)
    site_dir = out_dir / "site"
    artifacts = renderer.render(collection_release=collection_release, experience_spec=spec, out_dir=site_dir)

    artifact_records = []
    for artifact in sorted(artifacts, key=lambda p: p.relative_to(out_dir).as_posix()):
        artifact_records.append({"path": artifact.relative_to(out_dir).as_posix(), "sha256": sha256_file(artifact)})

    payload: dict[str, Any] = {
        "schema_id": "knowledge.experience-release",
        "schema_version": 1,
        "experience_id": spec.experience_id,
        "collection": {
            "collection_id": collection_release["collection_id"],
            "release_id": collection_release["release_id"],
            "sha256": sha256_file(collection_release_path),
        },
        "renderer": {"name": spec.renderer},
        "spec_sha256": sha256_file(spec_path),
        "artifacts": artifact_records,
    }
    release_hash = sha256_value(payload)
    release = dict(payload)
    release["release_id"] = f"sha256:{release_hash[:16]}"
    release["payload_sha256"] = release_hash
    write_canonical_json(out_dir / "experience.release.json", release)
    return release
