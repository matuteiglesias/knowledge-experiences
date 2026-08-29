#!/usr/bin/env python3
"""Promote LCD institutional browsing to E4 after a governed second live refresh."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INST = ROOT / "experiences" / "real" / "lcd-institutional"
SUBSET = ROOT / "experiences" / "real" / "lcd-thesis-resources"
OP = INST / "operations" / "r6-governed-refresh.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    op = load(OP)
    if op.get("schema_id") != "knowledge.operational-refresh" or op.get("schema_version") != 1:
        raise SystemExit("R6 operational receipt has unexpected schema")
    if op.get("operation_kind") != "governed_refresh" or op.get("result") != "pass":
        raise SystemExit("R6 requires a passing governed_refresh operation")
    previous = op["previous"]
    current = op["current"]
    if previous["producer_run_id"] == current["producer_run_id"]:
        raise SystemExit("R6 refresh did not create a distinct producer run")
    if current.get("producer_run_status") != "completed_trusted" or current.get("producer_trust_level") != "trusted":
        raise SystemExit("R6 current producer run is not trusted")
    if op.get("downstream_validation", {}).get("lcd-thesis-resources", {}).get("result") != "pass":
        raise SystemExit("R6 requires the existing curated downstream experience to survive the refreshed source")
    if not op.get("source_diff", {}).get("comparison_performed"):
        raise SystemExit("R6 source comparison evidence is missing")

    census_path = ROOT / "docs" / "experience-census.v1.json"
    census = load(census_path)
    rows = {row["id"]: row for row in census["experiences"]}
    row8 = rows[8]
    row9 = rows[9]
    if row8["composition_maturity"] != "E3":
        raise SystemExit("R6 expects LCD institutional experience #8 at E3")
    if row9["composition_maturity"] != "E3":
        raise SystemExit("R6 expects LCD thesis/resources experience #9 to remain E3")

    current_receipt = load(INST / "source" / "producer-receipt.json")
    current_proof = load(INST / "real-use-proof.json")
    subset_proof = load(SUBSET / "real-use-proof.json")

    row8.update(
        {
            "composition_maturity": "E4",
            "engineering_status": "proven_live",
            "code_pins": {
                "repo.lcd-uba-knowledgebase": current_receipt["producer_git_commit"],
                "repo.knowledge-experiences": current_proof["knowledge_experiences_commit"],
            },
            "exact_source_release": f"run:{current_receipt['producer_run_id']};git:{current_receipt['producer_git_commit']}",
            "collection_release": f"experiences/real/lcd-institutional/release/collection.release.json#{current_proof['collection_release_id']}",
            "rendered_artifact": "experiences/real/lcd-institutional/release/site/index.html",
            "cross_repo_proof": f"experiences/real/lcd-institutional/real-use-proof.json (GitHub Actions run {current_proof['github_run_id']})",
            "operational_evidence": "experiences/real/lcd-institutional/operations/r6-governed-refresh.json",
            "incremental_work": "second explicit live-source operation reused the existing producer, LCD adapter, Collection/Experience specs and static renderer; no composition capability was added",
            "blocker": "none for governed refresh operation; deployment/audience adoption are separate future evidence and are not claimed by E4 here",
            "observed_friction": "the second live refresh tested source stability, exact ID/content drift and downstream subset survival; the operation remained bounded to public WordPress pages and preserved the posts exclusion",
            "engineering_evidence": row8["engineering_evidence"] + [
                f"R6 governed refresh moved from producer run {previous['producer_run_id']} to distinct trusted run {current['producer_run_id']}",
                f"R6 compared source identity/content drift, rebuilt CollectionRelease {current_proof['collection_release_id']} and ExperienceRelease {current_proof['experience_release_id']}, and validated the existing LCD thesis/resources consumer against the refreshed source",
            ],
            "evidence_boundary": "E4 here means the same real-source experience has completed a second explicit governed refresh cycle with source comparison, trusted producer evidence, deterministic rebuild and downstream compatibility validation; it does not claim deployment health, audience reach, or automatic refresh cadence",
            "next_real_action": "use or circulate the refreshed institutional navigator, or run a later explicit refresh when there is source/update demand; do not schedule autonomous refresh until repeated operational need justifies it",
        }
    )

    # #9 is rebuilt against the refreshed source as downstream validation, but stays E3
    # because this wave does not assert independent operational demand for the curated subset.
    row9.update(
        {
            "code_pins": {
                "repo.lcd-uba-knowledgebase": current_receipt["producer_git_commit"],
                "repo.knowledge-experiences": subset_proof["knowledge_experiences_commit"],
            },
            "exact_source_release": f"run:{current_receipt['producer_run_id']};git:{current_receipt['producer_git_commit']}",
            "collection_release": f"experiences/real/lcd-thesis-resources/release/collection.release.json#{subset_proof['collection_release_id']}",
            "rendered_artifact": "experiences/real/lcd-thesis-resources/release/site/index.html",
            "cross_repo_proof": f"experiences/real/lcd-thesis-resources/real-use-proof.json (GitHub Actions run {subset_proof['github_run_id']}; R6 downstream refresh validation)",
            "engineering_evidence": row9["engineering_evidence"] + [
                f"R6 rebuilt the same four curated IDs from refreshed trusted producer run {current_receipt['producer_run_id']} and produced ExperienceRelease {subset_proof['experience_release_id']}"
            ],
            "observed_friction": "R6 confirmed the same four exact curated IDs survive the refreshed live institutional source; this is downstream compatibility evidence, not an independent E4 use claim",
            "evidence_boundary": "the curated collection remains E3: R6 proves it still composes from the refreshed trusted parent source, but no separate operational demand/use is claimed for this subset",
            "next_real_action": "review/use this refreshed curated subset or expand membership only by explicit real IDs when editorial intent requires it",
        }
    )

    census["as_of"] = "2026-08-29"
    census_path.write_text(json.dumps(census, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    counts = Counter(row["composition_maturity"] for row in census["experiences"])
    expected = Counter({"E0": 10, "E1": 1, "E3": 4, "E4": 1})
    if counts != expected:
        raise SystemExit(f"unexpected maturity distribution after R6: {counts}")

    human = [
        "# Experience Census — operational real-use ladder",
        "",
        "The machine-readable authority is `docs/experience-census.v1.json`. The original 15-entry census is an append-only baseline; each E0–E4 rung remains evidence-gated.",
        "",
        "## Current frontier",
        "",
        "**16 governed experiences: 1 is E4, 4 are E3, 1 is E1, and 10 remain E0.** R6 creates the first E4 through a second explicit trusted live-source refresh, not through stronger CI alone.",
        "",
        "| # | Experience | Maturity | Engineering status | Current evidence |",
        "|---|---|---|---|---|",
    ]
    for row in census["experiences"]:
        evidence = "declared / prior engineering evidence"
        if row["id"] == 8:
            evidence = f"second governed live refresh → `{current_proof['experience_release_id']}` + source-diff/downstream operation receipt"
        elif row["id"] == 9:
            evidence = f"refreshed trusted parent source → same 4 exact IDs → `{subset_proof['experience_release_id']}`; remains E3"
        elif row["id"] in {11, 12, 16}:
            evidence = "exact Git producer → deterministic frozen experience + persistent proof"
        elif row["id"] == 13:
            evidence = "32 exact-Git metadata records → reproducible E1 CollectionRelease"
        human.append(f"| {row['id']} | {row['name']} | **{row['composition_maturity']}** | {row['engineering_status']} | {evidence} |")
    human += [
        "",
        "## R6 interpretation",
        "",
        f"LCD institutional browsing crossed E4 because the producer was operated again against the live public WordPress page surface, yielding a distinct trusted run `{current['producer_run_id']}` after R1 `{previous['producer_run_id']}`. KX compared record identities and content hashes, rebuilt the frozen human experience, and verified that the existing four-ID thesis/resources derivative still composes from the refreshed source.",
        "",
        "The thesis/resources subset deliberately remains E3. It was rebuilt as a downstream compatibility check, but this wave does not manufacture a second E4 claim from one parent refresh. E4 is therefore scarce and tied to explicit operational evidence.",
        "",
        "## Next frontier",
        "",
        "The strongest scientific target remains a genuinely approved real Paper KB corpus. Other E3 experiences should cross E4 only after their own real refresh, circulation or recurring workflow creates independent operational evidence.",
        "",
    ]
    (ROOT / "docs" / "EXPERIENCE_CENSUS.md").write_text("\n".join(human), encoding="utf-8")

    system_path = ROOT / "SYSTEM.yaml"
    system = system_path.read_text(encoding="utf-8")
    system = re.sub(
        r"  maturity_snapshot:\n(?:    E\d: \d+\n)+",
        "  maturity_snapshot:\n    E4: 1\n    E3: 4\n    E1: 1\n    E0: 10\n",
        system,
    )
    system = re.sub(
        r"  phase: .*\n  next_gate: .*\n",
        "  phase: first-operational-experience\n  next_gate: paper-real-corpus-or-independent-operational-use\n",
        system,
    )
    system_path.write_text(system, encoding="utf-8")

    doc = f"""# R6 — first E4 through governed LCD refresh

R6 tests the top rung without weakening it. The same real LCD institutional experience is operated a second time against the live public WordPress page surface, compared with its R1 source state, deterministically rebuilt, and used to validate the existing curated LCD thesis/resources derivative.

## Operation

```text
R1 trusted run {previous['producer_run_id']}
        ↓
second explicit live fetch
        ↓
R6 trusted run {current['producer_run_id']}
        ↓
identity + content-hash comparison
        ↓
CollectionRelease {current_proof['collection_release_id']}
        ↓
ExperienceRelease {current_proof['experience_release_id']}
        ↓
refreshed institutional navigator
        ↓
rebuild existing 4-ID thesis/resources derivative
```

Operational evidence: `experiences/real/lcd-institutional/operations/r6-governed-refresh.json`.

## Source comparison

- previous records: {previous['records']}
- refreshed records: {current['records']}
- added IDs: {len(op['source_diff']['added_source_ids'])}
- removed IDs: {len(op['source_diff']['removed_source_ids'])}
- content-hash changes on persistent IDs: {len(op['source_diff']['content_changed_source_ids'])}
- exact source index changed: {str(previous['index_sha256'] != current['index_sha256']).lower()}

The operation accepts either a stable or changed live source; what matters is that differences are measured and the trusted downstream experience is rebuilt from the exact refreshed state.

## Why E4

This is not another proof of a frozen seam. It is a second explicit production-like operation of the same real-source experience: fetch current source, validate/promote a trusted producer run, compare against the prior accepted state, issue a new deterministic human experience release, and verify an existing downstream derivative. That is operational refresh evidence.

The E4 claim is intentionally narrow. It does **not** claim public deployment health, audience reach, automatic scheduling or continuous synchronization. Those remain separate future evidence.

## Deliberate non-promotion

Experience #9 was rebuilt from the refreshed source and validated successfully, but remains E3 because this wave does not demonstrate independent operational demand for that curated subset.

## Result

The ladder becomes **1×E4 + 4×E3 + 1×E1 + 10×E0**.
"""
    (ROOT / "docs" / "R6_LCD_OPERATIONAL_REFRESH.md").write_text(doc, encoding="utf-8")

    bundle_path = ROOT / "docs" / "BUILD_BUNDLE.md"
    bundle = bundle_path.read_text(encoding="utf-8")
    marker = "- **R5 — teaching discovery:**"
    if "- **R6 — first operational refresh:**" not in bundle:
        pos = bundle.find(marker)
        if pos < 0:
            raise SystemExit("BUILD_BUNDLE missing R5 marker")
        end = bundle.find("\n", pos)
        bundle = bundle[: end + 1] + "- **R6 — first operational refresh:** LCD institutional browsing completed a second trusted live-source refresh, source-diff comparison, deterministic rebuild and downstream subset validation; #8 therefore becomes the first narrowly scoped E4.\n" + bundle[end + 1 :]
    bundle = re.sub(
        r"After R5 the live census has \*\*16 governed experiences: 5×E3 \+ 1×E1 \+ 10×E0\*\*\.",
        "After R6 the live census has **16 governed experiences: 1×E4 + 4×E3 + 1×E1 + 10×E0**.",
        bundle,
    )
    bundle_path.write_text(bundle, encoding="utf-8")

    print(f"R6 promotion complete: #8 E4 via {current['producer_run_id']}; #9 remains E3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
