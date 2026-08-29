#!/usr/bin/env python3
"""Append the first discovered post-seed experience and record its E3 evidence."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiences" / "real" / "ldd-uba-exercise-catalog"
SOURCE_COMMIT = "a67a9d89c1464e68f8b701c9d3ab44c775042bfc"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    receipt = load(BASE / "source" / "source-receipt.json")
    collection = load(BASE / "release" / "collection.release.json")
    experience = load(BASE / "release" / "experience.release.json")
    proof = load(BASE / "e3-proof.json")
    records = receipt["record_count"]
    if records != 58:
        raise SystemExit(f"expected the 58 exercise pages declared by repo.ldd-uba; materialized {records}")
    if proof.get("result") != "pass" or proof.get("source_commit") != SOURCE_COMMIT:
        raise SystemExit("LDD E3 proof missing or pinned to the wrong producer commit")
    if proof.get("collection_release_id") != collection.get("release_id"):
        raise SystemExit("LDD CollectionRelease proof mismatch")
    if proof.get("experience_release_id") != experience.get("release_id"):
        raise SystemExit("LDD ExperienceRelease proof mismatch")

    census_path = ROOT / "docs" / "experience-census.v1.json"
    census = load(census_path)
    rows = census["experiences"]
    if len(rows) != 15 or rows[-1]["id"] != 15:
        raise SystemExit("R5 expects the accepted 15-entry seed census as its parent")
    rows.append(
        {
            "id": 16,
            "experience_id": "ldd-uba-exercise-catalog",
            "name": "LDD UBA teaching exercise catalog",
            "composition_maturity": "E3",
            "engineering_status": "proven_real_source_seam",
            "existing_surface": "repo.ldd-uba Hugo catalog of 58 teaching exercises/notebooks",
            "source_authorities": ["repo.ldd-uba"],
            "code_pins": {"repo.ldd-uba": SOURCE_COMMIT},
            "exact_source_release": f"git:{SOURCE_COMMIT};source-index:sha256:{receipt['source_index_sha256']}",
            "collection_release": f"experiences/real/ldd-uba-exercise-catalog/release/collection.release.json#{collection['release_id']}",
            "renderer_profile": "static-navigator-frozen-snapshot",
            "rendered_artifact": "experiences/real/ldd-uba-exercise-catalog/release/site/index.html",
            "cross_repo_proof": "experiences/real/ldd-uba-exercise-catalog/e3-proof.json + .github/workflows/git-vertical-seam-proof.yml",
            "operational_evidence": None,
            "capabilities_reused": ["git-markdown-metadata-projection", "static-navigator", "deterministic-releases", "exact-git-cross-repo-proof"],
            "incremental_work": "configuration and source pinning only over the already-amortized Git Markdown projection, composition kernel and static navigator",
            "blocker": "none for the reproducible exercise catalog; E4 requires actual recurring teaching use or governed refresh demand",
            "observed_friction": "the 58 exercise pages form a clean flat corpus; no ordered-group or course-reading semantics were needed, so #10 Course readings remains a separate unresolved experience",
            "v2_candidate": None,
            "engineering_evidence": [
                f"repo.ldd-uba@{SOURCE_COMMIT} contains exactly 58 tracked Markdown exercise pages under content/notebooks",
                f"R5 produced CollectionRelease {collection['release_id']} and ExperienceRelease {experience['release_id']} without a new source adapter, renderer, or kernel change",
                f"persistent real-source CI reproduces the final artifact sha256 {proof['rendered_artifact_sha256']} from the exact producer commit",
            ],
            "evidence_boundary": "E3 covers the exact 58-page teaching exercise corpus at the pinned Git commit and its frozen KX navigator; it does not assert notebook executability, current-course membership, live deployment health, or E4 operation",
            "next_real_action": "use the frozen exercise navigator in a real teaching/preparation workflow or perform an explicit refresh from a newer LDD commit; keep #10 Course readings separate until a real reading-list source is selected",
        }
    )
    census["as_of"] = "2026-08-29"
    census_path.write_text(json.dumps(census, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    counts = Counter(row["composition_maturity"] for row in rows)
    expected = Counter({"E0": 10, "E1": 1, "E3": 5})
    if counts != expected:
        raise SystemExit(f"unexpected maturity distribution after R5: {counts}")

    human = [
        "# Experience Census — expanding executable real-use ladder",
        "",
        "The machine-readable authority is `docs/experience-census.v1.json`. The original 15-entry census is now a governed baseline, not a permanent ceiling: new concrete experiences may be appended with contiguous IDs and the same strict E0–E4 evidence rules.",
        "",
        "## Current frontier",
        "",
        "**16 governed experiences: 5 are E3, 1 is E1, and 10 remain E0.** R5 adds the first post-seed discovery: a real teaching exercise corpus that was visible in the estate but semantically distinct from the original Course readings case.",
        "",
        "| # | Experience | Maturity | Engineering status | Current evidence |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        evidence = "declared / prior engineering evidence"
        if row["id"] == 16:
            evidence = f"58 exact Git exercise pages → `{experience['release_id']}` + persistent real-source proof"
        elif row["id"] in {11, 12}:
            evidence = "exact Git producer → deterministic frozen experience + persistent proof"
        elif row["id"] == 13:
            evidence = "32 exact-Git metadata records → reproducible E1 CollectionRelease"
        elif row["id"] in {8, 9}:
            evidence = "trusted live LCD source → rendered real-source experience + executable proof"
        human.append(f"| {row['id']} | {row['name']} | **{row['composition_maturity']}** | {row['engineering_status']} | {evidence} |")
    human += [
        "",
        "## R5 interpretation",
        "",
        "`repo.ldd-uba` owns a Hugo teaching catalog and exactly 58 tracked exercise pages under `content/notebooks/`. KX snapshots only metadata and exact source pointers, renders a separate immutable navigator, and proves the full seam from the pinned producer commit. The original Hugo site remains the pedagogical/content authority.",
        "",
        "This is deliberately **not** census #10 Course readings. Exercises and readings are different pedagogical objects; collapsing them merely to fill an existing row would weaken the ledger. The census therefore grows append-only to #16 instead.",
        "",
        "## Next frontier",
        "",
        "Paper KB remains the highest-value blocked scientific lane. Separately, the growing census can now discover additional real experiences rather than forcing the estate into the original 15 hypotheses. E4 still requires actual operation/use evidence, not more CI.",
        "",
    ]
    (ROOT / "docs" / "EXPERIENCE_CENSUS.md").write_text("\n".join(human), encoding="utf-8")

    system_path = ROOT / "SYSTEM.yaml"
    system = system_path.read_text(encoding="utf-8")
    if "    - repo.ldd-uba\n" not in system:
        system = system.replace("  vertical_experiences:\n    - repo.thesis\n    - repo.journal\n", "  vertical_experiences:\n    - repo.thesis\n    - repo.journal\n    - repo.ldd-uba\n")
    system = re.sub(r"  count: \d+\n", "  count: 16\n", system)
    system = re.sub(
        r"  maturity_snapshot:\n(?:    E\d: \d+\n)+",
        "  maturity_snapshot:\n    E3: 5\n    E1: 1\n    E0: 10\n",
        system,
    )
    system = re.sub(
        r"  phase: .*\n  next_gate: .*\n",
        "  phase: expanding-executable-multi-domain-ladder\n  next_gate: paper-real-corpus-or-e4-operational-use\n",
        system,
    )
    system_path.write_text(system, encoding="utf-8")

    r5 = f"""# R5 — teaching exercise catalog enters the ladder

R5 adds the first experience discovered after the original 15-case census: the 58-page `repo.ldd-uba` teaching exercise catalog. It is kept separate from #10 Course readings because exercises and readings have different semantics.

## Exact real-source path

```text
repo.ldd-uba@{SOURCE_COMMIT}
        ↓  content/notebooks/*.md (58 exact tracked pages)
metadata-only Git projection
        ↓
CollectionRelease {collection['release_id']}
        ↓
static-navigator
        ↓
ExperienceRelease {experience['release_id']}
        ↓
frozen teaching exercise navigator
        ↓
persistent cross-repo reproduction proof
```

Final artifact SHA-256: `{proof['rendered_artifact_sha256']}`.

## Governance change

The census checker now preserves the original 15 entries as a minimum append-only baseline and requires contiguous IDs through the current count. This removes an accidental discovery ceiling without weakening any E1/E2/E3/E4 evidence requirement.

## Boundary

KX does not claim the notebooks execute, belong to a current course, or replace the upstream Hugo catalog. It freezes and proves the exact teaching-exercise navigation corpus only. No source adapter, renderer, domain schema, ordering model, or kernel behavior was added.

## Result

The governed census becomes **16 experiences: 5×E3 + 1×E1 + 10×E0**.
"""
    (ROOT / "docs" / "R5_TEACHING_EXERCISE_CATALOG.md").write_text(r5, encoding="utf-8")
    print(f"R5 promotion complete: records={records} collection={collection['release_id']} experience={experience['release_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
