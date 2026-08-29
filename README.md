# Knowledge Experiences

`knowledge-experiences` is the composition authority that turns governed knowledge into reproducible human experiences at low marginal cost.

Its job is deliberately narrow:

```text
governed producers
       ↓
CollectionSpec → CollectionRelease
       ↓
ExperienceSpec → ExperienceRelease
       ↓
renderer adapters
       ↓
public or private human experience
```

This repository does **not** own paper semantics, document semantics, evidence truth, deep inspection, renderer internals, or editorial claims. Those stay with their existing authorities.

## Current capability

V1.1 provides an executable, dependency-light composition kernel:

- local models and draft schemas for collection/experience specs and releases;
- deterministic JSON validation and fail-closed unknown fields;
- a source-adapter boundary with a JSONL reference adapter;
- a renderer-adapter boundary with a self-contained static navigator;
- SHA-256 source/spec/artifact provenance;
- content-derived release IDs;
- `kx validate`, `kx compile-collection`, `kx build`, and `kx doctor`;
- a deterministic fixture used only to prove mechanics.

The reference navigator intentionally remains boring: client-side search, configured facets, sorting, item cards, stable anchors, provenance links, and responsive layout. It has no database, vector store, chat runtime, auth platform, or hosted backend.

## Quickstart

For a local editable command:

```bash
python3 -m pip install --no-deps -e .
kx doctor examples/fixture/demo.experience.json
kx build examples/fixture/demo.experience.json --out dist/example
```

Or run directly from source without installation:

```bash
make check
make example
```

Then open `dist/example/site/index.html` directly in a browser. The generated page is self-contained.

## Start here

Agents and developers should read, in order:

1. [`AGENTS.md`](AGENTS.md) — operating rules and autonomous-development protocol.
2. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — authority, boundaries, and target topology.
3. [`docs/BUILD_BUNDLE.md`](docs/BUILD_BUNDLE.md) — governed V1 → fan-out → V2 development program.
4. [`docs/V1_KERNEL.md`](docs/V1_KERNEL.md) — current operator contract and deliberately limited V1 semantics.
5. [`docs/EXPERIENCE_CENSUS.md`](docs/EXPERIENCE_CENSUS.md) — real experience pressure test.
6. [`docs/CROSS_REPO_HANDOFFS.md`](docs/CROSS_REPO_HANDOFFS.md) — bounded changes expected in neighboring repositories.

## North star

> Take any body of knowledge that matters and, with low marginal cost, turn it into the appropriate public or private experience.

The project succeeds when later experiences increasingly require configuration, selection, or curation rather than another bespoke application.
