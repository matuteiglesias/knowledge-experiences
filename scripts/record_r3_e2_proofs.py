#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for dirname in ("economics-of-aggregation-programme", "working-memory-journal"):
        base = ROOT / "experiences" / "real" / dirname
        collection = load(base / "release" / "collection.release.json")
        experience = load(base / "release" / "experience.release.json")
        artifact = base / "release" / "site" / "index.html"
        if not artifact.is_file() or artifact.stat().st_size == 0:
            raise SystemExit(f"missing human artifact for {dirname}")
        proof = {
            "schema_id": "knowledge.e2-snapshot-proof",
            "schema_version": 1,
            "result": "pass",
            "collection_release_id": collection["release_id"],
            "experience_release_id": experience["release_id"],
            "records": len(collection["items"]),
            "rendered_artifact": "release/site/index.html",
            "rendered_artifact_sha256": sha256(artifact),
        }
        (base / "e2-proof.json").write_text(
            json.dumps(proof, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(dirname, proof["experience_release_id"], proof["records"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
