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

---

## Wave V1.2 — First producer: Paper KB catalog seam

**Status:** accepted and merged on 2026-08-29.

Delivered producer-owned `paper.catalog-record@1` in Paper KB, `paper-catalog-jsonl` consumption here, exact facet selection, and a pinned cross-repository proof showing full-catalog and author-specific experiences from one producer release.

Evidence boundary remains explicit: the interface proof uses sanitized producer-generated artifacts, not a rights-sensitive real corpus. Working-paper-series support is not claimed because venue/series coverage is not guaranteed upstream.

---

## Wave V1.3 — Second renderer: Abstract Scroller handoff

**Status:** implemented in this tranche; accept only after repository CI and the pinned three-repository proof are green.

**Mission:** prove one ExperienceSpec can choose the real Abstract Scroller renderer without copying its implementation or moving Paper KB review semantics into the composition authority.

Implemented:

- `paper-review-jsonl` consumer adapter for the bounded Paper KB review surface;
- optional exact `ExperienceSpec.renderer_ref` pin;
- verified external renderer handoff through `KX_ABSTRACT_SCROLLER_ROOT`;
- source SHA check before renderer invocation;
- exact renderer Git HEAD check before invocation;
- real Scroller snapshot compiler + manifest validator invocation;
- renderer provenance captured in the frozen output;
- fail-closed rule that Abstract Scroller currently accepts only full-source membership;
- pinned CI across Paper KB → Knowledge Experiences → Abstract Scroller;
- identity assertion from Paper KB `paper_uid` to final Scroller tile `doc_id`;
- deterministic `kx doctor` over the external renderer path.

Pins used by the proof:

- Paper KB `ecf09f19c3211de85eea6e4f81a0c2a48f378fc0`;
- Abstract Scroller `6a738edd28d21bf54d6c52943883fee19f4cc033`.

**Evidence boundary:** this proves interface mechanics using real code on sanitized records. It does not by itself raise thesis rapid review or literature-review snapshot to real-corpus E2/E3 maturity.

**DoD:** accepted when the exact producer/composer/renderer chain builds reproducibly, Scroller validates the snapshot, and canonical `paper_uid` survives into final tiles.

---

## Wave V1.4 — Parallel ecosystem fan-out

**Status:** next gate after V1.3 merge.

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

---

## Wave W5b — Editorial/publication frontier

**Status:** parked.

`InspectionObservation → InsightCandidate → Claim → EditorialArtifact → Publication → Response` remains outside this repo's composition authority until repeated real publication workflows demand it.

---

## Stop rule

Stop a wave when evidence is sufficient to unlock the next real experience. The program fails if domain truth or renderer internals migrate here, optional AI becomes mandatory, or each experience still needs bespoke application code. It succeeds when later experiences increasingly become **selection + configuration + bounded curation**.
