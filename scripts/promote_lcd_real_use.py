#!/usr/bin/env python3
"""Promote the first real LCD experiences from checked-in proof artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTITUTIONAL = ROOT / "experiences/real/lcd-institutional"
THESIS = ROOT / "experiences/real/lcd-thesis-resources"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    receipt = load(INSTITUTIONAL / "source/producer-receipt.json")
    p8 = load(INSTITUTIONAL / "real-use-proof.json")
    p9 = load(THESIS / "real-use-proof.json")
    c8 = load(INSTITUTIONAL / "release/collection.release.json")
    e8 = load(INSTITUTIONAL / "release/experience.release.json")
    c9 = load(THESIS / "release/collection.release.json")
    e9 = load(THESIS / "release/experience.release.json")

    assert receipt["producer_run_status"] == "completed_trusted"
    assert receipt["producer_trust_level"] == "trusted"
    assert p8["result"] == p9["result"] == "pass"
    assert p8["producer_run_id"] == p9["producer_run_id"] == receipt["producer_run_id"]
    assert p8["collection_release_id"] == c8["release_id"]
    assert p8["experience_release_id"] == e8["release_id"]
    assert p9["collection_release_id"] == c9["release_id"]
    assert p9["experience_release_id"] == e9["release_id"]
    assert p9["parent_real_source_proof_run_id"] == p8["github_run_id"]
    exact = f"run:{receipt['producer_run_id']};git:{receipt['producer_git_commit']}"

    census_path = ROOT / "docs/experience-census.v1.json"
    census = load(census_path)
    rows = {row["id"]: row for row in census["experiences"]}

    rows[8].update(
        {
            "composition_maturity": "E3",
            "engineering_status": "proven_live",
            "code_pins": {
                "repo.lcd-uba-knowledgebase": receipt["producer_git_commit"],
                "repo.knowledge-experiences": p8["knowledge_experiences_commit"],
            },
            "exact_source_release": exact,
            "collection_release": f"experiences/real/lcd-institutional/release/collection.release.json#{c8['release_id']}",
            "rendered_artifact": "experiences/real/lcd-institutional/release/site/index.html",
            "cross_repo_proof": f"experiences/real/lcd-institutional/real-use-proof.json (GitHub Actions run {p8['github_run_id']})",
            "capabilities_reused": ["lcd-title-slug-index", "static-navigator", "deterministic-releases"],
            "incremental_work": "no new composition capability; real producer run plus the existing V1 adapter/renderer recipe",
            "blocker": "none for the page-scoped institutional experience; the public WordPress posts endpoint returned HTTP 500 during bootstrap probes and is explicitly outside this release",
            "observed_friction": "live use exposed an unhealthy posts endpoint; scope was narrowed to the coherent complete public page collection without weakening provenance or validation",
            "engineering_evidence": [
                f"live LCD producer run {receipt['producer_run_id']} completed_trusted over {receipt['page_records_fetched']} public pages",
                f"Knowledge Experiences build and real-use proof passed in GitHub Actions run {p8['github_run_id']}",
            ],
            "evidence_boundary": "E3 applies to the complete public WordPress page collection captured by this exact trusted run; posts are not claimed",
            "next_real_action": "review/use the frozen navigator and refresh only through another explicit trusted producer run when desired",
        }
    )

    rows[9].update(
        {
            "composition_maturity": "E3",
            "engineering_status": "proven_live",
            "code_pins": {
                "repo.lcd-uba-knowledgebase": receipt["producer_git_commit"],
                "repo.knowledge-experiences": p9["knowledge_experiences_commit"],
            },
            "exact_source_release": exact,
            "collection_release": f"experiences/real/lcd-thesis-resources/release/collection.release.json#{c9['release_id']}",
            "rendered_artifact": "experiences/real/lcd-thesis-resources/release/site/index.html",
            "cross_repo_proof": f"experiences/real/lcd-thesis-resources/real-use-proof.json (GitHub Actions run {p9['github_run_id']}; parent source proof run {p8['github_run_id']})",
            "capabilities_reused": ["lcd-title-slug-index", "ids-selection", "static-navigator", "deterministic-releases"],
            "incremental_work": "configuration/curation only: four exact IDs over the already frozen real source release",
            "blocker": "none for the current four-page curated subset; membership remains explicit human curation rather than an inferred thesis taxonomy",
            "observed_friction": "none in the composition model; exact-ID curation was sufficient and avoided inventing producer taxonomy",
            "v2_candidate": None,
            "engineering_evidence": [
                f"same trusted live source release reused from institutional experience run {p8['github_run_id']}",
                f"four exact live IDs built deterministically in GitHub Actions run {p9['github_run_id']} with no new adapter, renderer, or kernel change",
            ],
            "evidence_boundary": "the curated collection asserts only membership of the four exact pages selected from the frozen live source; it does not create an authoritative thesis taxonomy for LCD",
            "next_real_action": "review/use this curated subset; expand membership by explicit real IDs only when editorial intent requires it",
        }
    )
    census["as_of"] = "2026-08-29"
    census_path.write_text(json.dumps(census, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    checker = ROOT / "scripts/check_census.py"
    text = checker.read_text(encoding="utf-8")
    if '"proven_live"' not in text:
        text = text.replace('ENGINEERING = {\n', 'ENGINEERING = {\n    "proven_live",\n')
        text = text.replace(
            '{"proven_sanitized", "proven_contract_check", "existing_vertical"}',
            '{"proven_live", "proven_sanitized", "proven_contract_check", "existing_vertical"}',
        )
    checker.write_text(text, encoding="utf-8")

    human = f"""# Experience Census — real-use frontier

The machine-readable authority is `docs/experience-census.v1.json`. `E0`–`E4` remains strict: a concrete experience only advances on real-source evidence.

## Current frontier

**2 experiences are now E3; 13 remain E0.** The first real-source tranche used one trusted live LCD producer run and produced two human-usable deterministic experiences.

| # | Experience | KX maturity | Engineering status | Evidence |
|---|---|---|---|---|
| 8 | LCD institutional corpus | **E3** | proven_live | {receipt['page_records_fetched']} live public pages → `{c8['release_id']}` → static navigator; proof run {p8['github_run_id']} |
| 9 | LCD thesis/resources subset | **E3** | proven_live | same source release; 4 exact curated IDs → `{c9['release_id']}`; proof run {p9['github_run_id']} |

The other 13 records remain governed in the machine ledger with their prior blockers/statuses.

## What changed

The institutional experience crossed E1, E2 and E3 in one bounded run: the pinned LCD producer fetched the complete public WordPress **page** collection, produced a `completed_trusted` run, Knowledge Experiences froze its browse index into a `CollectionRelease`, and the existing static renderer produced a usable HTML artifact. The release deliberately excludes WordPress posts because repeated live probes returned HTTP 500 from `/wp-json/wp/v2/posts`; no post coverage is claimed.

The thesis/resources experience is the stronger composability result. It reused the exact same source release and selected these four real identities: `lcd:page:1948`, `lcd:page:1951`, `lcd:page:2147`, `lcd:page:2562`. No adapter, renderer, producer projection or kernel change was needed: the marginal experience was **selection + curation + configuration**.

## Maturity semantics

- `E0` — declared.
- `E1` — reproducible `CollectionRelease` from real source material.
- `E2` — human-usable rendered real-source artifact.
- `E3` — important real-source seam has executable evidence.
- `E4` — deployed or repeatedly used by a real consumer.

Neither LCD experience is E4: checked-in artifacts and CI evidence are not the same as deployment or repeated external use.

## Next frontier

The highest-information next move is a **second real-source domain**, preferably one of the already-proven Paper KB paths (bibliography, author works, or full review snapshot) using an explicitly approved real corpus. That tests whether the low marginal-cost pattern survives outside LCD rather than overfitting further around one producer.
"""
    (ROOT / "docs/EXPERIENCE_CENSUS.md").write_text(human, encoding="utf-8")

    findings = ROOT / "docs/V1_5_CENSUS_FINDINGS.md"
    old = findings.read_text(encoding="utf-8")
    note = f"""# Real-use update — 2026-08-29

The all-E0 V1.5 snapshot has now been crossed: cases #8 and #9 reached E3 using trusted live LCD source evidence. #8 materialized {receipt['page_records_fetched']} public institutional pages; #9 reused the same source release and required configuration/curation only. This is evidence for the intended declining marginal-cost curve. The next gate remains real use in a second source domain, not broad V2 construction.

---

"""
    if not old.startswith("# Real-use update"):
        findings.write_text(note + old, encoding="utf-8")

    system = ROOT / "SYSTEM.yaml"
    s = system.read_text(encoding="utf-8")
    if "maturity_snapshot:" not in s:
        s = s.replace(
            "  count: 15\n  composition_maturity_rule: real-source-only",
            "  count: 15\n  composition_maturity_rule: real-source-only\n  maturity_snapshot:\n    E3: 2\n    E0: 13",
        )
    s = s.replace(
        "  phase: v1.5-census-complete\n  next_gate: real-use-before-v2",
        "  phase: real-use-active\n  next_gate: second-real-source-domain",
    )
    system.write_text(s, encoding="utf-8")

    r1 = f"""# R1 — first real-source Knowledge Experiences

## Source

- producer: `repo.lcd-uba-knowledgebase`
- producer Git commit: `{receipt['producer_git_commit']}`
- producer run: `{receipt['producer_run_id']}`
- status: `completed_trusted` / `trusted`
- captured scope: complete public WordPress page collection at run time
- pages: {receipt['page_records_fetched']}
- source index SHA-256: `{receipt['index_sha256']}`
- excluded: WordPress posts; live bootstrap probes returned HTTP 500 and no post coverage is claimed

Only the public browsing index is copied here; normalized bodies and chunks remain producer-owned.

## Experience #8 — institutional pages

- CollectionRelease: `{c8['release_id']}`
- ExperienceRelease: `{e8['release_id']}`
- rendered artifact: `experiences/real/lcd-institutional/release/site/index.html`
- proof: `experiences/real/lcd-institutional/real-use-proof.json`
- maturity: **E3**

## Experience #9 — thesis resources

- exact membership: `lcd:page:1948`, `lcd:page:1951`, `lcd:page:2147`, `lcd:page:2562`
- CollectionRelease: `{c9['release_id']}`
- ExperienceRelease: `{e9['release_id']}`
- rendered artifact: `experiences/real/lcd-thesis-resources/release/site/index.html`
- proof: `experiences/real/lcd-thesis-resources/real-use-proof.json`
- maturity: **E3**

This second experience required no new code path: it reused the same source adapter, exact source release, ID selector and static renderer.
"""
    (ROOT / "docs/R1_LCD_REAL_USE.md").write_text(r1, encoding="utf-8")
    print("promoted LCD experiences #8 and #9 to E3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
