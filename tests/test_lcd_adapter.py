from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from knowledge_experiences.adapters import get_source_adapter
from knowledge_experiences.compiler import compile_collection
from knowledge_experiences.models import SourceSpec, ValidationError


class LcdAdapterTest(unittest.TestCase):
    def _index(self) -> list[dict]:
        return [
            {
                "slug": "plan-de-estudios",
                "title": "Plan de estudios",
                "source_url": "https://lcd.exactas.uba.ar/plan-de-estudios/",
                "entity_type": "page",
                "source_id": 395,
                "content_hash": "sha256:" + "a" * 64,
            },
            {
                "slug": "inscripciones-2026",
                "title": "Inscripciones 2026",
                "source_url": "https://lcd.exactas.uba.ar/inscripciones-2026/",
                "entity_type": "post",
                "source_id": 901,
                "content_hash": "sha256:" + "b" * 64,
            },
        ]

    def test_index_maps_page_and_post_without_domain_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "index.json"
            path.write_text(json.dumps(self._index()), encoding="utf-8")
            source = SourceSpec(
                adapter="lcd-title-slug-index",
                path="index.json",
                authority="repo.lcd-uba-knowledgebase",
                release_id="run:test",
            )
            loaded = get_source_adapter(source.adapter).load(source, base_dir=root)
            self.assertEqual([x["item_id"] for x in loaded.items], ["lcd:page:395", "lcd:post:901"])
            self.assertEqual(loaded.items[0]["facets"]["entity_type"], "page")
            self.assertEqual(loaded.items[1]["source_ref"]["object_id"], "post:901")

    def test_invalid_content_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rows = self._index()
            rows[0]["content_hash"] = "not-a-hash"
            (root / "index.json").write_text(json.dumps(rows), encoding="utf-8")
            source = SourceSpec(adapter="lcd-title-slug-index", path="index.json", authority="repo.lcd-uba-knowledgebase")
            with self.assertRaisesRegex(ValidationError, "content_hash"):
                get_source_adapter(source.adapter).load(source, base_dir=root)

    def test_existing_facet_selector_can_create_page_only_subset(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "index.json").write_text(json.dumps(self._index()), encoding="utf-8")
            spec = {
                "schema_id": "knowledge.collection-spec",
                "schema_version": 1,
                "collection_id": "lcd-pages",
                "title": "LCD pages",
                "source": {
                    "adapter": "lcd-title-slug-index",
                    "path": "index.json",
                    "authority": "repo.lcd-uba-knowledgebase",
                    "release_id": "run:test",
                },
                "selection": {"mode": "facets", "facets": {"entity_type": "page"}},
            }
            path = root / "collection.json"
            path.write_text(json.dumps(spec), encoding="utf-8")
            release = compile_collection(path)
            self.assertEqual([x["item_id"] for x in release["items"]], ["lcd:page:395"])


if __name__ == "__main__":
    unittest.main()
