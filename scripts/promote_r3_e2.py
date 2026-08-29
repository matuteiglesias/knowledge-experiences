#!/usr/bin/env python3
"""Promote two distinct frozen human snapshots from E1 to E2."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONFIG = {
    11: {
        "dir": "economics-of-aggregation-programme",
        "experience_file": "snapshot.experience.json",
        "title": "Economics of Aggregation — frozen research-programme index",
        "value": "portable immutable index of the exact 89-document research-programme state, distinct from the live Docusaurus portal",
        "next": "use or circulate the frozen snapshot; E3 requires a persistent executable source-to-snapshot seam or repeated real operational use, not merely this checked-in build",
    },
    12: {
        "dir": "working-memory-journal",
        "experience_file": "snapshot.experience.json",
        "title": "Working-memory journal — frozen explicit-publication inventory",
        "value": "auditable immutable inventory of the exact 2,868-note explicit-publication subset, distinct from Quartz's live semantic garden",
        "next": "use the inventory for publication/synthesis audit or circulation; compare with the live Quartz output before any E3 claim",
    },
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    evidence = {}
    for row_id, cfg in CONFIG.items():
        base = ROOT / "experiences" / "real" / cfg["dir"]
        e_release = load(base / "release" / "experience.release.json")
        c_release = load(base / "release" / "collection.release.json")
        proof = load(base / "e2-proof.json")
        if proof.get("result") != "pass":
            raise SystemExit(f"row {row_id}: E2 proof not passing")
        if proof.get("collection_release_id") != c_release.get("release_id"):
            raise SystemExit(f"row {row_id}: collection proof mismatch")
        if proof.get("experience_release_id") != e_release.get("release_id"):
            raise SystemExit(f"row {row_id}: experience proof mismatch")
        if proof.get("rendered_artifact") != "release/site/index.html":
            raise SystemExit(f"row {row_id}: unexpected rendered artifact")
        evidence[row_id] = (c_release, e_release, proof)

    census_path = ROOT / "docs" / "experience-census.v1.json"
    census = load(census_path)
    rows = {row["id"]: row for row in census["experiences"]}
    for row_id, cfg in CONFIG.items():
        c_release, e_release, proof = evidence[row_id]
        row = rows[row_id]
        if row["composition_maturity"] != "E1":
            raise SystemExit(f"row {row_id}: expected E1 parent state")
        row.update(
            {
                "composition_maturity": "E2",
                "renderer_profile": "static-navigator-frozen-snapshot",
                "rendered_artifact": f"experiences/real/{cfg['dir']}/release/site/index.html",
                "capabilities_reused": list(dict.fromkeys(row["capabilities_reused"] + ["static-navigator", "immutable-human-snapshot"])),
                "incremental_work": "experience configuration only over the accepted E1 CollectionRelease; existing static-navigator renderer reused unchanged",
                "blocker": "none for the frozen E2 artifact; the upstream live vertical remains authoritative for current content and richer semantics",
                "observed_friction": "none in rendering; the key discipline is keeping frozen snapshot semantics distinct from the live upstream vertical",
                "engineering_evidence": row["engineering_evidence"] + [
                    f"R3 deterministic build produced ExperienceRelease {e_release['release_id']} and human artifact sha256 {proof['rendered_artifact_sha256']}"
                ],
                "evidence_boundary": f"E2 claims only {cfg['value']}; no live-site replacement, deployment, cross-repo executable proof, or E3 operational claim is made",
                "next_real_action": cfg["next"],
            }
        )

    census["as_of"] = "2026-08-29"
    census_path.write_text(json.dumps(census, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = Counter(row["composition_maturity"] for row in census["experiences"])
    expected = Counter({"E0": 10, "E1": 1, "E2": 2, "E3": 2})
    if counts != expected:
        raise SystemExit(f"unexpected maturity distribution after R3: {counts}")

    human = [
        "# Experience Census — populated real-use ladder",
        "",
        "The machine-readable authority is `docs/experience-census.v1.json`. `E0`–`E4` remains strict: each rung is earned by the evidence it names.",
        "",
        "## Current frontier",
        "",
        "**2 experiences are E3, 2 are E2, 1 is E1, and 10 remain E0.** R3 converts two accepted real-source collections into distinct frozen human snapshots while leaving their upstream live products authoritative.",
        "",
        "| # | Experience | Maturity | Engineering status | Current evidence |",
        "|---|---|---|---|---|",
    ]
    for row in census["experiences"]:
        evidence_text = "declared / prior engineering evidence"
        if row["id"] in evidence:
            _, e_release, proof = evidence[row["id"]]
            evidence_text = f"frozen static snapshot → `{e_release['release_id']}` / `{proof['rendered_artifact_sha256'][:16]}…`"
        elif row["id"] == 13:
            evidence_text = "32 exact-Git metadata records → reproducible E1 CollectionRelease"
        elif row["id"] in {8, 9}:
            evidence_text = "trusted live LCD source → rendered real-source experience + executable proof"
        human.append(f"| {row['id']} | {row['name']} | **{row['composition_maturity']}** | {row['engineering_status']} | {evidence_text} |")
    human += [
        "",
        "## Why these are E2 and not duplicate products",
        "",
        "The thesis snapshot is a portable point-in-time inventory of one exact research-programme release. The Journal snapshot is an auditable point-in-time inventory of only the conservative explicit-publication subset. Neither tries to recreate Docusaurus/Quartz semantics, backlinks, editorial flow, or live-current authority.",
        "",
        "Knowledge-ecosystem technical docs remains E1. Its existing Docusaurus control surface already solves the primary human experience, and R3 found no distinct second consumer worth rendering merely to populate a rung.",
        "",
        "Paper KB remains E0 for concrete experiences until an approved real corpus is selected. Production code plus fixtures is still not real-source maturity.",
        "",
        "## Next frontier",
        "",
        "The ladder now has real occupancy at E1, E2 and E3. The highest-information next move is no longer another generic static snapshot: it is either a real Paper KB scientific corpus, or genuine use of one E2 snapshot that creates evidence for a persistent E3 seam / eventual E4 operation.",
        "",
    ]
    (ROOT / "docs" / "EXPERIENCE_CENSUS.md").write_text("\n".join(human), encoding="utf-8")

    system_path = ROOT / "SYSTEM.yaml"
    system = system_path.read_text(encoding="utf-8")
    system = re.sub(
        r"  maturity_snapshot:\n(?:    E\d: \d+\n)+",
        "  maturity_snapshot:\n    E3: 2\n    E2: 2\n    E1: 1\n    E0: 10\n",
        system,
    )
    system = re.sub(
        r"  phase: .*\n  next_gate: .*\n",
        "  phase: populated-real-use-ladder\n  next_gate: paper-real-corpus-or-operational-use\n",
        system,
    )
    system_path.write_text(system, encoding="utf-8")

    r3 = [
        "# R3 — two frozen E2 snapshots",
        "",
        "R3 starts from the accepted R2 E1 releases and adds no source adapter, domain schema, renderer, or selection semantics. It only configures and deterministically builds two distinct human-facing immutable snapshots with the existing `static-navigator`.",
        "",
        "| Census | Snapshot | CollectionRelease | ExperienceRelease | Artifact SHA-256 |",
        "|---|---|---|---|---|",
    ]
    for row_id in (11, 12):
        cfg = CONFIG[row_id]
        c_release, e_release, proof = evidence[row_id]
        r3.append(
            f"| #{row_id} | {cfg['title']} | `{c_release['release_id']}` | `{e_release['release_id']}` | `{proof['rendered_artifact_sha256']}` |"
        )
    r3 += [
        "",
        "## Boundary",
        "",
        "These artifacts are frozen derivative views. `repo.thesis` and `repo.journal` retain live content, editorial, status, link-graph and publication authority. E2 does not imply deployment or cross-repo executable proof.",
        "",
        "## Result",
        "",
        "The maturity ladder becomes **2×E3 + 2×E2 + 1×E1 + 10×E0**. The intentionally unrendered E1 technical-docs lane demonstrates that maturity is value-driven rather than score-driven.",
        "",
    ]
    (ROOT / "docs" / "R3_TWO_E2_SNAPSHOTS.md").write_text("\n".join(r3), encoding="utf-8")
    print("R3 promotion complete: E3=2 E2=2 E1=1 E0=10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
