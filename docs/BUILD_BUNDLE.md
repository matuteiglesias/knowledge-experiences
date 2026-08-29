# Governed Build Bundle

## Mission

Turn the seed architecture into a real composition capability by forcing it through heterogeneous experiences.

```text
SEED → V1 KERNEL → REAL PROOFS → PARALLEL FAN-OUT → EXPERIENCE CENSUS → V2
```

The repository should mature by **use pressure**, not speculative platform design.

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

Pinned Paper KB → Knowledge Experiences → Abstract Scroller handoff. Producer review bytes pass intact, renderer commit is verified, `paper_uid` survives to snapshot `doc_id`, and `kx doctor` proves deterministic external rendering. Selected review subsets remain intentionally unsupported downstream.

## Wave V1.4 — Ecosystem fan-out

**Status:** implemented in this tranche; accept only after repository CI and LCD pinned proof are green.

Lane A adds the first non-paper consumer seam by reusing the existing LCD run-scoped `title_slug_index.json`; no new producer contract or mixed-source core abstraction is required.

Lane B classifies Thesis and Journal as mature vertical experiences to adopt rather than replatform. Thesis owns curated research/status semantics; Journal owns publication filtering and working-memory garden semantics.

Lane C records Knowledge Inspect as an optional non-edge for this wave because no selected experience requires intelligence on the critical path.

Lane D records KB Artifacts as an optional non-edge for this wave because no selected experience yet requires governed evidence-selection receipts.

See `docs/V1_4_FANOUT.md`.

## Wave V1.5 — Experience census pressure test

**Status:** next gate after V1.4 merge.

Attempt all cases in `docs/EXPERIENCE_CENSUS.md` and record maturity honestly: source/release, collection release, renderer, maturity E0–E4, new code/contracts/adapters, reused capabilities, friction and V2 lesson.

Success is not fifteen deployed apps. Success is evidence that heterogeneous experiences increasingly require selection/configuration/curation rather than bespoke applications.

## Wave V2 — Evidence-pulled reconciliation

Do not design V2 before census evidence exists. Classify friction as configuration, source projection, adapter, renderer capability, composition-model, or genuinely vertical product need. Expand core semantics only for repeated patterns or unavoidable invariants.

## Wave W5b — Editorial/publication frontier

**Status:** parked.

`InspectionObservation → InsightCandidate → Claim → EditorialArtifact → Publication → Response` remains outside this repo's composition authority until repeated real publication workflows demand it.

## Stop rule

Stop a wave when evidence is sufficient to unlock the next real experience. The program fails if domain truth or renderer internals migrate here, optional AI becomes mandatory, or each experience still needs bespoke application code. It succeeds when later experiences increasingly become **selection + configuration + bounded curation**.
