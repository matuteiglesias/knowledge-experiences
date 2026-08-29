#!/usr/bin/env python3
"""Promote R2 multi-lane real-source collections to E1 from checked-in evidence."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONFIG = {
    11: {
        "dir": "economics-of-aggregation-programme",
        "authority": "repo.thesis",
        "source_commit": "7265018750db0f96b69efd4048aedad06ad803fc",
        "incremental_work": "bounded Git-backed Markdown metadata snapshot plus the existing generic jsonl adapter; no duplicate Docusaurus renderer",
        "blocker": "a distinct derived consumer is required before E2; the existing Docusaurus portal remains the authoritative human experience",
        "observed_friction": "research status, historical/current authority and curated reading trails remain substantive upstream semantics and are not inferred by Knowledge Experiences",
        "evidence_boundary": "E1 covers a machine-readable metadata collection pointing at exact versioned thesis-programme documents; document bodies and status semantics remain repo.thesis-owned, and no second human UI is claimed",
        "next_real_action": "consume this CollectionRelease in a genuinely distinct derived workflow before considering E2 or ordered-trail semantics",
    },
    12: {
        "dir": "working-memory-journal",
        "authority": "repo.journal",
        "source_commit": "11fc6ea42e13866cd952e4957c26dd2e55ef78d7",
        "incremental_work": "bounded metadata snapshot of only notes with explicit publish:true using the existing generic jsonl adapter; Quartz remains the publication renderer",
        "blocker": "a distinct downstream use is required before E2; editorial publication eligibility remains owned by repo.journal rather than Knowledge Experiences",
        "observed_friction": "publication eligibility is real semantic governance; R2 therefore selects only explicit publish:true and refuses to reinterpret publish:false or draft material",
        "evidence_boundary": "E1 covers only metadata and exact Git pointers for the conservative explicit-publication subset; it does not assert a live deployment, republish note bodies, or redefine Quartz filtering",
        "next_real_action": "use the release for a distinct publication/synthesis workflow and compare its membership with the vertical's own public output before raising maturity",
    },
    13: {
        "dir": "knowledge-ecosystem-technical-docs",
        "authority": "repo.knowledge-ecosystem-docs",
        "source_commit": "ab59145a0378edc5f56b61e03951f93ca018c60a",
        "incremental_work": "bounded architecture-doc metadata snapshot plus the existing generic jsonl adapter; no duplicate technical navigator",
        "blocker": "a distinct docs-derived consumer is required before E2; the existing architecture/control surface already solves primary human navigation",
        "observed_friction": "none at the collection boundary; document semantics and architectural authority remain entirely upstream",
        "evidence_boundary": "E1 is a reproducible metadata CollectionRelease over exact architecture documents, not a replacement docs site and not a copy of document bodies",
        "next_real_action": "use this release as input to a distinct synthesis, agent-context, or cross-estate navigation task before adding a renderer",
    },
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    evidence = {}
    for row_id, cfg in CONFIG.items():
        base = ROOT / "experiences" / "real" / cfg["dir"]
        receipt = load(base / "source" / "source-receipt.json")
        release = load(base / "release" / "collection.release.json")
        if receipt["source_authority"] != cfg["authority"]:
            raise SystemExit(f"row {row_id}: authority mismatch")
        if receipt["source_commit"] != cfg["source_commit"]:
            raise SystemExit(f"row {row_id}: source commit mismatch")
        if release["source"].get("release_id") != f"git:{cfg['source_commit']}":
            raise SystemExit(f"row {row_id}: collection release source pin mismatch")
        if len(release["items"]) != receipt["record_count"] or not release["items"]:
            raise SystemExit(f"row {row_id}: non-empty membership/count invariant failed")
        evidence[row_id] = (receipt, release)

    census_path = ROOT / "docs" / "experience-census.v1.json"
    census = load(census_path)
    rows = {row["id"]: row for row in census["experiences"]}
    for row_id, cfg in CONFIG.items():
        receipt, release = evidence[row_id]
        row = rows[row_id]
        row.update(
            {
                "composition_maturity": "E1",
                "exact_source_release": f"git:{cfg['source_commit']}",
                "collection_release": f"experiences/real/{cfg['dir']}/release/collection.release.json#{release['release_id']}",
                "capabilities_reused": ["jsonl", "deterministic-releases", "exact-git-source-pinning"],
                "incremental_work": cfg["incremental_work"],
                "blocker": cfg["blocker"],
                "observed_friction": cfg["observed_friction"],
                "engineering_evidence": row["engineering_evidence"] + [
                    f"R2 exact Git snapshot {cfg['source_commit']} produced {receipt['record_count']} metadata records and CollectionRelease {release['release_id']}"
                ],
                "evidence_boundary": cfg["evidence_boundary"],
                "next_real_action": cfg["next_real_action"],
            }
        )
    census["as_of"] = "2026-08-29"
    census_path.write_text(json.dumps(census, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    counts = Counter(row["composition_maturity"] for row in census["experiences"])
    if counts != Counter({"E0": 10, "E1": 3, "E3": 2}):
        raise SystemExit(f"unexpected maturity distribution after R2: {counts}")

    human = [
        "# Experience Census — multi-lane real-use frontier",
        "",
        "The machine-readable authority is `docs/experience-census.v1.json`. `E0`–`E4` remains strict: a concrete experience advances only on evidence appropriate to that rung.",
        "",
        "## Current frontier",
        "",
        "**2 experiences are E3, 3 are E1, and 10 remain E0.** R2 intentionally populated the lower rung across three independent public Git producers instead of manufacturing duplicate human interfaces.",
        "",
        "| # | Experience | Maturity | Engineering status | Current evidence |",
        "|---|---|---|---|---|",
    ]
    for row in census["experiences"]:
        evidence_text = "declared / prior engineering evidence"
        if row["id"] in evidence:
            receipt, release = evidence[row["id"]]
            evidence_text = f"{receipt['record_count']} exact-Git metadata records → `{release['release_id']}`"
        elif row["id"] in {8, 9}:
            evidence_text = "trusted live LCD source → rendered real-source experience + executable proof"
        human.append(
            f"| {row['id']} | {row['name']} | **{row['composition_maturity']}** | {row['engineering_status']} | {evidence_text} |"
        )
    human += [
        "",
        "## R2 interpretation",
        "",
        "The three E1 releases are deliberately **collection-only**. `repo.thesis`, `repo.journal`, and `repo.knowledge-ecosystem-docs` already own mature human surfaces; Knowledge Experiences does not gain maturity by cloning Docusaurus or Quartz. E1 means the exact real source can now cross the composition boundary reproducibly. E2 waits for a distinct human-facing use that creates additional value.",
        "",
        "The Journal release is stricter still: only notes carrying explicit `publish: true` metadata are admitted, while `publish: false`, drafts and excluded private/template paths are not reinterpreted downstream.",
        "",
        "Paper KB remains E0 in the concrete census because its current repository surface contains real production machinery and fixtures but no approved real versioned corpus selected for these experiences. That boundary is preserved rather than promoting fixtures.",
        "",
        "## Next frontier",
        "",
        "The highest-information next moves are: a real approved Paper KB corpus to populate the scientific lane; or one genuinely distinct consumer of an R2 CollectionRelease to justify E2. Broad V2 construction is still not warranted.",
        "",
    ]
    (ROOT / "docs" / "EXPERIENCE_CENSUS.md").write_text("\n".join(human), encoding="utf-8")

    system_path = ROOT / "SYSTEM.yaml"
    system = system_path.read_text(encoding="utf-8")
    system = re.sub(
        r"  maturity_snapshot:\n(?:    E\d: \d+\n)+",
        "  maturity_snapshot:\n    E3: 2\n    E1: 3\n    E0: 10\n",
        system,
    )
    system = re.sub(r"  phase: .*\n  next_gate: .*\n", "  phase: multi-lane-real-use-active\n  next_gate: paper-real-corpus-or-distinct-e2-consumer\n", system)
    system_path.write_text(system, encoding="utf-8")

    r2_lines = [
        "# R2 — multi-lane E1 source releases",
        "",
        "R2 deliberately moves three mature verticals only to **E1**. Their existing Docusaurus/Quartz sites remain the human authorities; this tranche proves a reproducible composition boundary without duplicating those products.",
        "",
        "| Census | Producer | Exact commit | Scope | Records | CollectionRelease |",
        "|---|---|---|---|---:|---|",
    ]
    for row_id in (11, 12, 13):
        cfg = CONFIG[row_id]
        receipt, release = evidence[row_id]
        r2_lines.append(
            f"| #{row_id} | `{cfg['authority']}` | `{cfg['source_commit']}` | `{receipt['scope_root']}` / `{receipt['selection_mode']}` | {receipt['record_count']} | `{release['release_id']}` |"
        )
    r2_lines += [
        "",
        "## Boundary",
        "",
        "Only metadata needed for collection identity/navigation and exact source pointers are copied. Markdown bodies remain producer-owned. No document schema, publication schema, second renderer, ordering model, or multi-source union is introduced.",
        "",
        "For the Journal, membership is conservative: explicit `publish: true`, not `draft: true`, and no `private`, `templates`, or `.obsidian` path. This is a bounded KX collection rule for this release, not a redefinition of Quartz's full publication semantics.",
        "",
        "## Result",
        "",
        "The maturity distribution becomes **2×E3 + 3×E1 + 10×E0**. This is a healthier ladder than promoting mature verticals to E2/E3 merely because they already have websites.",
        "",
    ]
    (ROOT / "docs" / "R2_MULTI_LANE_E1.md").write_text("\n".join(r2_lines), encoding="utf-8")
    print("R2 promotion complete: E3=2 E1=3 E0=10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
