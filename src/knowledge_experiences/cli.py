from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from .canonical import sha256_file
from .compiler import build_experience, compile_collection, read_json, read_typed
from .models import ExperienceSpec, ValidationError, validate_document


def _print(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def _tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def cmd_validate(path: str) -> int:
    doc = read_json(Path(path))
    parsed = validate_document(doc)
    _print({"ok": True, "schema_id": doc["schema_id"], "model": type(parsed).__name__})
    return 0


def cmd_compile_collection(path: str, out: str) -> int:
    release = compile_collection(Path(path), Path(out))
    _print({
        "ok": True,
        "collection_id": release["collection_id"],
        "release_id": release["release_id"],
        "items": len(release["items"]),
        "output": out,
    })
    return 0


def cmd_build(path: str, out: str) -> int:
    release = build_experience(Path(path), Path(out))
    _print({
        "ok": True,
        "experience_id": release["experience_id"],
        "release_id": release["release_id"],
        "artifacts": release["artifacts"],
        "output": out,
    })
    return 0


def cmd_doctor(path: str) -> int:
    spec_path = Path(path).resolve()
    parsed = read_typed(spec_path)
    if not isinstance(parsed, ExperienceSpec):
        raise ValidationError("doctor expects an ExperienceSpec")

    with tempfile.TemporaryDirectory(prefix="kx-doctor-a-") as a, tempfile.TemporaryDirectory(prefix="kx-doctor-b-") as b:
        release_a = build_experience(spec_path, Path(a))
        release_b = build_experience(spec_path, Path(b))
        hashes_a = _tree_hashes(Path(a))
        hashes_b = _tree_hashes(Path(b))
        stable = release_a == release_b and hashes_a == hashes_b
        if not stable:
            raise ValidationError("determinism check failed: identical inputs produced different outputs")
        _print({
            "ok": True,
            "experience_id": parsed.experience_id,
            "deterministic": True,
            "release_id": release_a["release_id"],
            "files": hashes_a,
        })
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kx", description="Compose governed knowledge into reproducible experiences.")
    sub = p.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("path")

    compile_p = sub.add_parser("compile-collection")
    compile_p.add_argument("path")
    compile_p.add_argument("--out", required=True)

    build = sub.add_parser("build")
    build.add_argument("path")
    build.add_argument("--out", required=True)

    doctor = sub.add_parser("doctor")
    doctor.add_argument("path")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "validate":
            return cmd_validate(args.path)
        if args.command == "compile-collection":
            return cmd_compile_collection(args.path, args.out)
        if args.command == "build":
            return cmd_build(args.path, args.out)
        if args.command == "doctor":
            return cmd_doctor(args.path)
        raise AssertionError(args.command)
    except ValidationError as exc:
        raise SystemExit(f"kx: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
