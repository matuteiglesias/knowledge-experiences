# Experience Census — expanding executable real-use ladder

The machine-readable authority is `docs/experience-census.v1.json`. The original 15-entry census is now a governed baseline, not a permanent ceiling: new concrete experiences may be appended with contiguous IDs and the same strict E0–E4 evidence rules.

## Current frontier

**16 governed experiences: 5 are E3, 1 is E1, and 10 remain E0.** R5 adds the first post-seed discovery: a real teaching-exercise corpus that was visible in the estate but semantically distinct from the original Course readings case.

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
| 11 | Economics of Aggregation programme | **E3** | proven_real_source_seam | exact Git producer → deterministic frozen experience + persistent proof |
| 12 | Working-memory journal | **E3** | proven_real_source_seam | exact Git producer → deterministic frozen experience + persistent proof |
| 13 | Knowledge-ecosystem technical docs | **E1** | existing_vertical | 32 exact-Git metadata records → reproducible E1 CollectionRelease |
| 14 | Personal publications | **E0** | blocked_capability | declared / prior engineering evidence |
| 15 | Policy/research dossier | **E0** | blocked_capability | declared / prior engineering evidence |
| 16 | LDD UBA teaching exercise catalog | **E3** | proven_real_source_seam | 60 exact numbered Git exercise pages → `sha256:24c5001976808e10` + persistent real-source proof |

## R5 interpretation

`repo.ldd-uba` owns a Hugo teaching catalog with 60 numbered exercise pages and four category `_index.md` navigation pages. KX uses an explicit repo-relative path filter to snapshot only `content/notebooks/[0-9]{2}.md`, then renders a separate immutable navigator and proves the full seam from the repaired producer commit. The original Hugo site remains the pedagogical/content authority.

The first R5 attempt was useful drift sensing: the README claimed 58 exercises while the repository contained numbered exercises through 60, and a recursive Markdown projection also included four category indexes. The upstream README was repaired before the accepted source was repinned; the KX path boundary now states exactly what counts as an exercise.

This is deliberately **not** census #10 Course readings. Exercises and readings are different pedagogical objects; collapsing them merely to fill an existing row would weaken the ledger. The census therefore grows append-only to #16 instead.

## Next frontier

Paper KB remains the highest-value blocked scientific lane. Separately, the growing census can now discover additional real experiences rather than forcing the estate into the original 15 hypotheses. E4 still requires actual operation/use evidence, not more CI.
