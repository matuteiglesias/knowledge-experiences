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

## Start here

Agents and developers should read, in order:

1. [`AGENTS.md`](AGENTS.md) — operating rules and autonomous-development protocol.
2. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — authority, boundaries, and target topology.
3. [`docs/BUILD_BUNDLE.md`](docs/BUILD_BUNDLE.md) — governed V1 → fan-out → V2 development program.
4. [`docs/EXPERIENCE_CENSUS.md`](docs/EXPERIENCE_CENSUS.md) — real experience pressure test.
5. [`docs/CROSS_REPO_HANDOFFS.md`](docs/CROSS_REPO_HANDOFFS.md) — bounded changes expected in neighboring repositories.

Run the seed integrity check before and after structural work:

```bash
make check
```

## North star

> Take any body of knowledge that matters and, with low marginal cost, turn it into the appropriate public or private experience.

The project succeeds when later experiences increasingly require configuration, selection, or curation rather than another bespoke application.
