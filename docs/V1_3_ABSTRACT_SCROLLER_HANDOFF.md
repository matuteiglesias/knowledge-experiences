# V1.3 — Abstract Scroller renderer handoff

## Decision

Knowledge Experiences may select and invoke Abstract Scroller as an external renderer, but it does not become a producer of `paper.review-record@1`.

The accepted boundary is:

```text
Paper KB
  governed chunk_set
       ↓ producer-owned projection
  paper.review-record@1 JSONL
       ↓ exact original bytes
Knowledge Experiences
  CollectionSpec + ExperienceSpec
       ↓ verified handoff
Abstract Scroller @ exact commit
       ↓
immutable snapshot
```

## Why the producer artifact passes intact

The generic collection item model is a display/composition projection. Reconstructing `paper.review-record@1` from those generic items would silently move paper-domain semantics into this repository. V1.3 therefore passes the original producer-owned review JSONL directly to the renderer after verifying that its SHA-256 is the same source frozen by the CollectionRelease.

The `paper-review-jsonl` source adapter exists so the collection can still be inspected and released through the composition model. It validates only the consumer surface required here; it does not vendor Paper KB's schema.

## Renderer pin

`ExperienceSpec.renderer_ref` records the exact renderer commit. The Abstract Scroller adapter requires:

- `renderer = abstract-scroller`;
- an exact 40-character commit SHA in `renderer_ref`;
- `KX_ABSTRACT_SCROLLER_ROOT` pointing to an Abstract Scroller checkout;
- the checkout HEAD to equal `renderer_ref`;
- the checkout `SYSTEM.yaml` to identify `repo.abstract-scroller`.

The frozen ExperienceRelease records both renderer name and ref, while `site/renderer.provenance.json` records renderer commit and producer input identity.

## Selection boundary

V1.3 supports only full-source membership for Abstract Scroller. The adapter compares the number of producer records with the frozen collection items and fails when a subset was selected.

This is intentional. A future request for a selected review subset must decide where that producer-domain projection belongs rather than reconstructing review records downstream by convenience.

## Executable proof

`.github/workflows/abstract-scroller-handoff-proof.yml` pins:

- Paper KB: `ecf09f19c3211de85eea6e4f81a0c2a48f378fc0`;
- Abstract Scroller: `6a738edd28d21bf54d6c52943883fee19f4cc033`.

CI uses real Paper KB writer/projection code over sanitized records, then `kx doctor` invokes the real pinned Scroller snapshot compiler twice. The proof checks:

- producer SHA survives CollectionRelease provenance;
- renderer SHA survives ExperienceRelease/provenance;
- Scroller manifest validation succeeds;
- final Brotli tile `doc_id` values equal original Paper KB `paper_uid` values;
- deterministic rebuilds are byte-stable.

This proves the interface mechanics and ownership boundary. It does not promote any thesis or literature-review census case above fixture-only maturity; real-corpus E2/E3 claims still require approved real source material.
