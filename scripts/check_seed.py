#!/usr/bin/env python3
"""Dependency-free integrity check for the governed seed.

This is intentionally structural, not a substitute for future V1 schema/runtime tests.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "SYSTEM.yaml",
    "AGENTS.md",
    "docs/ARCHITECTURE.md",
    "docs/BUILD_BUNDLE.md",
    "docs/EXPERIENCE_CENSUS.md",
    "docs/CROSS_REPO_HANDOFFS.md",
]

REQUIRED_SYSTEM_MARKERS = [
    "repo.knowledge-experiences",
    "knowledge experience composition authority",
    "repo.knowledge-ecosystem-docs",
    "repo.kb-contracts",
]

REQUIRED_BUNDLE_MARKERS = [
    "Wave V1.1",
    "Wave V1.2",
    "Wave V1.3",
    "Wave V1.4",
    "Wave V1.5",
    "Wave V2",
    "Wave W5b",
]

REQUIRED_CENSUS_MARKERS = [
    "Thesis bibliography",
    "Author works",
    "Working-paper series",
    "LCD institutional corpus",
    "Economics of Aggregation programme",
    "Policy/research dossier",
]


def require_file(path: str) -> Path:
    full = ROOT / path
    if not full.is_file():
        raise SystemExit(f"missing required seed file: {path}")
    return full


def require_markers(path: str, markers: list[str]) -> None:
    text = require_file(path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit(f"{path}: missing required markers: {missing}")


def main() -> int:
    for path in REQUIRED_FILES:
        require_file(path)

    require_markers("SYSTEM.yaml", REQUIRED_SYSTEM_MARKERS)
    require_markers("docs/BUILD_BUNDLE.md", REQUIRED_BUNDLE_MARKERS)
    require_markers("docs/EXPERIENCE_CENSUS.md", REQUIRED_CENSUS_MARKERS)

    print("knowledge-experiences seed integrity: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
