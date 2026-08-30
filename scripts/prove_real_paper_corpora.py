#!/usr/bin/env python3
"""Rebuild R8 experiences from one exact Paper KB fixture commit and compare bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from knowledge_experiences.compiler import build_experience

ROOT = Path(__file__).resolve().parents[1]
PAPER_KB_COMMIT = "e82e82deb646f30707306cd13ff8ba279c8bad50"
TESIS_SHA256 = "648d8461929629e5b13385510048f77ead7000b98318fdf87d22fe9332f28a1f"
ERIC_SHA256 = "273a484b873d5ae6f9041b24e3c8b4906d23d0683b26941c95713665353f1b41"

CASES = {
    "thesis-bibliography": {
        "producer": "fixture/corpora/tesis-cited/catalog/paper.catalog-record.v1.jsonl",
        "source": "experiences/real/thesis-bibliography/source/paper.catalog-record.v1.jsonl",
        "count": 19,
        "source_sha256": TESIS_SHA256,
    },
    "author-works": {
        "producer": "fixture/corpora/tesis-cited/catalog/paper.catalog-record.v1.jsonl",
        "source": "experiences/real/thesis-bibliography/source/paper.catalog-record.v1.jsonl",
        "count": 2,
        "source_sha256": TESIS_SHA256,
    },
    "fcv-literature-corpus": {
        "producer": "fixture/corpora/eric-mv/catalog/paper.catalog-record.v1.jsonl",
        "source": "experiences/real/fcv-literature-corpus/source/paper.catalog-record.v1.jsonl",
        "count": 7,
        "source_sha256": ERIC_SHA256,
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_equal(left: Path, right: Path, label: str) -> None:
    if left.read_bytes() != right.read_bytes():
        raise SystemExit(f"R8 proof failed: {label} differs: {left} != {right}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-kb-root", required=True, type=Path)
    args = parser.parse_args()
    paper_kb = args.paper_kb_root.resolve()

    head = subprocess.check_output(
        ["git", "-C", str(paper_kb), "rev-parse", "HEAD"], text=True
    ).strip()
    if head != PAPER_KB_COMMIT:
        raise SystemExit(f"R8 proof failed: Paper KB HEAD {head} != {PAPER_KB_COMMIT}")

    eric_manifest = json.loads(
        (paper_kb / "fixture/corpora/eric-mv/fixture-manifest.json").read_text(encoding="utf-8")
    )
    if eric_manifest.get("fixture_level") != "consumer":
        raise SystemExit("R8 proof failed: eric-mv is not a consumer fixture")
    if eric_manifest.get("source_pdf_count") != 7 or eric_manifest.get("chunk_set_count") != 7:
        raise SystemExit("R8 proof failed: eric-mv expected 7 PDFs and 7 chunk sets")

    checked_sources: set[tuple[str, str]] = set()
    for case in CASES.values():
        key = (case["producer"], case["source"])
        if key in checked_sources:
            continue
        checked_sources.add(key)
        producer = paper_kb / case["producer"]
        frozen = ROOT / case["source"]
        if sha256(producer) != case["source_sha256"]:
            raise SystemExit(f"R8 proof failed: producer hash drift for {producer}")
        if sha256(frozen) != case["source_sha256"]:
            raise SystemExit(f"R8 proof failed: frozen source hash drift for {frozen}")
        require_equal(producer, frozen, "producer projection")

    with tempfile.TemporaryDirectory(prefix="kx-r8-") as td:
        temp_root = Path(td)
        for experience_id, case in CASES.items():
            base = ROOT / "experiences/real" / experience_id
            generated = temp_root / experience_id
            build_experience(base / "snapshot.experience.json", generated)

            for rel in ("collection.release.json", "experience.release.json", "site/index.html"):
                require_equal(generated / rel, base / "release" / rel, f"{experience_id}/{rel}")

            collection = json.loads((generated / "collection.release.json").read_text(encoding="utf-8"))
            if len(collection["items"]) != case["count"]:
                raise SystemExit(
                    f"R8 proof failed: {experience_id} expected {case['count']} items, got {len(collection['items'])}"
                )
            if collection["source"]["sha256"] != case["source_sha256"]:
                raise SystemExit(f"R8 proof failed: {experience_id} source hash mismatch")
            if PAPER_KB_COMMIT not in collection["source"].get("release_id", ""):
                raise SystemExit(f"R8 proof failed: {experience_id} source release does not pin Paper KB")

            if experience_id == "author-works":
                ids = {item["item_id"] for item in collection["items"]}
                if ids != {"paper_340915ba55", "paper_7eac0538e3"}:
                    raise SystemExit(f"R8 proof failed: unexpected Angus Deaton subset {sorted(ids)}")
                if not all("Angus Deaton" in item["contributors"] for item in collection["items"]):
                    raise SystemExit("R8 proof failed: author facet did not survive")
            if experience_id == "fcv-literature-corpus":
                if not all("Eric Mvukiyehe" in item["contributors"] for item in collection["items"]):
                    raise SystemExit("R8 proof failed: eric-mv membership includes a non-Eric record")

            proof = json.loads((base / "e3-proof.json").read_text(encoding="utf-8"))
            experience = json.loads((generated / "experience.release.json").read_text(encoding="utf-8"))
            if proof["collection_release_id"] != collection["release_id"]:
                raise SystemExit(f"R8 proof failed: {experience_id} collection proof drift")
            if proof["experience_release_id"] != experience["release_id"]:
                raise SystemExit(f"R8 proof failed: {experience_id} experience proof drift")
            if proof["rendered_artifact_sha256"] != sha256(generated / "site/index.html"):
                raise SystemExit(f"R8 proof failed: {experience_id} rendered artifact drift")

            print(
                f"R8 {experience_id}: PASS "
                f"collection={collection['release_id']} experience={experience['release_id']} items={len(collection['items'])}"
            )

    print("R8 real Paper KB corpus fan-out: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
