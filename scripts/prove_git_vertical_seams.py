#!/usr/bin/env python3
"""Rebuild accepted Git-backed vertical experiences from exact upstream commits.

This is a cross-repository proof, not a new source adapter. It reuses the bounded
Markdown materializer plus the accepted CollectionSpec/ExperienceSpec and fails
closed unless source projection, frozen releases and rendered artifact reproduce
exactly from the pinned producer checkout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CASES = {
    "thesis": {
        "dir": "economics-of-aggregation-programme",
        "source_repo": "matuteiglesias/thesis",
        "authority": "repo.thesis",
        "commit": "7265018750db0f96b69efd4048aedad06ad803fc",
        "scope_root": "docs",
        "mode": "all-markdown",
        "collection_id": "economics-of-aggregation-programme",
        "title": "Economics of Aggregation programme — exact document index",
        "description": "Metadata-only index of exact versioned research-programme documents; repo.thesis retains content and status authority.",
        "kind": "research-document",
    },
    "journal": {
        "dir": "working-memory-journal",
        "source_repo": "matuteiglesias/journal",
        "authority": "repo.journal",
        "commit": "11fc6ea42e13866cd952e4957c26dd2e55ef78d7",
        "scope_root": "content",
        "mode": "explicit-publish",
        "collection_id": "working-memory-journal",
        "title": "Working-memory journal — explicit-publication collection",
        "description": "Conservative metadata-only subset of exact versioned journal notes carrying explicit publish:true; Quartz remains publication authority.",
        "kind": "journal-note",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args: str) -> None:
    subprocess.run(list(args), check=True)


def assert_same(actual: Path, expected: Path, label: str) -> None:
    if not actual.is_file() or not expected.is_file():
        raise SystemExit(f"{label}: missing comparison file")
    a = sha256(actual)
    e = sha256(expected)
    if a != e:
        raise SystemExit(f"{label}: sha mismatch regenerated={a} accepted={e}")


def prove_case(name: str, source_root: Path) -> dict:
    cfg = CASES[name]
    source_root = source_root.resolve()
    actual_commit = subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if actual_commit != cfg["commit"]:
        raise SystemExit(f"{name}: checkout mismatch {actual_commit} != {cfg['commit']}")

    accepted = ROOT / "experiences" / "real" / cfg["dir"]
    accepted_e2 = json.loads((accepted / "e2-proof.json").read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory(prefix=f"kx-r4-{name}-") as tmp_raw:
        tmp = Path(tmp_raw)
        regenerated = tmp / cfg["dir"]
        run(
            "python",
            str(ROOT / "scripts" / "materialize_markdown_collection.py"),
            "--repo-root", str(source_root),
            "--source-repo", cfg["source_repo"],
            "--authority", cfg["authority"],
            "--commit", cfg["commit"],
            "--scope-root", cfg["scope_root"],
            "--mode", cfg["mode"],
            "--collection-id", cfg["collection_id"],
            "--title", cfg["title"],
            "--description", cfg["description"],
            "--kind", cfg["kind"],
            "--out-dir", str(regenerated),
        )
        shutil.copy2(accepted / "snapshot.experience.json", regenerated / "snapshot.experience.json")

        assert_same(regenerated / "source" / "items.jsonl", accepted / "source" / "items.jsonl", f"{name} source projection")
        assert_same(regenerated / "source" / "source-receipt.json", accepted / "source" / "source-receipt.json", f"{name} source receipt")
        assert_same(regenerated / "collection.json", accepted / "collection.json", f"{name} collection spec")

        run("kx", "doctor", str(regenerated / "snapshot.experience.json"))
        run("kx", "build", str(regenerated / "snapshot.experience.json"), "--out", str(regenerated / "release"))

        assert_same(regenerated / "release" / "collection.release.json", accepted / "release" / "collection.release.json", f"{name} collection release")
        assert_same(regenerated / "release" / "experience.release.json", accepted / "release" / "experience.release.json", f"{name} experience release")
        assert_same(regenerated / "release" / "site" / "index.html", accepted / "release" / "site" / "index.html", f"{name} rendered artifact")

        release = json.loads((regenerated / "release" / "experience.release.json").read_text(encoding="utf-8"))
        artifact_sha = sha256(regenerated / "release" / "site" / "index.html")
        if release.get("release_id") != accepted_e2.get("experience_release_id"):
            raise SystemExit(f"{name}: regenerated ExperienceRelease id differs from accepted E2 proof")
        if artifact_sha != accepted_e2.get("rendered_artifact_sha256"):
            raise SystemExit(f"{name}: regenerated artifact hash differs from accepted E2 proof")

    return {
        "case": name,
        "source_repo": cfg["source_repo"],
        "source_commit": cfg["commit"],
        "collection_release_id": accepted_e2["collection_release_id"],
        "experience_release_id": accepted_e2["experience_release_id"],
        "rendered_artifact_sha256": accepted_e2["rendered_artifact_sha256"],
        "result": "pass",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--thesis-root", required=True)
    parser.add_argument("--journal-root", required=True)
    parser.add_argument("--write-proofs", action="store_true")
    args = parser.parse_args()

    results = [
        prove_case("thesis", Path(args.thesis_root)),
        prove_case("journal", Path(args.journal_root)),
    ]
    if args.write_proofs:
        for result in results:
            cfg = CASES[result["case"]]
            out = ROOT / "experiences" / "real" / cfg["dir"] / "e3-proof.json"
            payload = {
                "schema_id": "knowledge.e3-cross-repo-proof",
                "schema_version": 1,
                "proof": "exact-git-source-to-frozen-experience",
                **result,
            }
            out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
