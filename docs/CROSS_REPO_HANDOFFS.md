# Cross-Repository Handoffs

The composition layer should improve neighboring repositories only where a real experience exposes a bounded missing seam.

## Paper KB

Current role: governed paper corpus authority.

Expected bounded improvement:

- inspect the real `chunk_set` / paper metadata before changing anything;
- keep `paper.review-record@1` review-specific;
- if author/contributor/series browsing requires a richer public projection, prefer a producer-owned catalog projection (candidate: `paper.catalog-record@1`);
- expose it through a deterministic CLI/artifact with canonical `paper_uid` and provenance;
- add an executable producer → Knowledge Experiences proof.

Do not move paper semantics or source normalization into this repository.

## Abstract Scroller

Current role: immutable review snapshot compiler + fast static reader.

Expected bounded improvement:

- recognize Knowledge Experiences as a composition authority/renderer caller;
- accept a narrow handoff or adapter from a compatible `ExperienceRelease` while preserving its current preferred paper-review seam;
- keep snapshot representation, ordering, tiling/masks, and reader implementation owned by Scroller.

Do not turn Scroller into a generic corpus store or universal navigator.

## LCD UBA Knowledgebase

Current role: governed WordPress-derived document corpus with normalized docs/chunks and trusted run state.

Expected bounded improvement:

- expose/pin the exact latest-trusted artifacts needed by a collection compiler;
- add a deterministic export/manifest only if current run artifacts are awkward to consume directly;
- prove one institutional-doc collection end to end.

Do not duplicate LCD document normalization here.

## Thesis

Current role: mature curated research-programme portal and thesis archive.

Expected bounded improvement:

- add explicit ecosystem role/authority metadata if absent;
- document which navigation semantics are declarative (status, reading trails, groups, featured work) versus truly vertical;
- use it as a reverse-engineering specimen for V2, not as a generic renderer target that must be rebuilt.

Do not flatten historical/current intellectual-status semantics to fit a generic schema.

## Journal

Current role: semantic working-memory garden/publication surface with explicit publication policy.

Expected bounded improvement:

- add explicit ecosystem role/authority metadata if absent;
- document what an ExperienceSpec may reference versus what remains Journal-owned publication policy;
- preserve Quartz and journal content as a vertical surface.

Do not make public-note eligibility a global collection policy.

## Knowledge Inspect

Current role: semantic/analytical inspection capability.

Possible later improvement, only when demanded:

- accept a bounded collection scope or collection release as inspection input;
- emit derived observations/intelligence that can be attached to an experience without becoming source truth.

Do not equate observation with claim, publication, or selected evidence.

## KB Artifacts

Current role: deterministic evidence exploration/selection/governance capability.

Possible later improvement, only when demanded:

- provide a governed selection that can determine collection membership;
- retain evidence governance authority upstream.

Do not invent a mandatory direct Knowledge Inspect edge.

## Knowledge Ecosystem Docs

Current role: ecosystem architecture authority.

Expected after proofs exist:

- register `repo.knowledge-experiences`;
- promote W5a as the governed knowledge → collection → experience seam;
- record proven producer/renderer edges and justified non-edges;
- keep W5b editorial claim/publication automation parked until real repeated publication consumers exist.

## Change rule

Every cross-repo PR should state:

1. the exact experience that pulled the change;
2. the current authority being preserved;
3. the smallest new seam required;
4. how the seam is tested;
5. what tempting broader work is deliberately excluded.
