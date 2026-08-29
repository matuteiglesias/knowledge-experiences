# R5 — teaching exercise catalog enters the ladder

R5 adds the first experience discovered after the original 15-case census: the 60-page `repo.ldd-uba` teaching exercise catalog. It is kept separate from #10 Course readings because exercises and readings have different semantics.

## Exact real-source path

```text
repo.ldd-uba@1e8a3c400e1296055614e0dec627f7177c730537
        ↓  content/notebooks/[0-9]{2}.md (60 exact numbered pages)
metadata-only Git projection
        ↓
CollectionRelease sha256:099e370174316de7
        ↓
static-navigator
        ↓
ExperienceRelease sha256:24c5001976808e10
        ↓
frozen teaching exercise navigator
        ↓
persistent cross-repo reproduction proof
```

Final artifact SHA-256: `fbee88a9092a022f70c3c6224e04c28e6ef5e7ff3f99b2205c3348be92ef1580`.

## Drift discovered during materialization

The pre-R5 README declared 58 exercises. The actual source tree contained numbered exercise files through `60.md` plus four category `_index.md` pages. R5 therefore did not accept the naive 64-record recursive projection. The producer README was corrected first, and the accepted KX source boundary explicitly full-matches the 60 numbered exercise paths.

## Governance change

The census checker now preserves the original 15 entries as a minimum append-only baseline and requires contiguous IDs through the current count. This removes an accidental discovery ceiling without weakening any E1/E2/E3/E4 evidence requirement.

## Boundary

KX does not claim the notebooks execute, belong to a current course, or replace the upstream Hugo catalog. It freezes and proves the exact numbered teaching-exercise navigation corpus only. No renderer, domain schema, ordering model, or composition-kernel behavior was added; the only projection extension is an explicit provenance-bearing path filter.

## Result

The governed census becomes **16 experiences: 5×E3 + 1×E1 + 10×E0**.
