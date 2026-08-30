from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from knowledge_experiences.canonical import sha256_file
from knowledge_experiences.compiler import build_experience, compile_collection
from knowledge_experiences.models import CollectionSpec, ValidationError, validate_document


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "fixture"


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): sha256_file(p)
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


class KernelTest(unittest.TestCase):
    def test_contract_files_are_well_formed_and_owned_here(self) -> None:
        expected = {
            "collection.spec.v1.schema.json": "knowledge.collection-spec@1",
            "collection.release.v1.schema.json": "knowledge.collection-release@1",
            "experience.spec.v1.schema.json": "knowledge.experience-spec@1",
            "experience.release.v1.schema.json": "knowledge.experience-release@1",
        }
        for filename, schema_id in expected.items():
            raw = json.loads((ROOT / "contracts" / filename).read_text(encoding="utf-8"))
            self.assertEqual(raw["$id"], schema_id)

    def test_collection_release_is_deterministic(self) -> None:
        spec = FIXTURE / "demo.collection.json"
        a = compile_collection(spec)
        b = compile_collection(spec)
        self.assertEqual(a, b)
        self.assertEqual(a["release_id"], "sha256:" + a["payload_sha256"][:16])
        self.assertEqual([item["item_id"] for item in a["items"]], ["demo:1", "demo:2", "demo:3"])
        validate_document(a)

    def test_experience_build_is_content_stable_across_directories(self) -> None:
        spec = FIXTURE / "demo.experience.json"
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            release_a = build_experience(spec, Path(a))
            release_b = build_experience(spec, Path(b))
            self.assertEqual(release_a, release_b)
            self.assertEqual(tree_hashes(Path(a)), tree_hashes(Path(b)))
            validate_document(release_a)
            html = (Path(a) / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn("Knowledge Experiences — deterministic fixture", html)
            self.assertIn("demo:1", html)
            self.assertIn('"facets":["year","topic"]', html)

    def test_id_selection_is_explicit_and_preserves_requested_membership(self) -> None:
        raw = json.loads((FIXTURE / "demo.collection.json").read_text(encoding="utf-8"))
        raw["selection"] = {"mode": "ids", "item_ids": ["demo:3", "demo:1"]}
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "items.jsonl").write_bytes((FIXTURE / "items.jsonl").read_bytes())
            spec_path = td / "collection.json"
            spec_path.write_text(json.dumps(raw), encoding="utf-8")
            release = compile_collection(spec_path)
            self.assertEqual([item["item_id"] for item in release["items"]], ["demo:1", "demo:3"])

    def test_ordered_ids_preserve_declared_sequence(self) -> None:
        raw = json.loads((FIXTURE / "demo.collection.json").read_text(encoding="utf-8"))
        raw["selection"] = {"mode": "ordered_ids", "item_ids": ["demo:3", "demo:1"]}
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "items.jsonl").write_bytes((FIXTURE / "items.jsonl").read_bytes())
            spec = td / "collection.json"
            spec.write_text(json.dumps(raw), encoding="utf-8")
            release = compile_collection(spec)
            self.assertEqual([x["item_id"] for x in release["items"]], ["demo:3", "demo:1"])

    def test_curated_sort_preserves_release_order(self) -> None:
        collection = json.loads((FIXTURE / "demo.collection.json").read_text(encoding="utf-8"))
        collection["selection"] = {"mode": "ordered_ids", "item_ids": ["demo:3", "demo:1"]}
        experience = json.loads((FIXTURE / "demo.experience.json").read_text(encoding="utf-8"))
        experience["collection_spec"] = "collection.json"
        experience["navigation"] = {"default_sort": "curated"}
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "items.jsonl").write_bytes((FIXTURE / "items.jsonl").read_bytes())
            (td / "collection.json").write_text(json.dumps(collection), encoding="utf-8")
            (td / "experience.json").write_text(json.dumps(experience), encoding="utf-8")
            out = td / "release"
            build_experience(td / "experience.json", out)
            release = json.loads((out / "collection.release.json").read_text(encoding="utf-8"))
            self.assertEqual([x["item_id"] for x in release["items"]], ["demo:3", "demo:1"])
            html = (out / "site/index.html").read_text(encoding="utf-8")
            self.assertIn('"default_sort":"curated"', html)
            self.assertLess(html.index("demo:3"), html.index("demo:1"))

    def test_missing_selected_id_fails_closed(self) -> None:
        raw = json.loads((FIXTURE / "demo.collection.json").read_text(encoding="utf-8"))
        raw["selection"] = {"mode": "ids", "item_ids": ["missing"]}
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "items.jsonl").write_bytes((FIXTURE / "items.jsonl").read_bytes())
            spec_path = td / "collection.json"
            spec_path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "missing item_ids"):
                compile_collection(spec_path)

    def test_unknown_fields_fail_closed(self) -> None:
        raw = json.loads((FIXTURE / "demo.collection.json").read_text(encoding="utf-8"))
        raw["magic_query"] = "author=someone"
        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            CollectionSpec.from_dict(raw)


if __name__ == "__main__":
    unittest.main()
