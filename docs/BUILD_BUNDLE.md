# Governed Build Bundle

## Mission

Turn the seed architecture into a real composition capability by forcing it through heterogeneous experiences.

```text
SEED → V1 KERNEL → REAL PROOFS → PARALLEL FAN-OUT → EXPERIENCE CENSUS → REAL USE → SELECTIVE V2
```

## Wave S0 — Seed constitution

**Status:** accepted and merged on 2026-08-29.

## Wave V1.1 — Composition kernel

**Status:** accepted and merged on 2026-08-29.

Deterministic collection/experience kernel, local contracts, CLI, reference static renderer, tests and CI.

## Wave V1.2 — First producer: Paper KB catalog seam

**Status:** accepted and merged on 2026-08-29.

Producer-owned Paper KB catalog seam, author facet selection and pinned producer/composer proof. Sanitized proof artifacts do not imply real-corpus maturity.

## Wave V1.3 — Second renderer: Abstract Scroller handoff

**Status:** accepted and merged on 2026-08-29.

Pinned Paper KB → Knowledge Experiences → Abstract Scroller handoff. Producer review bytes pass intact, renderer commit is verified, `paper_uid` survives to snapshot `doc_id`, and external rendering is deterministic.

## Wave V1.4 — Ecosystem fan-out

**Status:** accepted and merged on 2026-08-29.

LCD supplied the first non-paper bounded adapter without a new core abstraction. Thesis and Journal were classified as vertical exceptions. Knowledge Inspect and KB Artifacts remained deliberate optional non-edges for this wave.

## Wave V1.5 — Experience census pressure test

**Status:** complete in this tranche; accept only when `scripts/check_census.py`, repository tests and all prior integration proofs remain green.

The fifteen-case authority is `docs/experience-census.v1.json`, summarized in `docs/EXPERIENCE_CENSUS.md` and interpreted in `docs/V1_5_CENSUS_FINDINGS.md`.

Key governance decision: E0–E4 remains real-source composition maturity. Sanitized proofs and mature pre-existing verticals are separately visible through `engineering_status`; they do not inflate the maturity score.

Census result at 2026-08-29: all fifteen concrete experiences remain E0 under the strict rule, while five have reusable/proven mechanics and three are mature vertical surfaces. The gap is now mostly real-source adoption rather than missing architecture.

Repeated V2 candidates:

- `ordered-groups-and-reading-trails` — pressure from economic-complexity path + course readings, with Thesis as vertical evidence;
- `multi-source-collections-and-curation-receipts` — pressure from personal publications + policy/research dossier.

## Post-V1 operating regime

**Default next gate: real use before V2.**

Materialize approved real-source experiences with the existing kernel, observe friction, then evolve selectively. Priority evidence is one real Paper KB experience and one verified live LCD experience because both should require little or no new platform code.

## Wave V2 — Evidence-pulled reconciliation

**Status:** eligible for evidence review, deliberately not started.

Do not build a broad V2 from the census table alone. Pull one candidate only when a real use makes its repeated friction concrete. Do not add an orchestrator, database, auth platform, vector store, chat requirement, universal domain object model or publication engine by default.

## Wave W5b — Editorial/publication frontier

**Status:** parked.

`InspectionObservation → InsightCandidate → Claim → EditorialArtifact → Publication → Response` remains outside this repo's composition authority until repeated real publication workflows demand it.

## Stop rule

V1 succeeds if real use can now start cheaply and architecture stays legible. Architecture work should stop when the next useful action is to supply real governed material rather than another abstraction. That is the current state.
