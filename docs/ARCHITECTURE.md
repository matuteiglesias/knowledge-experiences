# Architecture

## Purpose

`knowledge-experiences` sits between governed knowledge producers and human-facing renderers. It owns **composition**, not knowledge truth and not UI implementation.

```text
                         KNOWLEDGE ECOSYSTEM

   governed producers                  derived capabilities
   ┌───────────────┐                   ┌──────────────────┐
   │ Paper KB      │                   │ Knowledge Inspect│
   │ doc producers │                   │ KB Artifacts     │
   │ other domains │                   └─────────┬────────┘
   └───────┬───────┘                             │
           │ producer-owned artifacts            │ optional derived inputs
           └──────────────────┬───────────────────┘
                              ▼
                    KNOWLEDGE EXPERIENCES

                  CollectionSpec (recipe)
                              ↓
                  CollectionRelease (frozen)
                              ↓
                  ExperienceSpec (recipe)
                              ↓
                  ExperienceRelease (frozen)
                              │
                 renderer-specific handoff
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
         static navigator  Abstract Scroller  vertical renderer
                                               (Thesis, etc.)
                              │
                              ▼
                    public/private experience
```

## Core distinctions

### CollectionSpec vs CollectionRelease

A `CollectionSpec` declares *how membership should be selected or curated*. A `CollectionRelease` records the exact materialized membership and source provenance at one point in time.

Example:

```text
CollectionSpec
"all works by author X"
        ↓ compile against exact producer release
CollectionRelease
"these exact source objects, from this source identity/hash"
```

A collection release may project display metadata needed by renderers, but source semantics remain authoritative upstream.

V1.1 intentionally does **not** implement the example's author selector yet. Its executable selection semantics are only `all` and explicit item IDs; V1.2 must discover author/series requirements from a real Paper KB seam rather than pre-designing a query language.

### ExperienceSpec vs ExperienceRelease

An `ExperienceSpec` declares how humans should interact with a collection: renderer, visibility, configured facets and basic navigation. An `ExperienceRelease` freezes the resolved renderer handoff and reproducibility evidence.

### Experience vs Publication

An experience may be private (research workbench, course preparation, personal literature navigator) or public (author navigator, reading trail, working-paper archive). Publication is therefore downstream/optional rather than synonymous with experience composition.

### Browse vs intelligence

Search, facets, chronology, stable links, excerpts, and provenance should work without requiring semantic retrieval or chat. Knowledge Inspect, semantic search, summaries, or chat are opt-in capabilities pulled by an experience need.

## V1 local interface family

V1.1 implements these local, repository-owned interfaces:

- `knowledge.collection-spec@1`
- `knowledge.collection-release@1`
- `knowledge.experience-spec@1`
- `knowledge.experience-release@1`

They remain draft/local until real producer/renderer proofs demonstrate what should harden. Do **not** register them in `kb-contracts` merely because they cross components inside this repo. Shared ownership requires a real ecosystem-wide interoperability need.

Frozen releases have no wall-clock timestamp in their identity-bearing payload. Release IDs derive from canonical content, source/spec hashes, exact selected membership and rendered artifact hashes. `kx doctor` proves repeat builds are content-stable.

## Adapter boundaries

V1.1 has deliberately tiny adapter registries, not a generalized plugin framework.

- Source side: `jsonl` is a reference adapter over a generic display projection. Real producer semantics stay upstream and may be projected at the boundary.
- Renderer side: `static-navigator` is the reference renderer. Abstract Scroller and vertical products remain external authorities until proven handoffs are added.

## Reference renderer

The boring static navigator establishes a cheap E2 baseline with:

- text search;
- configured facets;
- title/date/source sorting;
- item summaries and contributors/tags;
- stable item anchors;
- source/provenance link-out;
- responsive desktop/mobile use.

It produces one self-contained HTML artifact. No chat, vector database, authentication platform, recommendation engine, framework runtime, or online backend belongs in the reference renderer by default.

## Architectural invariants

1. Producer semantics remain producer-owned.
2. Frozen projections carry provenance and can be regenerated.
3. Renderer internals remain renderer-owned.
4. Configuration is preferred over code when the capability already exists.
5. A new reusable capability is justified by repeated demand, not aesthetic completeness.
6. A bespoke vertical application is the final escalation, not the starting point.
7. Cross-repo edges are considered proven only with evidence.
8. Missing or rejected edges are valid architectural outcomes.
9. Human editorial judgment is outside the automated composition authority.
10. V2 is evidence-pulled from real experience failures.
