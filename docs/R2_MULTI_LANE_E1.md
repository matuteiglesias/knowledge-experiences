# R2 — multi-lane E1 source releases

R2 deliberately moves three mature verticals only to **E1**. Their existing Docusaurus/Quartz sites remain the human authorities; this tranche proves a reproducible composition boundary without duplicating those products.

| Census | Producer | Exact commit | Scope | Records | CollectionRelease |
|---|---|---|---|---:|---|
| #11 | `repo.thesis` | `7265018750db0f96b69efd4048aedad06ad803fc` | `docs` / `all-markdown` | 89 | `sha256:3c46140540fd493c` |
| #12 | `repo.journal` | `11fc6ea42e13866cd952e4957c26dd2e55ef78d7` | `content` / `explicit-publish` | 2868 | `sha256:1cdee66182d2514e` |
| #13 | `repo.knowledge-ecosystem-docs` | `ab59145a0378edc5f56b61e03951f93ca018c60a` | `docs` / `all-markdown` | 32 | `sha256:899417efd880dd51` |

## Boundary

Only metadata needed for collection identity/navigation and exact source pointers are copied. Markdown bodies remain producer-owned. No document schema, publication schema, second renderer, ordering model, or multi-source union is introduced.

For the Journal, membership is conservative: explicit `publish: true`, not `draft: true`, and no `private`, `templates`, or `.obsidian` path. This is a bounded KX collection rule for this release, not a redefinition of Quartz's full publication semantics.

## Result

The maturity distribution becomes **2×E3 + 3×E1 + 10×E0**. This is a healthier ladder than promoting mature verticals to E2/E3 merely because they already have websites.
