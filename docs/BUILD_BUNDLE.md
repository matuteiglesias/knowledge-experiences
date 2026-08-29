# Governed Build Bundle

## Mission

Turn the seed architecture into a real composition capability by forcing it through heterogeneous experiences. The development program is intentionally staged as:

```text
SEED → V1 KERNEL → REAL PROOFS → PARALLEL FAN-OUT → EXPERIENCE CENSUS → V2
```

The repository should mature by **use pressure**, not by speculative platform design.

## Wave S0 — Seed constitution

**Status:** accepted and merged on 2026-08-29.

Required:

- repository identity and authority in `SYSTEM.yaml`;
- agent operating protocol;
- architecture and invariants;
- experience census;
- cross-repo handoff map;
- dependency-free seed integrity check.

**DoD:** a new developer/agent can determine what the repo owns, what it must not own, which wave comes next, and how success is measured without relying on chat history.

---

## Wave V1.1 — Composition kernel

**Status:** accepted and merged on 2026-08-29 when this bundle is present on `main` with the executable kernel and green repository checks.

**Mission:** make composition executable without external service dependencies.

Implemented:

- small Python package and CLI;
- draft local schemas/models for `CollectionSpec`, `CollectionRelease`, `ExperienceSpec`, `ExperienceRelease`;
- deterministic fail-closed validation;
- source adapter interface plus JSONL reference adapter;
- renderer adapter interface plus self-contained static navigator;
- SHA-256 source/spec/artifact provenance and content-derived release IDs;
- `kx validate`, `kx compile-collection`, `kx build`, `kx doctor`;
- deterministic fixture, tests and CI.

The V1 selector remains deliberately limited to `all` or explicit item IDs. Rich filtering is deferred to real producer/census pressure.

**DoD:** the fixture compiles and renders deterministically; `kx doctor` independently rebuilds twice and requires complete file-hash equality.

**Forbidden:** database, vector store, chat, generalized plugin framework, auth platform, hosted orchestrator.

---

## Wave V1.2 — First real producer: Paper KB catalog seam

**Status:** next gate.

**Mission:** prove that a real governed paper corpus can become multiple experiences without making this repo a paper authority.

Inspect current Paper KB artifacts first. The existing `paper.review-record@1` is review-oriented and should not be expanded merely for collection browsing. If author/contributor/series facets require a richer producer projection, add the smallest justified producer-owned catalog projection in Paper KB (candidate name `paper.catalog-record@1`) and prove it against real corpus output.

Target experiences:

- thesis bibliography navigator;
- author works navigator;
- working-paper-series navigator.

**DoD:** at least one real Paper KB artifact produces an `E2` experience; producer identity survives into release provenance; author/series functionality, if claimed, comes from producer-owned metadata rather than guessed enrichment here.

---

## Wave V1.3 — Second renderer: Abstract Scroller handoff

**Mission:** prove one collection can select a renderer other than the reference navigator.

Reuse Abstract Scroller's existing immutable-snapshot boundary. Prefer an adapter/handoff that preserves Scroller ownership over snapshot compilation. Do not duplicate its reader or vendor Paper KB schemas.

Target experiences:

- thesis rapid review;
- literature-review snapshot.

**DoD:** one real collection/experience release can reproducibly hand off to the real Scroller build path and produce a usable snapshot (`E3` for the important seam if CI proof is practical).

---

## Wave V1.4 — Parallel ecosystem fan-out

Run independent bounded lanes where possible.

### Lane A — document producer

Use `lcd-UBA-knowledgebase` as the first non-paper pressure test. Reuse its trusted normalized/chunk/run artifacts. Add only the clean producer seam required for deterministic consumption.

Targets:

- LCD institutional corpus;
- LCD thesis/resources subset.

### Lane B — existing vertical experiences

Study `thesis` and `journal` as mature exemplars. Add ecosystem-awareness metadata/docs only where useful. Do not rewrite them into generic renderers. Determine which parts of their navigation/publication semantics can be represented declaratively and which properly remain vertical.

Targets:

- Economics of Aggregation research programme;
- working-memory journal.

### Lane C — optional intelligence

Only when demanded by a selected experience, explore bounded `CollectionRelease → Knowledge Inspect` scope/inspection support. Keep `observation ≠ claim`, and do not place chat on the critical path.

### Lane D — governed selection

Only when a real curated evidence workflow needs it, demonstrate how KB Artifacts selections can feed collection membership. Do not invent a mandatory Knowledge Inspect → KB Artifacts edge.

**DoD:** each lane either produces a real accepted seam or records a justified non-edge/vertical exception.

---

## Wave V1.5 — Experience census pressure test

Attempt all cases in `docs/EXPERIENCE_CENSUS.md` and record maturity honestly.

For every case record:

- source authority;
- exact collection input/release if available;
- renderer/profile;
- maturity `E0`–`E4`;
- new code introduced;
- new producer contract/projection introduced;
- new adapter introduced;
- existing capabilities reused;
- blocker/friction;
- candidate V2 lesson.

Success is **not** fifteen deployed apps. Success is evidence that many heterogeneous experiences can be represented and increasingly materialized with low marginal engineering cost.

Desired direction, not a hard quota:

- all census cases at least `E0`;
- most straightforward cases `E1`;
- several distinct families `E2`;
- 2–3 high-value real cross-repo seams `E3`;
- `E4` only where actual use/deployment exists.

---

## Wave V2 — Evidence-pulled reconciliation

Do not design V2 before V1.5 evidence exists.

Classify observed friction into:

1. configuration gap;
2. source projection gap;
3. adapter gap;
4. reusable renderer capability gap;
5. composition-model gap;
6. genuinely vertical product need.

Change the core model only for patterns repeated across independent experiences or for one unavoidable invariant. Keep an explicit V2 evidence ledger linking every model expansion to concrete census cases.

Candidate questions that must remain unanswered until evidence exists:

- whether contributors need a generic core representation;
- whether groups and reading trails are one abstraction or two;
- whether nested collections are needed;
- whether mixed-source collections require extra namespace rules;
- whether visibility belongs in experience specs or deployment policy;
- whether derived intelligence needs typed attachment slots;
- whether renderer capability negotiation needs a formal contract.

**DoD:** V2 demonstrably reduces repeated friction without turning the repository into a universal knowledge model.

---

## Wave W5b — Editorial/publication frontier

**Status:** parked and explicitly outside the critical path.

Future concepts such as `InspectionObservation → InsightCandidate → Claim → EditorialArtifact → Publication → Response` may later consume experiences/knowledge, but this repo must not automate intellectual stance or collapse experience composition into editorial publication.

Pull this frontier only after repeated real publication workflows demand an explicit boundary.

---

## Stop rule

Stop a development wave when its evidence is sufficient to unlock the next real experience. Do not continue adding abstractions because they seem generally useful.

The program fails if:

- every experience still requires bespoke application code;
- domain truth migrates into this repository;
- renderer internals migrate into this repository;
- optional AI infrastructure becomes mandatory;
- V2 is designed from taste rather than census evidence.

The program succeeds when later experiences increasingly become **selection + configuration + bounded curation**.
