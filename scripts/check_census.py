#!/usr/bin/env python3
"""Fail-closed structural checks for the V1.5 experience census."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "docs" / "experience-census.v1.json"

MATURITY = {"E0", "E1", "E2", "E3", "E4"}
ENGINEERING = {
    "proven_live",
    "proven_sanitized",
    "proven_contract_check",
    "blocked_producer_metadata",
    "blocked_capability",
    "design_ready",
    "existing_vertical",
    "declared",
}
REQUIRED = {
    "id", "experience_id", "name", "composition_maturity", "engineering_status",
    "existing_surface", "source_authorities", "code_pins", "exact_source_release",
    "collection_release", "renderer_profile", "rendered_artifact", "cross_repo_proof",
    "operational_evidence", "capabilities_reused", "incremental_work", "blocker",
    "observed_friction", "v2_candidate", "engineering_evidence", "evidence_boundary",
    "next_real_action",
}


def fail(message: str) -> None:
    raise SystemExit(f"experience census invalid: {message}")


def main() -> int:
    payload = json.loads(CENSUS.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        fail("schema_version must be 1")
    rows = payload.get("experiences")
    if not isinstance(rows, list) or len(rows) != 15:
        fail("exactly 15 experience records are required")
    ids = [row.get("id") for row in rows if isinstance(row, dict)]
    if ids != list(range(1, 16)):
        fail(f"ids must be ordered 1..15, got {ids}")
    names: set[str] = set()
    slugs: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            fail("every experience must be an object")
        missing = REQUIRED - set(row)
        extra = set(row) - REQUIRED
        if missing or extra:
            fail(f"row {row.get('id')}: missing={sorted(missing)} extra={sorted(extra)}")
        if row["composition_maturity"] not in MATURITY:
            fail(f"row {row['id']}: invalid maturity")
        if row["engineering_status"] not in ENGINEERING:
            fail(f"row {row['id']}: invalid engineering_status")
        if not isinstance(row["source_authorities"], list) or not row["source_authorities"]:
            fail(f"row {row['id']}: source_authorities must be non-empty")
        if not isinstance(row["engineering_evidence"], list):
            fail(f"row {row['id']}: engineering_evidence must be an array")
        for field in ("experience_id", "name", "renderer_profile", "incremental_work", "blocker", "observed_friction", "evidence_boundary", "next_real_action"):
            if not isinstance(row[field], str) or not row[field].strip():
                fail(f"row {row['id']}: {field} must be non-empty")
        if row["name"] in names or row["experience_id"] in slugs:
            fail(f"row {row['id']}: duplicate name or experience_id")
        names.add(row["name"])
        slugs.add(row["experience_id"])

        level = int(row["composition_maturity"][1])
        if level >= 1 and (not row["exact_source_release"] or not row["collection_release"]):
            fail(f"row {row['id']}: E1+ requires exact_source_release and collection_release")
        if level >= 2 and not row["rendered_artifact"]:
            fail(f"row {row['id']}: E2+ requires rendered_artifact")
        if level >= 3 and not row["cross_repo_proof"]:
            fail(f"row {row['id']}: E3+ requires cross_repo_proof")
        if level >= 4 and not row["operational_evidence"]:
            fail(f"row {row['id']}: E4 requires operational_evidence")

        if row["engineering_status"] in {"proven_live", "proven_sanitized", "proven_contract_check", "existing_vertical"} and not row["engineering_evidence"]:
            fail(f"row {row['id']}: engineering status requires evidence")

    counts = Counter(row["composition_maturity"] for row in rows)
    statuses = Counter(row["engineering_status"] for row in rows)
    print("experience census: OK")
    print("maturity:", dict(sorted(counts.items())))
    print("engineering:", dict(sorted(statuses.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
