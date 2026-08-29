from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .canonical import sha256_file, write_canonical_json
from .models import ExperienceSpec, ValidationError


_SCROLLER_REPO_MARKER = "repo.abstract-scroller"
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def _run_checked(cmd: list[str], *, cwd: Path, label: str) -> str:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise ValidationError(f"{label} failed ({proc.returncode}): {detail}")
    return (proc.stdout or "").strip()


class AbstractScrollerRenderer:
    """Bounded handoff to the real Abstract Scroller snapshot compiler.

    The renderer consumes the original producer-owned paper.review-record@1
    JSONL. Knowledge Experiences never reconstructs that domain contract from
    its generic item projection.
    """

    name = "abstract-scroller"

    def render(
        self,
        *,
        collection_release: dict[str, Any],
        experience_spec: ExperienceSpec,
        out_dir: Path,
        source_path: Path,
    ) -> list[Path]:
        source = collection_release.get("source") or {}
        if source.get("adapter") != "paper-review-jsonl":
            raise ValidationError(
                "abstract-scroller currently requires source.adapter='paper-review-jsonl'"
            )
        source_path = Path(source_path).resolve()
        if not source_path.is_file():
            raise ValidationError(f"abstract-scroller source file does not exist: {source_path}")
        if sha256_file(source_path) != source.get("sha256"):
            raise ValidationError("abstract-scroller source bytes changed after collection compilation")

        nonempty_lines = [line for line in source_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(nonempty_lines) != len(collection_release.get("items", [])):
            raise ValidationError(
                "abstract-scroller handoff currently requires full source membership; "
                "subset review projection remains producer-owned"
            )

        renderer_ref = experience_spec.renderer_ref
        if renderer_ref is None or not _COMMIT_RE.fullmatch(renderer_ref):
            raise ValidationError("abstract-scroller requires renderer_ref as an exact 40-character commit SHA")

        root_raw = os.environ.get("KX_ABSTRACT_SCROLLER_ROOT")
        if not root_raw:
            raise ValidationError("set KX_ABSTRACT_SCROLLER_ROOT to the pinned Abstract Scroller checkout")
        root = Path(root_raw).expanduser().resolve()
        system_path = root / "SYSTEM.yaml"
        if not system_path.is_file() or _SCROLLER_REPO_MARKER not in system_path.read_text(encoding="utf-8"):
            raise ValidationError("KX_ABSTRACT_SCROLLER_ROOT is not an Abstract Scroller checkout")

        actual_ref = _run_checked(["git", "rev-parse", "HEAD"], cwd=root, label="Abstract Scroller identity check")
        if actual_ref != renderer_ref:
            raise ValidationError(
                f"Abstract Scroller checkout mismatch: expected {renderer_ref}, got {actual_ref}"
            )

        out_dir = Path(out_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        _run_checked(
            [
                sys.executable,
                "-m",
                "backend.jobs.mvp_snapshot",
                "--input",
                str(source_path),
                "--format",
                "paper_review_record_jsonl",
                "--out",
                str(out_dir),
            ],
            cwd=root,
            label="Abstract Scroller snapshot compilation",
        )
        _run_checked(
            [sys.executable, "-m", "backend.publish.manifest", "--validate", str(out_dir)],
            cwd=root,
            label="Abstract Scroller manifest validation",
        )

        provenance = {
            "renderer": "repo.abstract-scroller",
            "renderer_commit": actual_ref,
            "input_contract": "paper.review-record@1",
            "input_sha256": source["sha256"],
            "input_authority": source.get("authority"),
            "input_release_id": source.get("release_id"),
        }
        write_canonical_json(out_dir / "renderer.provenance.json", provenance)
        return [p for p in sorted(out_dir.rglob("*")) if p.is_file()]
