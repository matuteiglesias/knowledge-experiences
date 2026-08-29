from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from knowledge_experiences.adapters import get_source_adapter
from knowledge_experiences.compiler import compile_collection
from knowledge_experiences.models import SourceSpec, ValidationError


class PaperCatalogAdapterTest(unittest.TestCase):
    def _record(self, *, uid: str, title: str, authors: list[str], year: int = 2026, venue: str = "Example Papers") -> dict:
        return {
            "schema_id": "paper.catalog-record",
            "schema_version": 1,
            "paper_uid": uid,
            "paper_id": uid,
            "title": title,
            "authors": authors,
            "abstract": f"Abstract for {title}",
            "date": None,
            "year": year,
            "venue": venue,
            "doi": None,
            "arxiv_id": None,
            "repec_id": None,
            "tags": ["proof"],
            "source_url": f"https://example.org/{uid}",
        }

    def test_adapter_maps_producer_metadata_to_display_facets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "catalog.jsonl"
            path.write_text(json.dumps(self._record(uid="paper:1", title="One", authors=["Ada Example", "Ben Builder"])) + "\n", encoding="utf-8")
            source = SourceSpec(adapter="paper-catalog-jsonl", path="catalog.jsonl", authority="repo.paper-kb", release_id="producer-sha")
            loaded = get_source_adapter(source.adapter).load(source, base_dir=root)
            self.assertEqual(len(loaded.items), 1)
            item = loaded.items[0]
            self.assertEqual(item["item_id"], "paper:1")
            self.assertEqual(item["contributors"], ["Ada Example", "Ben Builder"])
            self.assertEqual(item["facets"]["author"], ["Ada Example", "Ben Builder"])
            self.assertEqual(item["facets"]["year"], 2026)
            self.assertEqual(item["facets"]["venue"], "Example Papers")
            self.assertEqual(item["source_ref"]["authority"], "repo.paper-kb")

    def test_adapter_rejects_malformed_author_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self._record(uid="paper:1", title="One", authors=["Ada Example"])
            record["authors"] = "Ada Example"
            (root / "catalog.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
            source = SourceSpec(adapter="paper-catalog-jsonl", path="catalog.jsonl", authority="repo.paper-kb")
            with self.assertRaisesRegex(ValidationError, "authors must be an array"):
                get_source_adapter(source.adapter).load(source, base_dir=root)

    def test_facet_selection_creates_low_cost_author_subset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = [
                self._record(uid="paper:a", title="A", authors=["Ada Example"]),
                self._record(uid="paper:b", title="B", authors=["Other Author"]),
                self._record(uid="paper:c", title="C", authors=["Ada Example", "Ben Builder"]),
            ]
            (root / "catalog.jsonl").write_text("".join(json.dumps(row) + "\n" for row in records), encoding="utf-8")
            spec = {
                "schema_id": "knowledge.collection-spec",
                "schema_version": 1,
                "collection_id": "ada-works",
                "title": "Ada Example — Works",
                "source": {"adapter": "paper-catalog-jsonl", "path": "catalog.jsonl", "authority": "repo.paper-kb", "release_id": "producer-sha"},
                "selection": {"mode": "facets", "facets": {"author": "Ada Example"}},
            }
            spec_path = root / "collection.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            release = compile_collection(spec_path)
            self.assertEqual([row["item_id"] for row in release["items"]], ["paper:a", "paper:c"])
            self.assertEqual(release["source"]["release_id"], "producer-sha")

    def test_facet_selection_fails_closed_on_typo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "catalog.jsonl").write_text(json.dumps(self._record(uid="paper:a", title="A", authors=["Ada Example"])) + "\n", encoding="utf-8")
            spec = {
                "schema_id": "knowledge.collection-spec",
                "schema_version": 1,
                "collection_id": "nobody",
                "title": "Nobody",
                "source": {"adapter": "paper-catalog-jsonl", "path": "catalog.jsonl", "authority": "repo.paper-kb"},
                "selection": {"mode": "facets", "facets": {"author": "Typo Author"}},
            }
            spec_path = root / "collection.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "matched no items"):
                compile_collection(spec_path)


if __name__ == "__main__":
    unittest.main()
