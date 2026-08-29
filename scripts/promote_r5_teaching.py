#!/usr/bin/env python3
"""Append the first discovered post-seed experience and record its E3 evidence."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiences" / "real" / "ldd-uba-exercise-catalog"
SOURCE_COMMIT = "1e8a3c400e1296055614e0dec627f7177c730537"
PATH_REGEX = r"content/notebooks/[0-9]{2}\.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    receipt = load(BASE / "source" / "source-receipt.json")
    collection = load(BASE / "release" / "collection.release.json")
    experience = load(BASE / "release" / "experience.release.json")
    proof = load(BASE / "e3-proof.json")
    records = receipt["record_count"]
    if records != 60:
        raise SystemExit(f"expected 60 numbered exercise pages from repaired repo.ldd-uba authority; materialized {records}")
    if receipt.get("path_regex") != PATH_REGEX:
        raise SystemExit("LDD receipt is missing the exact numbered-exercise path filter")
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
            "existing_surface": "repo.ldd-uba Hugo catalog of 60 numbered teaching exercises plus four category indexes",
            "source_authorities": ["repo.ldd-uba"],
            "code_pins": {"repo.ldd-uba": SOURCE_COMMIT},
            "exact_source_release": f"git:{SOURCE_COMMIT};source-index:sha256:{receipt['source_index_sha256']}",
            "collection_release": f"experiences/real/ldd-uba-exercise-catalog/release/collection.release.json#{collection['release_id']}",
            "renderer_profile": "static-navigator-frozen-snapshot",
            "rendered_artifact": "experiences/real/ldd-uba-exercise-catalog/release/site/index.html",
            "cross_repo_proof": "experiences/real/ldd-uba-exercise-catalog/e3-proof.json + .github/workflows/git-vertical-seam-proof.yml",
            "operational_evidence": None,
            "capabilities_reused": ["git-markdown-metadata-projection", "explicit-path-filter", "static-navigator", "deterministic-releases", "exact-git-cross-repo-proof"],
            "incremental_work": "bounded path filtering plus configuration/source pinning over the already-amortized Git Markdown projection, composition kernel and static navigator",
            "blocker": "none for the reproducible exercise catalog; E4 requires actual recurring teaching use or governed refresh demand",
            "observed_friction": "real use exposed upstream README drift (58 declared vs 60 numbered exercises) and four structural Hugo _index.md pages; the source authority was repaired and KX now filters the exact numbered exercise paths rather than conflating navigation with exercises",
            "v2_candidate": None,
            "engineering_evidence": [
                f"repo.ldd-uba@{SOURCE_COMMIT} explicitly documents 60 numbered exercises and four category indexes",
                f"R5 path-filtered exactly {records} numbered Markdown exercises under content/notebooks and produced CollectionRelease {collection['release_id']} plus ExperienceRelease {experience['release_id']}",
                f"persistent real-source CI reproduces the final artifact sha256 {proof['rendered_artifact_sha256']} from the exact repaired producer commit",
            ],
            "evidence_boundary": "E3 covers the exact 60 numbered teaching-exercise pages at the pinned Git commit and their frozen KX navigator; category _index.md pages, notebook executability, current-course membership, live deployment health and E4 operation are not claimed",
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
        "**16 governed experiences: 5 are E3, 1 is E1, and 10 remain E0.** R5 adds the first post-seed discovery: a real teaching-exercise corpus that was visible in the estate but semantically distinct from the original Course readings case.",
        "",
        "| # | Experience | Maturity | Engineering status | Current evidence |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        evidence = "declared / prior engineering evidence"
        if row["id"] == 16:
            evidence = f"60 exact numbered Git exercise pages → `{experience['release_id']}` + persistent real-source proof"
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
        "`repo.ldd-uba` owns a Hugo teaching catalog with 60 numbered exercise pages and four category `_index.md` navigation pages. KX uses an explicit repo-relative path filter to snapshot only `content/notebooks/[0-9]{2}.md`, then renders a separate immutable navigator and proves the full seam from the repaired producer commit. The original Hugo site remains the pedagogical/content authority.",
        "",
        "The first R5 attempt was useful drift sensing: the README claimed 58 exercises while the repository contained numbered exercises through 60, and a recursive Markdown projection also included four category indexes. The upstream README was repaired before the accepted source was repinned; the KX path boundary now states exactly what counts as an exercise.",
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

R5 adds the first experience discovered after the original 15-case census: the 60-page `repo.ldd-uba` teaching exercise catalog. It is kept separate from #10 Course readings because exercises and readings have different semantics.

## Exact real-source path

```text
repo.ldd-uba@{SOURCE_COMMIT}
        ↓  content/notebooks/[0-9]{{2}}.md (60 exact numbered pages)
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

## Drift discovered during materialization

The pre-R5 README declared 58 exercises. The actual source tree contained numbered exercise files through `60.md` plus four category `_index.md` pages. R5 therefore did not accept the naive 64-record recursive projection. The producer README was corrected first, and the accepted KX source boundary explicitly full-matches the 60 numbered exercise paths.

## Governance change

The census checker now preserves the original 15 entries as a minimum append-only baseline and requires contiguous IDs through the current count. This removes an accidental discovery ceiling without weakening any E1/E2/E3/E4 evidence requirement.

## Boundary

KX does not claim the notebooks execute, belong to a current course, or replace the upstream Hugo catalog. It freezes and proves the exact numbered teaching-exercise navigation corpus only. No renderer, domain schema, ordering model, or composition-kernel behavior was added; the only projection extension is an explicit provenance-bearing path filter.

## Result

The governed census becomes **16 experiences: 5×E3 + 1×E1 + 10×E0**.
"""
    (ROOT / "docs" / "R5_TEACHING_EXERCISE_CATALOG.md").write_text(r5, encoding="utf-8")
    print(f"R5 promotion complete: records={records} collection={collection['release_id']} experience={experience['release_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
