# Experience Census — V1.5

This is the pressure-test ledger for `knowledge-experiences`. The machine-readable authority for the fifteen rows is `docs/experience-census.v1.json`; this page explains how to read it.

## Two different kinds of maturity

`E0`–`E4` remains deliberately strict and measures **concrete Knowledge Experiences composition maturity**:

- `E0` — declared: intended authorities and renderer/profile are known;
- `E1` — compiled: a reproducible `CollectionRelease` exists from real source material;
- `E2` — rendered: a human can open/use the generated real-source experience;
- `E3` — proven: the important real-source cross-repository seam has executable evidence;
- `E4` — operational: deployed or repeatedly used by a real consumer.

A sanitized integration proof is engineering evidence, not real-source maturity. Likewise, a mature pre-existing Thesis or Journal site does not magically become an E1 Knowledge Experiences collection when no CollectionRelease exists. V1.5 therefore records `engineering_status` separately.

## Census result

| # | Experience | KX maturity | Engineering status | Current disposition |
|---|---|---|---|---|
| 1 | Thesis bibliography | E0 | proven_sanitized | real approved Paper KB release needed; then configuration |
| 2 | Thesis rapid paper review | E0 | proven_sanitized | Scroller handoff ready; real review release needed |
| 3 | Author works | E0 | proven_sanitized | author subset is configuration-only once real catalog exists |
| 4 | Working-paper series | E0 | blocked_producer_metadata | series/venue must become authoritative upstream |
| 5 | Economic-complexity reading path | E0 | blocked_capability | ordered/grouped curation is not yet modeled |
| 6 | FCV literature corpus | E0 | design_ready | approved corpus needed; static/private path already reusable |
| 7 | Literature-review snapshot | E0 | proven_sanitized | complete review handoff ready; real release needed |
| 8 | LCD institutional corpus | E0 | proven_contract_check | non-paper seam works; checked run is explicitly local_contract_check |
| 9 | LCD thesis/resources subset | E0 | design_ready | curate exact real IDs before inventing taxonomy |
| 10 | Course readings | E0 | blocked_capability | independently repeats ordered/grouped-reading pressure |
| 11 | Economics of Aggregation programme | E0 | existing_vertical | keep Thesis/Docusaurus vertical |
| 12 | Working-memory journal | E0 | existing_vertical | keep Quartz publication/editorial vertical |
| 13 | Knowledge-ecosystem technical docs | E0 | existing_vertical | existing architecture docs surface already solves primary need |
| 14 | Personal publications | E0 | blocked_capability | first real multi-source attempt needed |
| 15 | Policy/research dossier | E0 | blocked_capability | multi-source + curation receipt pressure; intelligence optional |

## What the all-E0 result means

It does **not** mean V1 failed. It means the architecture and seams were developed faster than concrete real-source experience releases were admitted into this execution surface. We now know much more precisely which cases are cheap:

- Thesis bibliography, Author works, FCV literature and full Literature-review snapshot are largely waiting for approved real producer releases, not another application.
- LCD institutional browsing needs a verified live producer run, not another composition abstraction.
- Thesis, Journal and ecosystem docs already have strong vertical human experiences and should not be rebuilt merely to increase a census score.

That is a useful stop signal. Inflating fixture proofs to E2/E3 would hide the real next job: **use the machinery on real approved material**.

## Repeated friction that may justify V2 later

Two patterns are now stronger than isolated ideas.

**Ordered/grouped reading trails.** Economic-complexity reading paths (#5) and Course readings (#10) independently need curator-controlled sequence/group semantics, while the existing Economics of Aggregation vertical (#11) demonstrates that curated trails are genuinely useful. This is the strongest V2 candidate, but it should still be pulled by one real materialization rather than implemented from prose alone.

**Multi-source collections plus curation provenance.** Personal publications (#14) and Policy/research dossier (#15) both cross source-authority boundaries. The dossier adds explicit selection/governance pressure. This is a real composition-model frontier, but no real two-authority collection has yet been attempted, so namespace/union/receipt semantics remain premature.

Weaker or producer-local observations should stay local: working-paper series metadata is a Paper KB producer gap; LCD record-level `content_hash` exposure is only one provenance case; selected Abstract Scroller subsets remain a bounded handoff limitation until a real selected-review experience needs them.

## Marginal-cost evidence

The important result is already visible even without E1 claims:

```text
first paper experience    → producer projection + adapter + renderer baseline
second author experience  → selection/configuration over the same release
second paper renderer     → one bounded handoff; producer bytes remain producer-owned
first non-paper producer  → one bounded adapter; existing selection/renderer reused unchanged
mature vertical products  → classified, not rewritten
```

The model is therefore showing the desired direction: new experience families cost a bounded adapter/handoff, while nearby experiences increasingly become configuration and curation.

## Next regime

After V1.5, the default should be **real use → observation → selective evolution**, not immediate V2 construction. The most valuable next evidence is one approved real Paper KB experience and one verified live LCD experience. Only implement a V2 abstraction when a real use exposes repeated friction already visible in this ledger.

The original required census names remain represented explicitly: Thesis bibliography, Author works, Working-paper series, LCD institutional corpus, Economics of Aggregation programme, and Policy/research dossier, together with the other nine cases.
