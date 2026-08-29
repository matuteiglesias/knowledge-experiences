# Experience Census — multi-lane real-use frontier

The machine-readable authority is `docs/experience-census.v1.json`. `E0`–`E4` remains strict: a concrete experience advances only on evidence appropriate to that rung.

## Current frontier

**2 experiences are E3, 3 are E1, and 10 remain E0.** R2 intentionally populated the lower rung across three independent public Git producers instead of manufacturing duplicate human interfaces.

| # | Experience | Maturity | Engineering status | Current evidence |
|---|---|---|---|---|
| 1 | Thesis bibliography | **E0** | proven_sanitized | declared / prior engineering evidence |
| 2 | Thesis rapid paper review | **E0** | proven_sanitized | declared / prior engineering evidence |
| 3 | Author works | **E0** | proven_sanitized | declared / prior engineering evidence |
| 4 | Working-paper series | **E0** | blocked_producer_metadata | declared / prior engineering evidence |
| 5 | Economic-complexity reading path | **E0** | blocked_capability | declared / prior engineering evidence |
| 6 | FCV literature corpus | **E0** | design_ready | declared / prior engineering evidence |
| 7 | Literature-review snapshot | **E0** | proven_sanitized | declared / prior engineering evidence |
| 8 | LCD institutional corpus | **E3** | proven_live | trusted live LCD source → rendered real-source experience + executable proof |
| 9 | LCD thesis/resources subset | **E3** | proven_live | trusted live LCD source → rendered real-source experience + executable proof |
| 10 | Course readings | **E0** | blocked_capability | declared / prior engineering evidence |
| 11 | Economics of Aggregation programme | **E1** | existing_vertical | 89 exact-Git metadata records → `sha256:3c46140540fd493c` |
| 12 | Working-memory journal | **E1** | existing_vertical | 2868 exact-Git metadata records → `sha256:1cdee66182d2514e` |
| 13 | Knowledge-ecosystem technical docs | **E1** | existing_vertical | 32 exact-Git metadata records → `sha256:899417efd880dd51` |
| 14 | Personal publications | **E0** | blocked_capability | declared / prior engineering evidence |
| 15 | Policy/research dossier | **E0** | blocked_capability | declared / prior engineering evidence |

## R2 interpretation

The three E1 releases are deliberately **collection-only**. `repo.thesis`, `repo.journal`, and `repo.knowledge-ecosystem-docs` already own mature human surfaces; Knowledge Experiences does not gain maturity by cloning Docusaurus or Quartz. E1 means the exact real source can now cross the composition boundary reproducibly. E2 waits for a distinct human-facing use that creates additional value.

The Journal release is stricter still: only notes carrying explicit `publish: true` metadata are admitted, while `publish: false`, drafts and excluded private/template paths are not reinterpreted downstream.

Paper KB remains E0 in the concrete census because its current repository surface contains real production machinery and fixtures but no approved real versioned corpus selected for these experiences. That boundary is preserved rather than promoting fixtures.

## Next frontier

The highest-information next moves are: a real approved Paper KB corpus to populate the scientific lane; or one genuinely distinct consumer of an R2 CollectionRelease to justify E2. Broad V2 construction is still not warranted.
