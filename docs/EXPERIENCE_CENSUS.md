# Experience Census — populated real-use ladder

The machine-readable authority is `docs/experience-census.v1.json`. `E0`–`E4` remains strict: each rung is earned by the evidence it names.

## Current frontier

**2 experiences are E3, 2 are E2, 1 is E1, and 10 remain E0.** R3 converts two accepted real-source collections into distinct frozen human snapshots while leaving their upstream live products authoritative.

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
| 11 | Economics of Aggregation programme | **E2** | existing_vertical | frozen static snapshot → `sha256:e48e77652ca1c927` / `319c680845f7e692…` |
| 12 | Working-memory journal | **E2** | existing_vertical | frozen static snapshot → `sha256:943be14e62f6a14f` / `5a99c59f74774872…` |
| 13 | Knowledge-ecosystem technical docs | **E1** | existing_vertical | 32 exact-Git metadata records → reproducible E1 CollectionRelease |
| 14 | Personal publications | **E0** | blocked_capability | declared / prior engineering evidence |
| 15 | Policy/research dossier | **E0** | blocked_capability | declared / prior engineering evidence |

## Why these are E2 and not duplicate products

The thesis snapshot is a portable point-in-time inventory of one exact research-programme release. The Journal snapshot is an auditable point-in-time inventory of only the conservative explicit-publication subset. Neither tries to recreate Docusaurus/Quartz semantics, backlinks, editorial flow, or live-current authority.

Knowledge-ecosystem technical docs remains E1. Its existing Docusaurus control surface already solves the primary human experience, and R3 found no distinct second consumer worth rendering merely to populate a rung.

Paper KB remains E0 for concrete experiences until an approved real corpus is selected. Production code plus fixtures is still not real-source maturity.

## Next frontier

The ladder now has real occupancy at E1, E2 and E3. The highest-information next move is no longer another generic static snapshot: it is either a real Paper KB scientific corpus, or genuine use of one E2 snapshot that creates evidence for a persistent E3 seam / eventual E4 operation.
