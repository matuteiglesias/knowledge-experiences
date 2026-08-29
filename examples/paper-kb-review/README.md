# Paper KB → Abstract Scroller proof

This directory contains the declarative V1.3 recipe. CI creates `generated/paper.review-record.v1.jsonl` with the real pinned Paper KB writer/projection over sanitized records, then `kx build` hands those exact producer bytes to the pinned Abstract Scroller snapshot compiler.

The generated review JSONL is intentionally not committed. A real corpus instance must use an explicitly approved corpus and preserve its rights/provenance boundary.
