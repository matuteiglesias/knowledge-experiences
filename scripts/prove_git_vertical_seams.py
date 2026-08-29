#!/usr/bin/env python3
"""Rebuild accepted Git-backed vertical experiences from exact upstream commits.

This is a cross-repository proof, not a new source adapter. It reuses the bounded
Markdown materializer plus accepted CollectionSpec/ExperienceSpec files and fails
closed unless source projection, frozen releases and rendered artifact reproduce
exactly from each pinned producer checkout.
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
    "ldd": {
        "dir": "ldd-uba-exercise-catalog",
        "source_repo": "matuteiglesias/ldd-uba",
        "authority": "repo.ldd-uba",
        "commit": "a67a9d89c1464e68f8b701c9d3ab44c775042bfc",
        "scope_root": "content/notebooks",
        "mode": "all-markdown",
        "collection_id": "ldd-uba-exercise-catalog",
        "title": "LDD UBA — frozen teaching exercise catalog",
        "description": "Metadata-only index of the exact versioned teaching exercise pages; repo.ldd-uba retains pedagogical content and Hugo navigation authority.",
        "kind": "teaching-exercise",
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
    accepted_collection = json.loads((accepted / "release" / "collection.release.json").read_text(encoding="utf-8"))
    accepted_experience = json.loads((accepted / "release" / "experience.release.json").read_text(encoding="utf-8"))
    accepted_artifact = accepted / "release" / "site" / "index.html"

    with tempfile.TemporaryDirectory(prefix=f"kx-git-seam-{name}-") as tmp_raw:
        regenerated = Path(tmp_raw) / cfg["dir"]
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
        assert_same(regenerated / "release" / "site" / "index.html", accepted_artifact, f"{name} rendered artifact")

    return {
        "case": name,
        "source_repo": cfg["source_repo"],
        "source_commit": cfg["commit"],
        "collection_release_id": accepted_collection["release_id"],
        "experience_release_id": accepted_experience["release_id"],
        "rendered_artifact_sha256": sha256(accepted_artifact),
        "result": "pass",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--thesis-root")
    parser.add_argument("--journal-root")
    parser.add_argument("--ldd-root")
    parser.add_argument("--write-proofs", action="store_true")
    args = parser.parse_args()

    requested = []
    if args.thesis_root:
        requested.append(("thesis", Path(args.thesis_root)))
    if args.journal_root:
        requested.append(("journal", Path(args.journal_root)))
    if args.ldd_root:
        requested.append(("ldd", Path(args.ldd_root)))
    if not requested:
        raise SystemExit("provide at least one producer checkout")

    results = [prove_case(name, root) for name, root in requested]
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
