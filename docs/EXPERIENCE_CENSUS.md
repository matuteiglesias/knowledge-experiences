# Experience Census — operational real-use ladder

The machine-readable authority is `docs/experience-census.v1.json`. The original 15-entry census is an append-only baseline; each E0–E4 rung remains evidence-gated.

## Current frontier

**16 governed experiences: 1 is E4, 8 are E3, 1 is E1, and 6 remain E0.** R8 removes the real-Paper-KB-source blocker for three experiences without adding any KX capability.

| # | Experience | Maturity | Engineering status | Current evidence |
|---|---|---|---|---|
| 1 | Thesis bibliography | **E3** | proven_real_source_seam | exact 19-paper `tesis-cited` catalog → deterministic frozen navigator |
| 2 | Thesis rapid paper review | **E0** | blocked_producer_metadata | real review projection exists, but abstracts/date/venue are currently sparse/null |
| 3 | Author works | **E3** | proven_real_source_seam | existing author facet selects 2 real Angus Deaton records from the same 19-paper source |
| 4 | Working-paper series | **E0** | blocked_producer_metadata | authoritative series/venue metadata remains insufficient |
| 5 | Economic-complexity reading path | **E3** | proven_real_source_seam | six exact Thesis Trail B steps preserve producer-curated order |
| 6 | FCV literature corpus | **E3** | proven_real_source_seam | exact 7-paper `eric-mv` seed corpus → deterministic private navigator; producer fixture also has 7 chunk sets |
| 7 | Literature-review snapshot | **E0** | blocked_producer_metadata | real review projection exists, but substantive review metadata is not yet adequate |
| 8 | LCD institutional corpus | **E4** | proven_live | second governed live refresh with source-diff/downstream operation receipt |
| 9 | LCD thesis/resources subset | **E3** | proven_live | refreshed trusted parent source → same 4 exact IDs; remains E3 |
| 10 | Course readings | **E0** | blocked_capability | next real ordered/grouped teaching case must test R7 capability first |
| 11 | Economics of Aggregation programme | **E3** | proven_real_source_seam | exact Git producer → deterministic frozen experience + persistent proof |
| 12 | Working-memory journal | **E3** | proven_real_source_seam | exact Git producer → deterministic frozen experience + persistent proof |
| 13 | Knowledge-ecosystem technical docs | **E1** | existing_vertical | 32 exact-Git metadata records → reproducible CollectionRelease; existing Docusaurus surface is sufficient |
| 14 | Personal publications | **E0** | blocked_capability | wait for a concrete multi-source/publication need |
| 15 | Policy/research dossier | **E0** | blocked_capability | wait for concrete multi-source dossier pressure |
| 16 | LDD UBA teaching exercise catalog | **E3** | proven_real_source_seam | exact Git producer → deterministic frozen experience + persistent proof |

## R6 interpretation

LCD institutional browsing crossed E4 because the producer was operated again against the live public WordPress page surface, yielding a distinct trusted run after R1. KX compared record identities and content hashes, rebuilt the frozen human experience, and verified that the existing four-ID thesis/resources derivative still composes from the refreshed source.

The thesis/resources subset deliberately remains E3. One parent refresh does not manufacture a second E4 claim.

## R7 interpretation

The first V2 capability was earned by a real representational failure. `repo.thesis` already declared Trail B as a six-step editorial sequence; V1 could select the IDs but canonicalized and re-sorted them, erasing the reading path. R7 added only `ordered_ids` plus `curated` navigation. Grouping remains deliberately absent.

## R8 interpretation

R8 used `paper-kb@e82e82deb646f30707306cd13ff8ba279c8bad50` as a real-source pressure test. The 19-paper `tesis-cited` catalog and seven-paper `eric-mv` corpus produced three different E3 experiences: Thesis bibliography, a real author-facet view, and the bounded FCV literature seed corpus. The existing `paper-catalog-jsonl` adapter, selection semantics and static navigator were sufficient; **no KX kernel capability changed**.

This is evidence of falling marginal cost rather than merely a larger E count. One governed producer surface fanned out into multiple semantically distinct experiences through configuration and exact-source proof.

R8 also produced a negative result: the real thesis `paper.review-record@1` projection currently has sparse substantive review metadata. `thesis-rapid-paper-review` and `literature-review-snapshot` therefore remain E0. The pressure is upstream in Paper KB metadata preservation/enrichment, not evidence for a new KX abstraction.

## Next frontier

Prefer external/useful evidence over more kernel work:

1. operate or circulate one of the new Paper KB E3 experiences and let real use create an E4 candidate;
2. test Course readings against R7 ordered semantics before adding grouping;
3. improve real Paper KB review metadata, then rerun the review experiences;
4. grow the FCV seed corpus only as concrete research demand adds papers.

Do not add a new V-wave merely because more experiences can be imagined.
