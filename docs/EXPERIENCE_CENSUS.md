# Experience Census — real-use frontier

The machine-readable authority is `docs/experience-census.v1.json`. `E0`–`E4` remains strict: a concrete experience only advances on real-source evidence.

## Current frontier

**2 experiences are now E3; 13 remain E0.** The first real-source tranche used one trusted live LCD producer run and produced two human-usable deterministic experiences.

| # | Experience | KX maturity | Engineering status | Evidence |
|---|---|---|---|---|
| 8 | LCD institutional corpus | **E3** | proven_live | 19 live public pages → `sha256:582187c7ac71a101` → static navigator; proof run 33278164562 |
| 9 | LCD thesis/resources subset | **E3** | proven_live | same source release; 4 exact curated IDs → `sha256:01bbef6b349aefea`; proof run 33278265492 |

The other 13 records remain governed in the machine ledger with their prior blockers/statuses.

## What changed

The institutional experience crossed E1, E2 and E3 in one bounded run: the pinned LCD producer fetched the complete public WordPress **page** collection, produced a `completed_trusted` run, Knowledge Experiences froze its browse index into a `CollectionRelease`, and the existing static renderer produced a usable HTML artifact. The release deliberately excludes WordPress posts because repeated live probes returned HTTP 500 from `/wp-json/wp/v2/posts`; no post coverage is claimed.

The thesis/resources experience is the stronger composability result. It reused the exact same source release and selected these four real identities: `lcd:page:1948`, `lcd:page:1951`, `lcd:page:2147`, `lcd:page:2562`. No adapter, renderer, producer projection or kernel change was needed: the marginal experience was **selection + curation + configuration**.

## Maturity semantics

- `E0` — declared.
- `E1` — reproducible `CollectionRelease` from real source material.
- `E2` — human-usable rendered real-source artifact.
- `E3` — important real-source seam has executable evidence.
- `E4` — deployed or repeatedly used by a real consumer.

Neither LCD experience is E4: checked-in artifacts and CI evidence are not the same as deployment or repeated external use.

## Next frontier

The highest-information next move is a **second real-source domain**, preferably one of the already-proven Paper KB paths (bibliography, author works, or full review snapshot) using an explicitly approved real corpus. That tests whether the low marginal-cost pattern survives outside LCD rather than overfitting further around one producer.

## Remaining E0 cases

The machine ledger retains all remaining cases and their exact blockers: Thesis bibliography; Thesis rapid paper review; Author works; Working-paper series; Economic-complexity reading path; FCV literature corpus; Literature-review snapshot; Course readings; Economics of Aggregation programme; Working-memory journal; Knowledge-ecosystem technical docs; Personal publications; Policy/research dossier.
