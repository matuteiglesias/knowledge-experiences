# V1.4 — Ecosystem fan-out findings

## Purpose

V1.4 tests whether the composition model survives outside the first Paper KB path and whether mature existing experiences should be absorbed, adapted, or explicitly left vertical.

## Lane A — LCD non-paper producer

Inspected `matuteiglesias/lcd-UBA-knowledgebase` at commit `dcaa61e338b284d43764b9c06a0f112629e958f6`.

The producer already owns stable document contracts (`page_doc.v1`, `chunk_doc.v1`, `run_manifest.v1`) and a run-scoped combined `indexes/title_slug_index.json`. The index is a particularly cheap browsing seam because it already combines page and post identity, title, URL, entity type and content hash.

Decision: **reuse the existing producer artifact; do not create a new LCD catalog contract merely for this consumer.**

Knowledge Experiences adds only `lcd-title-slug-index`, mapping the bounded consumer surface into generic display items. Existing `selection.mode=facets` can already derive a page-only or post-only collection without new core semantics.

Pinned proof run:

- repository commit: `dcaa61e338b284d43764b9c06a0f112629e958f6`;
- trusted run: `local_contract_check_20260424T161417Z`;
- producer status: `completed_trusted` / manifest `pass`;
- combined index rows: 2 (one page, one post).

Maturity warning: the run name and repository evidence identify this as a local contract-check run. Treat the seam as executable mechanics, not a live-source E1/E2 institutional corpus. A later approved live run can reuse the same composition configuration with a new exact source release.

Observed friction: LCD records carry per-record `content_hash`, but the current generic item provenance model exposes stable object identity and source-release SHA rather than a first-class record hash. Reproducibility is still preserved by freezing the source file SHA; record-level hash exposure is a V2 evidence candidate only if another producer needs it.

## Lane B — mature vertical experiences

### Thesis

Inspected `matuteiglesias/thesis` at `7265018750db0f96b69efd4048aedad06ad803fc`.

The repository is a Docusaurus research portal, not a generic renderer waiting to be extracted. Its value includes curated research trails, status distinctions (current manuscript, peer-reviewed publication, working paper, thesis result, research direction, archival material), historical-vs-current authority rules and a deep thesis archive.

Decision: **vertical exception / adopt, do not replatform.** Knowledge Experiences may eventually describe or point to selected trails, but it should not replace the portal's editorial hierarchy or claim ownership of research-status semantics.

Potential reusable lesson for V2: ordered/grouped reading trails are real composition pressure. Do not add a generic trail model until the census shows whether course readings or another independent experience needs the same semantics.

### Journal

Inspected `matuteiglesias/journal` at `11fc6ea42e13866cd952e4957c26dd2e55ef78d7`.

The repository is a Quartz working-memory/publication garden with explicit `publish: true` filtering, draft/private exclusions, backlinks and a strong rule that dated notes are historical evidence rather than current operational truth.

Decision: **vertical exception / publication surface, not a renderer to absorb.** Its publication filter is an editorial/governance boundary. Feeding material into it belongs near the parked W5b publication frontier, not V1 composition mechanics.

## Lane C — optional intelligence

No selected V1.4 experience requires semantic inspection or chat. Therefore `CollectionRelease → Knowledge Inspect` remains a **justified non-edge for this wave**. Existing Paper KB → Knowledge Inspect proofs remain available independently; do not make intelligence critical-path infrastructure merely to complete a topology diagram.

## Lane D — governed evidence selection

No selected V1.4 experience requires KB Artifacts evidence promotion/selection semantics. Therefore no new Knowledge Experiences ↔ KB Artifacts edge is introduced. When a real dossier or curated evidence workflow appears, that consumer pressure can determine whether a selection receipt or artifact reference is needed.

## Fan-out result

V1.4 produced one new non-paper executable seam and three deliberate non-expansions:

```text
LCD run index ──> bounded adapter ──> static navigator       ACCEPTED MECHANICS
Thesis portal                                                KEEP VERTICAL
Journal / Quartz publication garden                         KEEP VERTICAL
Knowledge Inspect / KB Artifacts optional lanes             NO NEW EDGE YET
```

This is a positive result. Fan-out is not measured by the number of arrows added; it is measured by whether real systems can be composed without erasing their authority boundaries.
