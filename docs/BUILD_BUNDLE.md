# Governed Build Bundle

## Mission

Turn the seed architecture into a real composition capability by forcing it through heterogeneous experiences.

```text
SEED → V1 KERNEL → REAL PROOFS → PARALLEL FAN-OUT → EXPERIENCE CENSUS → V2
```

The repository should mature by **use pressure**, not speculative platform design.

## Wave S0 — Seed constitution

**Status:** accepted and merged on 2026-08-29.

Established repository identity/authority, agent protocol, architecture, experience census, cross-repo handoffs and seed integrity checks.

---

## Wave V1.1 — Composition kernel

**Status:** accepted and merged on 2026-08-29.

Delivered the small Python package/CLI, local collection/experience contracts, deterministic releases, JSONL source boundary, self-contained static navigator, `kx validate/compile-collection/build/doctor`, tests and CI.

V1.1 deliberately started with `all` and explicit-ID selection only.

**DoD:** accepted; `kx doctor` independently rebuilds and requires complete file-hash equality.

**Still forbidden:** database, vector store, chat, generalized plugin framework, auth platform, hosted orchestrator.

---

## Wave V1.2 — First producer: Paper KB catalog seam

**Status:** bounded interface tranche implemented; acceptance requires this branch's cross-repository CI to be green before merge.

**Observed need:** `paper.review-record@1` is correctly review-oriented and does not expose authors. Current Paper KB TEI production already places parsed author names in governed `chunk_set.paper_meta`, so browsing should be served by a sibling producer projection rather than widening the review schema.

Implemented across the ecosystem:

- Paper KB producer-owned `paper.catalog-record@1` merged at `ecf09f19c3211de85eea6e4f81a0c2a48f378fc0`;
- Paper KB catalog projection copies only existing paper metadata and refuses inference;
- Knowledge Experiences `paper-catalog-jsonl` adapter validates only its consumer surface and maps authors/year/venue to display facets;
- first evidence-pulled core expansion: exact `selection.mode=facets`;
- pinned cross-repository workflow creates canonical sanitized producer output through real Paper KB code;
- full catalog and author-specific experience reuse the same source release and static renderer.

**Important evidence boundary:** the executable seam is real, but CI uses sanitized producer-generated artifacts. No rights-sensitive real corpus was run or published here. Therefore actual thesis/author corpus instances remain to be materialized when an approved corpus is available to the execution environment.

**Not claimed:** working-paper-series support as a real experience. `venue` can be consumed when present, but current Paper KB TEI production does not guarantee venue/series coverage.

**DoD for this tranche:** producer identity is pinned and survives release provenance; real producer code feeds real consumer code; author selection is producer-backed rather than inferred downstream; a second experience is created by configuration/selection rather than another app.

---

## Wave V1.3 — Second renderer: Abstract Scroller handoff

**Status:** next gate after V1.2 merge.

**Mission:** prove one collection can select a renderer other than the reference navigator.

Reuse Abstract Scroller's existing immutable-snapshot boundary. Prefer an adapter/handoff that preserves Scroller ownership over snapshot compilation. Do not duplicate its reader or vendor Paper KB schemas.

Target experiences:

- thesis rapid review;
- literature-review snapshot.

**DoD:** one collection/experience definition reproducibly invokes the real Scroller build path and produces a usable immutable snapshot; important cross-repo identity is preserved and pinned.

---

## Wave V1.4 — Parallel ecosystem fan-out

### Lane A — document producer
Use `lcd-UBA-knowledgebase` as the first non-paper pressure test. Reuse trusted normalized/chunk/run artifacts and add only the clean producer seam required for deterministic consumption.

### Lane B — existing vertical experiences
Study `thesis` and `journal` as mature exemplars. Add ecosystem-awareness metadata/docs only where useful. Do not rewrite them into generic renderers.

### Lane C — optional intelligence
Only when demanded by an experience, explore bounded `CollectionRelease → Knowledge Inspect` inspection. Keep `observation ≠ claim`; chat is not critical-path infrastructure.

### Lane D — governed selection
Only when a real curated evidence workflow needs it, demonstrate how KB Artifacts selections can feed collection membership. Do not invent a mandatory Knowledge Inspect → KB Artifacts edge.

**DoD:** each lane either produces a real accepted seam or records a justified non-edge/vertical exception.

---

## Wave V1.5 — Experience census pressure test

Attempt all cases in `docs/EXPERIENCE_CENSUS.md` and record maturity honestly: source/release, collection release, renderer, maturity E0–E4, new code/contracts/adapters, reused capabilities, friction and V2 lesson.

Success is not fifteen deployed apps. Success is evidence that heterogeneous experiences increasingly require selection/configuration/curation rather than bespoke applications.

---

## Wave V2 — Evidence-pulled reconciliation

Do not design V2 before census evidence exists. Classify friction as configuration, source projection, adapter, renderer capability, composition-model, or genuinely vertical product need. Expand core semantics only for repeated patterns or unavoidable invariants.

Open questions stay open until evidence exists: groups vs trails, nested collections, mixed-source namespace rules, visibility/deployment policy, typed derived intelligence attachments and formal renderer capability negotiation.

---

## Wave W5b — Editorial/publication frontier

**Status:** parked.

`InspectionObservation → InsightCandidate → Claim → EditorialArtifact → Publication → Response` remains outside this repo's composition authority until repeated real publication workflows demand it.

---

## Stop rule

Stop a wave when evidence is sufficient to unlock the next real experience. The program fails if domain truth or renderer internals migrate here, optional AI becomes mandatory, or each experience still needs bespoke application code. It succeeds when later experiences increasingly become **selection + configuration + bounded curation**.
