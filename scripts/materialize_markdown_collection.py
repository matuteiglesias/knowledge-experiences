#!/usr/bin/env python3
"""Materialize a bounded Git-backed Markdown metadata collection for real-use proofs.

This helper does not define document-domain semantics. It snapshots only explicit
metadata and stable source pointers from an exact Git checkout into the existing
Knowledge Experiences generic JSONL display projection. Optional path filtering
is an explicit source-boundary rule recorded in the receipt; it does not infer
producer taxonomy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


EXCLUDED_PARTS = {"private", "templates", ".obsidian"}


def parse_scalar(raw: str):
    raw = raw.strip()
    if not raw:
        return ""
    low = raw.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"\'') for part in inner.split(",") if part.strip()]
    return raw


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    out = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"title", "date", "created", "publish", "draft", "tags", "status", "research_status"}:
            out[key] = parse_scalar(value)
    return out


def first_heading(text: str) -> str | None:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return re.sub(r"[*_`]", "", match.group(1)).strip()
    return None


def tracked_markdown(repo_root: Path, scope_root: str, path_regex: str | None = None) -> list[Path]:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", scope_root],
        check=True,
        text=True,
        capture_output=True,
    )
    matcher = re.compile(path_regex) if path_regex else None
    paths = []
    for raw in proc.stdout.splitlines():
        path = Path(raw)
        if path.suffix.lower() not in {".md", ".mdx"}:
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if matcher is not None and matcher.fullmatch(path.as_posix()) is None:
            continue
        paths.append(path)
    return sorted(paths, key=lambda p: p.as_posix())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--source-repo", required=True)
    parser.add_argument("--authority", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--scope-root", required=True)
    parser.add_argument("--path-regex", help="optional full-match regex over repo-relative paths")
    parser.add_argument("--mode", choices=["all-markdown", "explicit-publish"], required=True)
    parser.add_argument("--collection-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--kind", default="document")
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    actual = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if actual != args.commit:
        raise SystemExit(f"checkout mismatch: expected {args.commit}, got {actual}")

    records = []
    excluded_unpublished = 0
    for rel in tracked_markdown(repo_root, args.scope_root, args.path_regex):
        text = (repo_root / rel).read_text(encoding="utf-8")
        meta = frontmatter(text)
        if args.mode == "explicit-publish":
            if meta.get("publish") is not True or meta.get("draft") is True:
                excluded_unpublished += 1
                continue

        title = str(meta.get("title") or first_heading(text) or rel.stem).strip()
        url = f"https://github.com/{args.source_repo}/blob/{args.commit}/{rel.as_posix()}"
        facets = {
            "source_path": rel.as_posix(),
            "top_level": rel.parts[1] if len(rel.parts) > 1 else rel.parts[0],
        }
        explicit_status = meta.get("status") or meta.get("research_status")
        if isinstance(explicit_status, str) and explicit_status.strip():
            facets["upstream_status"] = explicit_status.strip()

        record = {
            "item_id": f"{args.authority}:{rel.as_posix()}",
            "kind": args.kind,
            "title": title,
            "contributors": [],
            "tags": meta.get("tags") if isinstance(meta.get("tags"), list) else [],
            "facets": facets,
            "canonical_url": url,
            "source_ref": {
                "authority": args.authority,
                "object_id": rel.as_posix(),
                "url": url,
            },
        }
        date = meta.get("date") or meta.get("created")
        if isinstance(date, str) and date.strip():
            record["date"] = date.strip()
        records.append(record)

    if not records:
        raise SystemExit(f"no records selected for {args.collection_id}; refusing empty E1 release")

    out_dir = Path(args.out_dir)
    source_dir = out_dir / "source"
    release_dir = out_dir / "release"
    source_dir.mkdir(parents=True, exist_ok=True)
    release_dir.mkdir(parents=True, exist_ok=True)
    items_path = source_dir / "items.jsonl"
    with items_path.open("w", encoding="utf-8") as handle:
        for record in sorted(records, key=lambda row: row["item_id"]):
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n")

    spec = {
        "schema_id": "knowledge.collection-spec",
        "schema_version": 1,
        "collection_id": args.collection_id,
        "title": args.title,
        "description": args.description,
        "source": {
            "adapter": "jsonl",
            "path": "source/items.jsonl",
            "authority": args.authority,
            "release_id": f"git:{args.commit}",
        },
        "selection": {"mode": "all"},
    }
    (out_dir / "collection.json").write_text(
        json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    receipt = {
        "schema_id": "knowledge.git-markdown-source-receipt",
        "schema_version": 1,
        "source_repo": args.source_repo,
        "source_authority": args.authority,
        "source_commit": args.commit,
        "scope_root": args.scope_root,
        "selection_mode": args.mode,
        "record_count": len(records),
        "excluded_unpublished_count": excluded_unpublished,
        "body_copy_policy": "metadata and exact source pointers only; Markdown bodies remain producer-owned",
        "source_index_sha256": sha256_file(items_path),
    }
    if args.path_regex:
        receipt["path_regex"] = args.path_regex
    (source_dir / "source-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
