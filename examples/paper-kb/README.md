# Paper KB executable proof inputs

`generated.catalog.jsonl` is intentionally **not committed**. The cross-repository workflow checks out the exact Paper KB commit pinned in the specs, creates sanitized chunk-set artifacts through the real Paper KB writer, exports them through the real `paper.catalog-record@1` projection, and writes the generated JSONL here for the duration of CI.

The two experiences then prove marginal composability:

1. the full catalog uses the static navigator with author/year/venue facets;
2. the author subset reuses the same source and renderer, changing only declarative collection selection.

These are interface proofs, not claims that a rights-sensitive real paper corpus has been published or deployed.
