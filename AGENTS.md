# AGENTS.md

## Mission

Develop `knowledge-experiences` as a thin composition authority that makes governed knowledge reusable across many public and private human experiences.

The north star is:

> take any body of knowledge that matters and, with low marginal cost, turn it into the appropriate public or private experience.

## Before changing code

1. Read `SYSTEM.yaml`.
2. Read `docs/ARCHITECTURE.md`.
3. Read `docs/BUILD_BUNDLE.md` and identify the earliest unfinished gate.
4. Read `docs/EXPERIENCE_CENSUS.md` and select a real experience that exercises that gate.
5. Read `docs/CROSS_REPO_HANDOFFS.md` before proposing changes outside this repository.
6. Run `make check`.

Do not start by designing a universal platform. Start from the earliest real experience that is not yet reproducibly materializable.

## Autonomous development protocol

For each bounded development wave:

1. **Reconstruct current truth.** Inspect current `main`, relevant producer/renderer authority, and existing executable seams. Never trust a historical diagram over current code.
2. **Choose one pressure test.** Name the exact experience and target maturity level (`E0`–`E4`) before implementation.
3. **Prefer reuse.** Configuration first; bounded adapter second; reusable capability third; bespoke application last.
4. **Keep semantics with producers.** If an experience needs richer paper/document metadata, ask the producer for a producer-owned projection rather than expanding a generic collection schema into a domain schema.
5. **Freeze releases, not truths.** `CollectionRelease` and `ExperienceRelease` are reproducible projections with provenance, never alternate authorities for source objects.
6. **Prove real seams.** Cross-repo claims require executable evidence using real producer output and real consumer/renderer behavior where practical.
7. **Record friction.** Every workaround or repeated missing field belongs in the V2 evidence ledger. Do not generalize from one case unless the abstraction is already obvious and low-risk.
8. **Run checks and inspect generated output.** A successful command is not sufficient when the wave claims a human experience.
9. **Update the build bundle.** Mark only demonstrated gates as accepted.
10. **Stop at the boundary.** Do not refactor neighboring repos merely for symmetry or architectural neatness.

## Cross-repository safety

- Work in separate branches and narrow PRs.
- Never copy producer-owned schemas here to simplify consumption.
- Never make `kb-contracts` a warehouse for domain schemas.
- Never force `knowledge-inspect ↔ kb-artifacts` integration unless a real workflow requires it.
- Never turn Abstract Scroller into a corpus authority.
- Never turn Thesis or Journal into universal renderers merely because they are useful exemplars.
- Never introduce credentials, broad write permissions, or online services merely to satisfy a proof that can be performed producer-side or with immutable artifacts.
- Preserve existing vertical products when a thin adapter can compose them.

If authorization for a consequential cross-repo change is unclear, leave a reviewable branch/PR or decision packet rather than silently broadening scope.

## Definition of done for a capability

A capability is not done because a schema or abstraction exists. It is done when at least one real experience uses it and the evidence is inspectable.

Use the maturity ladder:

- `E0` — declared: real intended sources/renderers identified.
- `E1` — compiled: a reproducible `CollectionRelease` can be produced from real source material.
- `E2` — rendered: a human can open the generated experience and use its claimed basic interactions.
- `E3` — proven: an executable integration proof covers the important cross-repo seam.
- `E4` — operational: deployed or repeatedly used by a real consumer, with observed feedback.

Do not report `E3` or `E4` from fixtures alone.

## V2 rule

V1 is deliberately a hypothesis. V2 may change the composition model only from evidence gathered across the experience census. Prefer changes supported by multiple independent experiences or by one unavoidable architectural invariant.

The repository fails if it becomes a universal knowledge object model, a mandatory orchestration runtime, a CMS, an all-purpose RAG service, or an excuse to build custom applications before composition has been tried.
