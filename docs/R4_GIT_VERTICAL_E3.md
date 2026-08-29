# R4 — persistent Git vertical E3 seams

R4 upgrades the two R3 real-source frozen snapshots from E2 to E3 by making their complete producer-to-experience paths executable in persistent CI. No composition semantics or renderer capability changed.

| Census | Producer pin | CollectionRelease | ExperienceRelease | Artifact SHA-256 |
|---|---|---|---|---|
| #11 | `matuteiglesias/thesis@7265018750db0f96b69efd4048aedad06ad803fc` | `sha256:3c46140540fd493c` | `sha256:e48e77652ca1c927` | `319c680845f7e692555dd5971d8932b8b0db2ac5c736d3b03edeac1e83277e0f` |
| #12 | `matuteiglesias/journal@11fc6ea42e13866cd952e4957c26dd2e55ef78d7` | `sha256:1cdee66182d2514e` | `sha256:943be14e62f6a14f` | `5a99c59f74774872d5a3c8da68ad985ed9176fc22829b0bce3f810abd8fdb32e` |

## Executable proof

`.github/workflows/git-vertical-seam-proof.yml` checks out both exact upstream public Git commits, reruns `scripts/materialize_markdown_collection.py`, compares the source projection and receipt, runs `kx doctor`, rebuilds the experience, and compares the accepted CollectionRelease, ExperienceRelease, and final `site/index.html` byte-for-byte.

## Boundary

The proof is intentionally pinned. It establishes reproducibility of an accepted real-source seam, not freshness of upstream `main`. A newer source state requires an explicit governed refresh and a new release identity. E4 additionally requires real operational use; stronger CI is not a substitute.

## Result

The ladder becomes **4×E3 + 1×E1 + 10×E0**. The empty E2 rung is not filled cosmetically; the next E2 should come from a genuinely useful new human experience.
