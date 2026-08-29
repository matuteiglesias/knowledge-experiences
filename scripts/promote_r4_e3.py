#!/usr/bin/env python3
"""Promote the two accepted Git-backed frozen snapshots from E2 to E3."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONFIG = {
    11: {
        "dir": "economics-of-aggregation-programme",
        "source": "repo.thesis",
        "label": "Economics of Aggregation programme",
    },
    12: {
        "dir": "working-memory-journal",
        "source": "repo.journal",
        "label": "Working-memory journal",
    },
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    proofs = {}
    for row_id, cfg in CONFIG.items():
        base = ROOT / "experiences" / "real" / cfg["dir"]
        proof = load(base / "e3-proof.json")
        e2 = load(base / "e2-proof.json")
        if proof.get("result") != "pass" or proof.get("proof") != "exact-git-source-to-frozen-experience":
            raise SystemExit(f"row {row_id}: E3 cross-repo proof not passing")
        for field in ("collection_release_id", "experience_release_id", "rendered_artifact_sha256"):
            if proof.get(field) != e2.get(field):
                raise SystemExit(f"row {row_id}: {field} differs from accepted E2 evidence")
        proofs[row_id] = proof

    census_path = ROOT / "docs" / "experience-census.v1.json"
    census = load(census_path)
    rows = {row["id"]: row for row in census["experiences"]}
    for row_id, cfg in CONFIG.items():
        row = rows[row_id]
        proof = proofs[row_id]
        if row["composition_maturity"] != "E2":
            raise SystemExit(f"row {row_id}: expected E2 parent state")
        row.update(
            {
                "composition_maturity": "E3",
                "engineering_status": "proven_real_source_seam",
                "cross_repo_proof": f"experiences/real/{cfg['dir']}/e3-proof.json + .github/workflows/git-vertical-seam-proof.yml",
                "incremental_work": "persistent proof only: exact upstream Git checkout is reprojected and rebuilt with the existing materializer, kernel and static renderer",
                "blocker": "none for reproducible E3 seam; E4 still requires genuine operational use/refresh demand rather than stronger CI",
                "observed_friction": "large public Git producers are cheap to reproduce when commit identity and selection policy are explicit; no new adapter or renderer was needed",
                "engineering_evidence": row["engineering_evidence"] + [
                    f"R4 persistent cross-repo CI reproduces {proof['source_repo']}@{proof['source_commit']} through source projection, CollectionRelease {proof['collection_release_id']}, ExperienceRelease {proof['experience_release_id']} and artifact {proof['rendered_artifact_sha256']}"
                ],
                "evidence_boundary": "E3 means the accepted real-source producer-to-experience seam is executable and reproducible from exact Git pins; it does not claim live deployment, automatic refresh, audience use, or E4 operation",
                "next_real_action": "use the frozen experience in a real research/publication workflow or perform a governed refresh from a newer upstream commit; only repeated operational demand can justify E4",
            }
        )

    census["as_of"] = "2026-08-29"
    census_path.write_text(json.dumps(census, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = Counter(row["composition_maturity"] for row in census["experiences"])
    expected = Counter({"E0": 10, "E1": 1, "E3": 4})
    if counts != expected:
        raise SystemExit(f"unexpected maturity distribution after R4: {counts}")

    human = [
        "# Experience Census — executable real-use ladder",
        "",
        "The machine-readable authority is `docs/experience-census.v1.json`. `E0`–`E4` remains strict: each rung is earned by the evidence it names.",
        "",
        "## Current frontier",
        "",
        "**4 experiences are E3, 1 is E1, and 10 remain E0.** R4 promotes the two R3 Git-backed snapshots only after their complete source-to-artifact paths became persistent executable cross-repository proofs.",
        "",
        "| # | Experience | Maturity | Engineering status | Current evidence |",
        "|---|---|---|---|---|",
    ]
    for row in census["experiences"]:
        evidence = "declared / prior engineering evidence"
        if row["id"] in proofs:
            p = proofs[row["id"]]
            evidence = f"exact Git producer → deterministic frozen experience / `{p['experience_release_id']}`"
        elif row["id"] == 13:
            evidence = "32 exact-Git metadata records → reproducible E1 CollectionRelease"
        elif row["id"] in {8, 9}:
            evidence = "trusted live LCD source → rendered real-source experience + executable proof"
        human.append(f"| {row['id']} | {row['name']} | **{row['composition_maturity']}** | {row['engineering_status']} | {evidence} |")
    human += [
        "",
        "## R4 interpretation",
        "",
        "The thesis and Journal E3 claims are stronger than checked-in snapshots: CI checks out the exact real upstream commits, reruns the bounded metadata projection, reproduces the accepted collection and human experience, and compares every identity-bearing release plus the final HTML artifact. The upstream repositories retain domain/editorial authority throughout.",
        "",
        "Knowledge-ecosystem technical docs remains E1 because a distinct second human experience is still not justified. Paper KB concrete experiences remain E0 because the tracked repository still contains production machinery plus fixtures, not an approved real governed corpus.",
        "",
        "## Next frontier",
        "",
        "The most informative next work is now either (a) a genuinely real Paper KB corpus, (b) a new lower-rung domain with clean source authority, or (c) actual use/refresh of an E3 experience sufficient to test E4 operation. More CI alone cannot earn E4.",
        "",
    ]
    (ROOT / "docs" / "EXPERIENCE_CENSUS.md").write_text("\n".join(human), encoding="utf-8")

    system_path = ROOT / "SYSTEM.yaml"
    system = system_path.read_text(encoding="utf-8")
    system = re.sub(
        r"  maturity_snapshot:\n(?:    E\d: \d+\n)+",
        "  maturity_snapshot:\n    E3: 4\n    E1: 1\n    E0: 10\n",
        system,
    )
    system = re.sub(
        r"  phase: .*\n  next_gate: .*\n",
        "  phase: executable-multi-domain-ladder\n  next_gate: paper-real-corpus-or-e4-operational-use\n",
        system,
    )
    system_path.write_text(system, encoding="utf-8")

    lines = [
        "# R4 — persistent Git vertical E3 seams",
        "",
        "R4 upgrades the two R3 real-source frozen snapshots from E2 to E3 by making their complete producer-to-experience paths executable in persistent CI. No composition semantics or renderer capability changed.",
        "",
        "| Census | Producer pin | CollectionRelease | ExperienceRelease | Artifact SHA-256 |",
        "|---|---|---|---|---|",
    ]
    for row_id in (11, 12):
        p = proofs[row_id]
        lines.append(f"| #{row_id} | `{p['source_repo']}@{p['source_commit']}` | `{p['collection_release_id']}` | `{p['experience_release_id']}` | `{p['rendered_artifact_sha256']}` |")
    lines += [
        "",
        "## Executable proof",
        "",
        "`.github/workflows/git-vertical-seam-proof.yml` checks out both exact upstream public Git commits, reruns `scripts/materialize_markdown_collection.py`, compares the source projection and receipt, runs `kx doctor`, rebuilds the experience, and compares the accepted CollectionRelease, ExperienceRelease, and final `site/index.html` byte-for-byte.",
        "",
        "## Boundary",
        "",
        "The proof is intentionally pinned. It establishes reproducibility of an accepted real-source seam, not freshness of upstream `main`. A newer source state requires an explicit governed refresh and a new release identity. E4 additionally requires real operational use; stronger CI is not a substitute.",
        "",
        "## Result",
        "",
        "The ladder becomes **4×E3 + 1×E1 + 10×E0**. The empty E2 rung is not filled cosmetically; the next E2 should come from a genuinely useful new human experience.",
        "",
    ]
    (ROOT / "docs" / "R4_GIT_VERTICAL_E3.md").write_text("\n".join(lines), encoding="utf-8")
    print("R4 promotion complete: E3=4 E1=1 E0=10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
