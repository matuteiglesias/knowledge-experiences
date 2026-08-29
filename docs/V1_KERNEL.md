# V1 Composition Kernel

## Status

V1.1 established the deterministic composition loop. V1.2 added the first producer-backed selection pressure. V1.3 adds a second renderer without moving renderer or paper semantics into this repository.

```text
CollectionSpec
   ↓ resolve exact source + selection
CollectionRelease
   ↓ bind ExperienceSpec
renderer handoff
   ↓
ExperienceRelease + human-facing artifact
```

## Operator surface

After `python3 -m pip install --no-deps -e .`:

```bash
kx validate examples/fixture/demo.collection.json
kx compile-collection examples/fixture/demo.collection.json --out /tmp/collection.release.json
kx build examples/fixture/demo.experience.json --out /tmp/kx-demo
kx doctor examples/fixture/demo.experience.json
```

`doctor` builds the same experience twice into independent temporary directories and fails unless complete output file hashes and release objects match exactly.

## Local contracts

The repository-owned V1 schemas remain:

- `knowledge.collection-spec@1`
- `knowledge.collection-release@1`
- `knowledge.experience-spec@1`
- `knowledge.experience-release@1`

V1.3 adds optional `renderer_ref` to ExperienceSpec so an external renderer can be pinned without creating a shared ecosystem contract.

## Selection semantics

Supported selection remains deliberately small:

- `selection.mode = all`;
- `selection.mode = ids`;
- `selection.mode = facets` with exact scalar equality / array containment.

Zero facet matches fail closed. This is not a general query language.

## Source adapter boundary

Current adapters are:

- `jsonl` — local generic display projection;
- `paper-catalog-jsonl` — producer-owned `paper.catalog-record@1` consumer surface;
- `paper-review-jsonl` — producer-owned `paper.review-record@1` consumer surface.

The two Paper KB adapters do not vendor Paper KB JSON schemas and do not infer missing domain metadata.

## Paper KB catalog proof

The pinned V1.2 proof uses Paper KB `ecf09f19c3211de85eea6e4f81a0c2a48f378fc0` to build a full catalog and an author subset from the same source release. It demonstrated the first falling marginal cost: the second experience is selection/configuration, not another application.

## External renderer boundary

`static-navigator` is internal and dependency-free.

`abstract-scroller` is an external renderer handoff. Knowledge Experiences verifies the exact checkout commit and invokes Scroller's own snapshot compiler. For this renderer the original producer-owned review JSONL is passed intact after SHA verification; generic collection items are not transformed back into `paper.review-record@1`.

V1.3 deliberately rejects selected subsets for Abstract Scroller. That missing capability is evidence for later design, not permission to move paper-domain projection semantics downstream.

See `docs/V1_3_ABSTRACT_SCROLLER_HANDOFF.md`.

## Reproducibility model

Collection release identity depends on canonical spec bytes, exact source bytes SHA-256, producer authority/release identity, and exact normalized selected items.

Experience release identity additionally depends on canonical ExperienceSpec bytes, exact CollectionRelease file hash, renderer identity/ref and exact rendered artifact hashes.

There are no wall-clock timestamps in identity-bearing releases.

## Next pressure test

After V1.3 is accepted, V1.4 should fan out selectively: first a non-paper producer and then mature vertical experiences. Do not broaden the kernel before those cases expose repeated friction.
