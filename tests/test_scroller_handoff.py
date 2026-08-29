from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from knowledge_experiences.adapters import get_source_adapter
from knowledge_experiences.external_renderers import AbstractScrollerRenderer
from knowledge_experiences.models import ExperienceSpec, SourceSpec, ValidationError


class ScrollerHandoffTest(unittest.TestCase):
    def _record(self, uid: str = "paper:one") -> dict:
        return {
            "schema_id": "paper.review-record",
            "schema_version": 1,
            "paper_uid": uid,
            "paper_id": uid,
            "title": "A governed review record",
            "abstract": "Sanitized abstract.",
            "date": "2026-08-29",
            "year": 2026,
            "venue": "Example Venue",
            "doi": None,
            "arxiv_id": None,
            "repec_id": None,
            "tags": ["proof"],
            "badges": ["has_code"],
            "source_url": "https://example.org/paper",
        }

    def test_paper_review_adapter_maps_only_consumer_surface(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path = root / "review.jsonl"
            source_path.write_text(json.dumps(self._record()) + "\n", encoding="utf-8")
            source = SourceSpec(
                adapter="paper-review-jsonl",
                path="review.jsonl",
                authority="repo.paper-kb",
                release_id="producer-sha",
            )
            loaded = get_source_adapter(source.adapter).load(source, base_dir=root)
            self.assertEqual(len(loaded.items), 1)
            item = loaded.items[0]
            self.assertEqual(item["item_id"], "paper:one")
            self.assertEqual(item["facets"]["year"], 2026)
            self.assertEqual(item["facets"]["venue"], "Example Venue")
            self.assertEqual(item["facets"]["badge"], ["has_code"])
            self.assertEqual(item["source_ref"]["authority"], "repo.paper-kb")

    def test_paper_review_adapter_fails_on_wrong_contract(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path = root / "review.jsonl"
            record = self._record()
            record["schema_id"] = "paper.catalog-record"
            source_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            source = SourceSpec(adapter="paper-review-jsonl", path="review.jsonl", authority="repo.paper-kb")
            with self.assertRaisesRegex(ValidationError, "expected paper.review-record@1"):
                get_source_adapter(source.adapter).load(source, base_dir=root)

    def test_renderer_ref_round_trips_in_experience_spec(self) -> None:
        raw = {
            "schema_id": "knowledge.experience-spec",
            "schema_version": 1,
            "experience_id": "review",
            "collection_spec": "collection.json",
            "renderer": "abstract-scroller",
            "renderer_ref": "6a738edd28d21bf54d6c52943883fee19f4cc033",
        }
        spec = ExperienceSpec.from_dict(raw)
        self.assertEqual(spec.renderer_ref, raw["renderer_ref"])
        self.assertEqual(spec.to_dict()["renderer_ref"], raw["renderer_ref"])

    def test_scroller_refuses_subset_before_external_execution(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path = root / "review.jsonl"
            source_path.write_text(
                json.dumps(self._record("paper:one")) + "\n" + json.dumps(self._record("paper:two")) + "\n",
                encoding="utf-8",
            )
            from knowledge_experiences.canonical import sha256_file

            release = {
                "source": {"adapter": "paper-review-jsonl", "sha256": sha256_file(source_path)},
                "items": [{"item_id": "paper:one"}],
            }
            spec = ExperienceSpec.from_dict({
                "schema_id": "knowledge.experience-spec",
                "schema_version": 1,
                "experience_id": "review",
                "collection_spec": "collection.json",
                "renderer": "abstract-scroller",
                "renderer_ref": "6a738edd28d21bf54d6c52943883fee19f4cc033",
            })
            with self.assertRaisesRegex(ValidationError, "full source membership"):
                AbstractScrollerRenderer().render(
                    collection_release=release,
                    experience_spec=spec,
                    out_dir=root / "out",
                    source_path=source_path,
                )


if __name__ == "__main__":
    unittest.main()
