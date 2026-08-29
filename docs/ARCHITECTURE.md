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
"these 143 exact source objects, from this source identity/hash"
```

A collection release may project display metadata needed by renderers, but source semantics remain authoritative upstream.

### ExperienceSpec vs ExperienceRelease

An `ExperienceSpec` declares how humans should interact with a collection: renderer, visibility, facets, ordering, trails, and optional capabilities. An `ExperienceRelease` freezes the resolved renderer handoff and reproducibility evidence.

### Experience vs Publication

An experience may be private (research workbench, course preparation, personal literature navigator) or public (author navigator, reading trail, working-paper archive). Publication is therefore downstream/optional rather than synonymous with experience composition.

### Browse vs intelligence

Search, facets, chronology, stable links, excerpts, and provenance should work without requiring semantic retrieval or chat. Knowledge Inspect, semantic search, summaries, or chat are opt-in capabilities pulled by an experience need.

## V1 planned interface family

These names are provisional until V1 implementation and real proofs harden them:

- `knowledge.collection-spec@1`
- `knowledge.collection-release@1`
- `knowledge.experience-spec@1`
- `knowledge.experience-release@1`

Do **not** register them in `kb-contracts` merely because they cross components inside this repo. They are owned here unless a real ecosystem-wide interoperability requirement emerges.

## Reference renderer

V1 should include one deliberately boring static navigator. Its purpose is not to become a universal UI. Its purpose is to establish a cheap baseline capable of:

- text search;
- configured facets;
- sorting;
- list/card views;
- item detail/excerpt;
- stable item links;
- source/provenance link-out;
- featured items, groups, or reading trails when declared;
- responsive desktop/mobile use.

No chat, vector database, authentication platform, recommendation engine, or online backend belongs in the reference renderer by default.

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
