# V1 Composition Kernel

## Status

V1.1 established the smallest executable composition loop. V1.2 has now supplied the first real producer pressure and one deliberately small model expansion.

```text
CollectionSpec
   ↓ resolve exact source + selection
CollectionRelease
   ↓ bind ExperienceSpec
renderer adapter
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

The repository-owned V1 schemas are:

- `knowledge.collection-spec@1`
- `knowledge.collection-release@1`
- `knowledge.experience-spec@1`
- `knowledge.experience-release@1`

They belong here. Do not register them in `kb-contracts` unless a later ecosystem-wide interoperability boundary requires shared ownership.

Runtime validation remains dependency-light and fail-closed for unknown fields.

## Selection semantics

V1.1 began with only:

- `selection.mode = all`;
- `selection.mode = ids`.

V1.2 added the first evidence-pulled expansion:

- `selection.mode = facets` with a non-empty mapping of exact facet values.

Facet matching is deliberately boring: scalar facets require equality; array facets match when they contain the requested scalar; all configured facet predicates must match. Zero matches fail closed so typos do not silently publish empty collections.

This is not a general query DSL. There are still no arbitrary field expressions, graph queries, semantic queries, regex conditions or nested collection semantics.

## Source adapter boundary

The generic `jsonl` adapter accepts the local display projection.

The `paper-catalog-jsonl` adapter consumes the compatibility surface it actually needs from producer-owned `paper.catalog-record@1`:

- validates schema id/version and required paper identity/title/authors;
- maps `paper_uid` to item identity;
- maps authors to contributors and the `author` facet;
- carries year/venue into facets only when the producer supplied them;
- carries abstract/date/tags/source URL when present;
- records `repo.paper-kb` as source authority.

The adapter does **not** vendor Paper KB's JSON Schema and does not infer missing authors, venue or series metadata.

## Paper KB executable proof

`.github/workflows/paper-kb-catalog-proof.yml` pins Paper KB commit:

```text
ecf09f19c3211de85eea6e4f81a0c2a48f378fc0
```

The workflow uses the real Paper KB chunk-set writer and catalog projection to create sanitized canonical records, then builds:

1. a full catalog navigator with author/year/venue facets;
2. an author-specific navigator from the same source release using only declarative facet selection.

This is an executable producer/consumer proof. It is not a claim that a real rights-sensitive corpus was published or deployed.

## Reproducibility model

Collection release identity depends on canonical spec bytes, exact source bytes SHA-256, producer authority/release identity, and exact normalized selected items.

Experience release identity additionally depends on canonical ExperienceSpec bytes, the exact CollectionRelease file hash, renderer identity and exact rendered artifact hashes.

There are no wall-clock timestamps in identity-bearing releases.

## Renderer boundary

`static-navigator` remains the only internal V1 renderer. Search, configured facets, simple sorting, summaries, stable anchors and provenance links are available without a backend, vector store or chat runtime.

## Next pressure test

V1.3 should prove a second renderer using Abstract Scroller's existing immutable snapshot compiler/reader boundary. Preserve Scroller ownership: Knowledge Experiences should prepare and invoke a renderer handoff, not duplicate its snapshot implementation or copy Paper KB review schemas.
