# V1 Composition Kernel

## Status

V1.1 establishes the smallest executable composition loop. It is intentionally a mechanics kernel, not a universal knowledge model.

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

`doctor` builds the same experience twice into independent temporary directories and fails unless the complete output file hashes and release objects match exactly.

## Local contracts

The draft producer-owned schemas in `contracts/` are:

- `knowledge.collection-spec@1`
- `knowledge.collection-release@1`
- `knowledge.experience-spec@1`
- `knowledge.experience-release@1`

They belong to this repository. Do not register them in `kb-contracts` unless a later real interoperability boundary requires shared ownership.

Runtime validation is implemented without a JSON Schema dependency. The checked-in JSON schemas are inspectable contract documents and the Python models are the executable V1 validator. Unknown fields fail closed so V2 extensions cannot silently become accidental semantics.

## Deliberately small selection semantics

V1 supports only:

- `selection.mode = all`;
- `selection.mode = ids` with an explicit ordered list of source item IDs.

The compiled release canonicalizes selected membership by `item_id` so a source's incidental line order does not alter the release.

There is intentionally no generic author query, venue query, filter DSL, graph query, semantic query, or nested collection semantics. V1.2/V1.5 must supply evidence before those abstractions are introduced.

## Reference source item projection

The JSONL adapter accepts a generic display projection with:

- required `item_id`, `kind`, `title`;
- optional subtitle, summary, date, contributors, tags, facets, canonical URL and source reference.

This is an adapter input shape, not a claim that all producers should adopt one universal domain schema. Real producer adapters may project producer-owned records into this shape at the boundary.

HTTP(S) URLs are validated before they can be emitted by the static renderer.

## Reproducibility model

Collection release identity depends on:

- canonical CollectionSpec bytes;
- exact source bytes SHA-256;
- producer authority/release identity when supplied;
- exact selected normalized items.

Experience release identity additionally depends on:

- canonical ExperienceSpec bytes;
- exact CollectionRelease file hash;
- renderer name;
- exact rendered artifact hashes.

There are no wall-clock timestamps in identity-bearing releases. Identical inputs therefore produce identical release IDs and files.

## Renderer boundary

`static-navigator` is the only V1 renderer. It produces one self-contained HTML file with:

- text search;
- configured facets;
- title/date/source sorting;
- item summaries and contributors/tags;
- stable item anchors;
- source/canonical links;
- responsive layout.

Its purpose is to make a cheap E2 experience possible. It is not the destination architecture for every collection.

## Next pressure test

The next gate is V1.2: inspect current Paper KB and prove a real producer seam. Do not extend this kernel first merely to make Paper KB fit. If author/series experiences need metadata that the current Paper KB review projection does not own, improve Paper KB with the smallest justified producer-owned catalog projection and adapt that real output here.
