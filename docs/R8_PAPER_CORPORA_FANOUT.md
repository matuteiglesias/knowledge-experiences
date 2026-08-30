# R8 — real Paper KB corpus fan-out

## Question

After R7, the strongest remaining source-side uncertainty was whether approved real Paper KB corpora would compose into concrete Knowledge Experiences at low marginal cost, or whether real papers would force another KX capability wave.

R8 answers that question with two governed Paper KB fixtures and three distinct experiences.

## Exact producer evidence

Pinned producer:

- repository: `matuteiglesias/paper-kb`
- commit: `e82e82deb646f30707306cd13ff8ba279c8bad50`

`tesis-cited`:

- 19 governed source PDFs represented by the fixture/source manifests;
- catalog projection: `fixture/corpora/tesis-cited/catalog/paper.catalog-record.v1.jsonl`;
- catalog SHA-256: `648d8461929629e5b13385510048f77ead7000b98318fdf87d22fe9332f28a1f`.

`eric-mv`:

- 7 governed source PDFs;
- catalog projection: `fixture/corpora/eric-mv/catalog/paper.catalog-record.v1.jsonl`;
- catalog SHA-256: `273a484b873d5ae6f9041b24e3c8b4906d23d0683b26941c95713665353f1b41`;
- consumer fixture also contains 7 canonical chunk-set artifacts.

The KX proof freezes the exact producer catalog bytes and independently compares them with the pinned Paper KB checkout.

## Three real experiences

### Thesis bibliography

- source: all 19 `tesis-cited` catalog records;
- CollectionRelease: `sha256:a766463507d2f5cc`;
- ExperienceRelease: `sha256:a6289e933594e505`;
- rendered HTML SHA-256: `9e004afd0f5fc1b410e1fee1d7f7830db7ff676b3cdc10d9003434a74f319052`.

Result: **E0 → E3**.

### Author works

The same 19-paper source is reused with the existing author facet and no new composition capability.

- selector: `author = Angus Deaton`;
- selected records: 2/19;
- exact paper IDs: `paper_340915ba55`, `paper_7eac0538e3`;
- CollectionRelease: `sha256:646d6b43072e15b4`;
- ExperienceRelease: `sha256:799a247b0ed2f161`;
- rendered HTML SHA-256: `d78670e5b9c9b72a18a8839540332d6ede710d1ada0390502db16ac88d8f618b`.

Result: **E0 → E3**.

### FCV literature corpus

- source: all 7 `eric-mv` catalog records;
- all seven records include Eric Mvukiyehe among the producer-preserved contributors;
- CollectionRelease: `sha256:010486a65a5888d2`;
- ExperienceRelease: `sha256:8a7b561e877d1c82`;
- rendered HTML SHA-256: `c933aaa087e52dd9fbc868ccfe7fcfe2990575fa3014222d2f04423798c9a82f`.

This is deliberately a **seven-paper FCV seed corpus**, not a completeness claim about the FCV literature.

Result: **E0 → E3**.

## Capability finding

**No KX capability was added in R8.**

All three experiences reuse the existing:

- `paper-catalog-jsonl` adapter;
- `all` or `facets` selection;
- producer-owned author metadata;
- deterministic Collection/Experience releases;
- `static-navigator` renderer.

This is positive evidence that marginal experience cost is falling: one new real Paper KB source surface fanned out into three semantically different experiences without modifying the KX kernel.

## Negative result: review metadata

The real `tesis-cited` `paper.review-record@1` release exists, but its records currently contain titles while substantive review fields such as abstract, date and venue are null. R8 therefore does **not** promote `thesis-rapid-paper-review` or `literature-review-snapshot` merely because the renderer could display title-only cards.

The new evidence points upstream: the next review experiment should determine whether Paper KB can preserve or enrich authoritative review metadata. This is producer-metadata pressure, not evidence for a new KX abstraction.

## Permanent proof

`scripts/prove_real_paper_corpora.py` plus `.github/workflows/r8-real-paper-corpora-proof.yml`:

1. check out the exact Paper KB commit;
2. verify producer/frozen catalog byte identity and SHA-256;
3. verify the `eric-mv` consumer fixture boundary;
4. rebuild all three experiences;
5. byte-compare CollectionRelease, ExperienceRelease and final HTML with the committed releases;
6. reassert real selection/membership semantics;
7. validate the governed census.

## R8 conclusion

R8 changes the census from:

`1×E4 + 5×E3 + 1×E1 + 9×E0`

to:

`1×E4 + 8×E3 + 1×E1 + 6×E0`.

The main scientific result is not the count itself. It is that three previously hypothetical Paper KB experiences became reproducible real-source E3 experiences with **zero new KX capability**.
