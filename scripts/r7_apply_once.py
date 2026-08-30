#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THESIS_COMMIT = "7265018750db0f96b69efd4048aedad06ad803fc"
THESIS_ROOT = Path("/tmp/thesis-r7")
TRAIL_ROOT = ROOT / "experiences/real/economic-complexity-reading-path"
PARENT_ROOT = ROOT / "experiences/real/economics-of-aggregation-programme"
TARGETS = [
    "observations-lq-problem",
    "convenient-framework-location-quotient",
    "characterization-of-plq",
    "probabilistic-location-quotient",
    "Location-Quotients/empirical-distributions",
    "Location-Quotients/conclusion-location-quotients",
]


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(list(args), cwd=cwd, check=True)


def patch(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"{path}: expected one patch target, found {text.count(old)}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_trail(thesis: Path) -> tuple[list[str], list[str]]:
    intro = (thesis / "docs/intro.md").read_text(encoding="utf-8")
    start = intro.find("### Trail B —")
    end = intro.find("### Trail C —", start)
    if start < 0 or end < 0:
        raise SystemExit("producer Trail B section boundaries not found")
    section = intro[start:end]
    positions = [section.find(f"(./{target})") for target in TARGETS]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        raise SystemExit(f"literal Trail B links missing/reordered inside Trail B section: {positions}")

    keys = [target.rsplit("/", 1)[-1] for target in TARGETS]
    mapping: dict[str, str] = {}
    for path in sorted((thesis / "docs").rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"(?m)^slug:\s*/?([^\s]+)\s*$", text)
        if match and match.group(1) in keys:
            key = match.group(1)
            if key in mapping:
                raise SystemExit(f"duplicate producer slug: {key}")
            mapping[key] = path.relative_to(thesis).as_posix()
    missing = [key for key in keys if key not in mapping]
    if missing:
        raise SystemExit(f"producer Trail B targets do not resolve to exact Markdown files: {missing}")
    return keys, [mapping[key] for key in keys]


def implement_core() -> None:
    patch(
        "src/knowledge_experiences/models.py",
        '        if mode not in {"all", "ids", "facets"}:\n            raise ValidationError("selection.mode must be \'all\', \'ids\', or \'facets\'")',
        '        if mode not in {"all", "ids", "ordered_ids", "facets"}:\n            raise ValidationError("selection.mode must be \'all\', \'ids\', \'ordered_ids\', or \'facets\'")',
    )
    patch(
        "src/knowledge_experiences/models.py",
        '        if mode == "ids" and not ids:\n            raise ValidationError("selection.item_ids must be non-empty when mode=\'ids\'")\n        if mode != "ids" and ids:\n            raise ValidationError("selection.item_ids is only valid when mode=\'ids\'")',
        '        if mode in {"ids", "ordered_ids"} and not ids:\n            raise ValidationError("selection.item_ids must be non-empty when mode is \'ids\' or \'ordered_ids\'")\n        if mode not in {"ids", "ordered_ids"} and ids:\n            raise ValidationError("selection.item_ids is only valid when mode is \'ids\' or \'ordered_ids\'")',
    )
    patch(
        "src/knowledge_experiences/models.py",
        '        if self.mode == "ids":\n            out["item_ids"] = list(self.item_ids)',
        '        if self.mode in {"ids", "ordered_ids"}:\n            out["item_ids"] = list(self.item_ids)',
    )
    patch(
        "src/knowledge_experiences/models.py",
        '        if default_sort not in {"title", "date", "source"}:\n            raise ValidationError("navigation.default_sort must be title, date, or source")',
        '        if default_sort not in {"title", "date", "source", "curated"}:\n            raise ValidationError("navigation.default_sort must be title, date, source, or curated")',
    )
    patch(
        "src/knowledge_experiences/compiler.py",
        '    elif spec.selection.mode == "ids":',
        '    elif spec.selection.mode in {"ids", "ordered_ids"}:',
    )
    patch(
        "src/knowledge_experiences/compiler.py",
        '    return sorted(selected, key=lambda item: item["item_id"])',
        '    if spec.selection.mode == "ordered_ids":\n        return selected\n    return sorted(selected, key=lambda item: item["item_id"])',
    )
    patch(
        "src/knowledge_experiences/renderers.py",
        '<option value="source">Source</option>\n</select>',
        '<option value="source">Source</option>\n<option value="curated">Curated order</option>\n</select>',
    )
    patch(
        "src/knowledge_experiences/renderers.py",
        'function sorted(items){\n  return [...items].sort((a,b)=>{',
        'function sorted(items){\n  if(state.sort==="curated") return [...items];\n  return [...items].sort((a,b)=>{',
    )

    p = ROOT / "contracts/collection.spec.v1.schema.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["properties"]["selection"]["properties"]["mode"]["enum"] = ["all", "ids", "ordered_ids", "facets"]
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    p = ROOT / "contracts/experience.spec.v1.schema.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["properties"]["navigation"]["properties"]["default_sort"]["enum"] = ["title", "date", "source", "curated"]
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    p = ROOT / "tests/test_kernel.py"
    text = p.read_text(encoding="utf-8")
    marker = "    def test_missing_selected_id_fails_closed(self) -> None:\n"
    addition = '''    def test_ordered_ids_preserve_declared_sequence(self) -> None:\n        raw = json.loads((FIXTURE / "demo.collection.json").read_text(encoding="utf-8"))\n        raw["selection"] = {"mode": "ordered_ids", "item_ids": ["demo:3", "demo:1"]}\n        with tempfile.TemporaryDirectory() as td:\n            td = Path(td)\n            (td / "items.jsonl").write_bytes((FIXTURE / "items.jsonl").read_bytes())\n            spec = td / "collection.json"\n            spec.write_text(json.dumps(raw), encoding="utf-8")\n            release = compile_collection(spec)\n            self.assertEqual([x["item_id"] for x in release["items"]], ["demo:3", "demo:1"])\n\n    def test_curated_sort_preserves_release_order(self) -> None:\n        collection = json.loads((FIXTURE / "demo.collection.json").read_text(encoding="utf-8"))\n        collection["selection"] = {"mode": "ordered_ids", "item_ids": ["demo:3", "demo:1"]}\n        experience = json.loads((FIXTURE / "demo.experience.json").read_text(encoding="utf-8"))\n        experience["collection_spec"] = "collection.json"\n        experience["navigation"] = {"default_sort": "curated"}\n        with tempfile.TemporaryDirectory() as td:\n            td = Path(td)\n            (td / "items.jsonl").write_bytes((FIXTURE / "items.jsonl").read_bytes())\n            (td / "collection.json").write_text(json.dumps(collection), encoding="utf-8")\n            (td / "experience.json").write_text(json.dumps(experience), encoding="utf-8")\n            out = td / "release"\n            build_experience(td / "experience.json", out)\n            release = json.loads((out / "collection.release.json").read_text(encoding="utf-8"))\n            self.assertEqual([x["item_id"] for x in release["items"]], ["demo:3", "demo:1"])\n            html = (out / "site/index.html").read_text(encoding="utf-8")\n            self.assertIn('"default_sort":"curated"', html)\n            self.assertLess(html.index("demo:3"), html.index("demo:1"))\n\n'''
    if marker not in text:
        raise SystemExit("test insertion marker missing")
    p.write_text(text.replace(marker, addition + marker), encoding="utf-8")


def materialize() -> tuple[dict, dict, dict]:
    if THESIS_ROOT.exists():
        shutil.rmtree(THESIS_ROOT)
    run("git", "clone", "-q", "https://github.com/matuteiglesias/thesis.git", str(THESIS_ROOT))
    run("git", "-C", str(THESIS_ROOT), "checkout", "-q", THESIS_COMMIT)
    actual = subprocess.run(["git", "-C", str(THESIS_ROOT), "rev-parse", "HEAD"], check=True, text=True, capture_output=True).stdout.strip()
    if actual != THESIS_COMMIT:
        raise SystemExit(f"thesis checkout mismatch: {actual}")

    with tempfile.TemporaryDirectory(prefix="kx-r7-parent-") as td_raw:
        parent = Path(td_raw) / "economics-of-aggregation-programme"
        run(
            "python", str(ROOT / "scripts/materialize_markdown_collection.py"),
            "--repo-root", str(THESIS_ROOT), "--source-repo", "matuteiglesias/thesis",
            "--authority", "repo.thesis", "--commit", THESIS_COMMIT, "--scope-root", "docs",
            "--mode", "all-markdown", "--collection-id", "economics-of-aggregation-programme",
            "--title", "Economics of Aggregation programme — exact document index",
            "--description", "Metadata-only index of exact versioned research-programme documents; repo.thesis retains content and status authority.",
            "--kind", "research-document", "--out-dir", str(parent),
        )
        if sha(parent / "source/items.jsonl") != sha(PARENT_ROOT / "source/items.jsonl"):
            raise SystemExit("exact Thesis 89-document source projection no longer matches accepted parent")
        rows = [json.loads(line) for line in (parent / "source/items.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]

    _, paths = resolve_trail(THESIS_ROOT)
    by_path = {row["source_ref"]["object_id"]: row for row in rows}
    missing = [path for path in paths if path not in by_path]
    if missing:
        raise SystemExit(f"Trail B files missing from accepted parent projection: {missing}")
    ids = [by_path[path]["item_id"] for path in paths]

    TRAIL_ROOT.mkdir(parents=True, exist_ok=True)
    collection = {
        "schema_id": "knowledge.collection-spec", "schema_version": 1,
        "collection_id": "economic-complexity-reading-path",
        "title": "Economic complexity — location-quotient problem reading path",
        "description": "Six-step producer-curated Trail B from the exact Thesis programme; editorial sequence is collection meaning.",
        "source": {"adapter": "jsonl", "path": "../economics-of-aggregation-programme/source/items.jsonl", "authority": "repo.thesis", "release_id": f"git:{THESIS_COMMIT}"},
        "selection": {"mode": "ordered_ids", "item_ids": ids},
    }
    experience = {
        "schema_id": "knowledge.experience-spec", "schema_version": 1,
        "experience_id": "economic-complexity-reading-path",
        "title": "Understand the location-quotient problem",
        "collection_spec": "collection.json", "renderer": "static-navigator", "visibility": "public",
        "capabilities": {"search": True, "facets": []}, "navigation": {"default_sort": "curated"},
    }
    receipt = {
        "schema_id": "knowledge.curated-trail-source-receipt", "schema_version": 1,
        "producer": "repo.thesis", "producer_git_commit": THESIS_COMMIT,
        "producer_authority_document": "docs/intro.md#Trail-B",
        "trail_label": "Why is a location quotient not on a common scale?",
        "ordered_link_targets": TARGETS, "ordered_source_paths": paths, "ordered_item_ids": ids,
        "source_projection": "experiences/real/economics-of-aggregation-programme/source/items.jsonl",
        "ordering_semantics": "producer editorial sequence; not alphabetical or item-id sort",
    }
    (TRAIL_ROOT / "collection.json").write_text(json.dumps(collection, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (TRAIL_ROOT / "snapshot.experience.json").write_text(json.dumps(experience, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (TRAIL_ROOT / "source-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if (TRAIL_ROOT / "release").exists():
        shutil.rmtree(TRAIL_ROOT / "release")
    run("kx", "doctor", str(TRAIL_ROOT / "snapshot.experience.json"), cwd=ROOT)
    run("kx", "build", str(TRAIL_ROOT / "snapshot.experience.json"), "--out", str(TRAIL_ROOT / "release"), cwd=ROOT)

    collection_release = json.loads((TRAIL_ROOT / "release/collection.release.json").read_text(encoding="utf-8"))
    experience_release = json.loads((TRAIL_ROOT / "release/experience.release.json").read_text(encoding="utf-8"))
    actual_ids = [row["item_id"] for row in collection_release["items"]]
    if actual_ids != ids:
        raise SystemExit(f"CollectionRelease lost curated order: {actual_ids}")
    html_path = TRAIL_ROOT / "release/site/index.html"
    html = html_path.read_text(encoding="utf-8")
    positions = [html.find(item_id) for item_id in ids]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        raise SystemExit("rendered payload lost curated order")
    proof = {
        "schema_id": "knowledge.e3-cross-repo-proof", "schema_version": 1,
        "proof": "producer-curated-order-to-frozen-experience",
        "source_repo": "matuteiglesias/thesis", "source_commit": THESIS_COMMIT,
        "producer_authority_document": "docs/intro.md#Trail-B", "ordered_item_ids": ids,
        "collection_release_id": collection_release["release_id"],
        "experience_release_id": experience_release["release_id"],
        "rendered_artifact_sha256": sha(html_path), "result": "pass",
    }
    (TRAIL_ROOT / "e3-proof.json").write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt, collection_release, proof


def write_persistent_proof() -> None:
    content = '''#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COMMIT="7265018750db0f96b69efd4048aedad06ad803fc"
TARGETS=["observations-lq-problem","convenient-framework-location-quotient","characterization-of-plq","probabilistic-location-quotient","Location-Quotients/empirical-distributions","Location-Quotients/conclusion-location-quotients"]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(*a): subprocess.run(list(a),check=True)
def resolve(root):
    intro=(root/"docs/intro.md").read_text(); start=intro.find("### Trail B —"); end=intro.find("### Trail C —",start)
    if start<0 or end<0: raise SystemExit("Trail B boundaries missing")
    section=intro[start:end]; pos=[section.find(f"(./{t})") for t in TARGETS]
    if any(p<0 for p in pos) or pos!=sorted(pos): raise SystemExit("Trail B links missing/reordered")
    keys=[t.rsplit("/",1)[-1] for t in TARGETS]; mapping={}
    for path in sorted((root/"docs").rglob("*.md")):
        m=re.search(r"(?m)^slug:\\s*/?([^\\s]+)\\s*$",path.read_text(errors="replace"))
        if m and m.group(1) in keys:
            if m.group(1) in mapping: raise SystemExit(f"duplicate slug {m.group(1)}")
            mapping[m.group(1)]=path.relative_to(root).as_posix()
    missing=[k for k in keys if k not in mapping]
    if missing: raise SystemExit(f"unresolved Trail B targets {missing}")
    return [mapping[k] for k in keys]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--thesis-root",required=True); a=ap.parse_args(); source=Path(a.thesis_root).resolve()
    actual=subprocess.run(["git","-C",str(source),"rev-parse","HEAD"],check=True,text=True,capture_output=True).stdout.strip()
    if actual!=COMMIT: raise SystemExit(f"thesis checkout mismatch {actual}")
    paths=resolve(source); accepted_parent=ROOT/"experiences/real/economics-of-aggregation-programme"; accepted=ROOT/"experiences/real/economic-complexity-reading-path"; receipt=json.loads((accepted/"source-receipt.json").read_text())
    if receipt["ordered_source_paths"]!=paths: raise SystemExit("accepted source paths drifted from Trail B")
    with tempfile.TemporaryDirectory(prefix="kx-r7-proof-") as td0:
        td=Path(td0); parent=td/"economics-of-aggregation-programme"
        run("python",str(ROOT/"scripts/materialize_markdown_collection.py"),"--repo-root",str(source),"--source-repo","matuteiglesias/thesis","--authority","repo.thesis","--commit",COMMIT,"--scope-root","docs","--mode","all-markdown","--collection-id","economics-of-aggregation-programme","--title","Economics of Aggregation programme — exact document index","--description","Metadata-only index of exact versioned research-programme documents; repo.thesis retains content and status authority.","--kind","research-document","--out-dir",str(parent))
        if sha(parent/"source/items.jsonl")!=sha(accepted_parent/"source/items.jsonl"): raise SystemExit("parent projection mismatch")
        rows=[json.loads(x) for x in (parent/"source/items.jsonl").read_text().splitlines() if x.strip()]; by={x["source_ref"]["object_id"]:x["item_id"] for x in rows}; ids=[by[p] for p in paths]
        spec=json.loads((accepted/"collection.json").read_text());
        if spec["selection"]!={"mode":"ordered_ids","item_ids":ids}: raise SystemExit("ordered selection mismatch")
        trail=td/"trail"; trail.mkdir(); shutil.copy2(accepted/"collection.json",trail/"collection.json"); shutil.copy2(accepted/"snapshot.experience.json",trail/"snapshot.experience.json")
        # Preserve relative sibling source layout used by the accepted spec.
        sibling=td/"economics-of-aggregation-programme/source"; sibling.mkdir(parents=True); shutil.copy2(parent/"source/items.jsonl",sibling/"items.jsonl")
        run("kx","doctor",str(trail/"snapshot.experience.json")); run("kx","build",str(trail/"snapshot.experience.json"),"--out",str(trail/"release"))
        for rel in ["collection.release.json","experience.release.json","site/index.html"]:
            if sha(trail/"release"/rel)!=sha(accepted/"release"/rel): raise SystemExit(f"{rel} mismatch")
    print(json.dumps({"case":"economic-complexity-reading-path","source_commit":COMMIT,"ordered_steps":6,"result":"pass"},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
'''
    path = ROOT / "scripts/prove_ordered_thesis_trail.py"
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def promote(receipt: dict, collection_release: dict, proof: dict) -> None:
    census_path = ROOT / "docs/experience-census.v1.json"
    census = json.loads(census_path.read_text(encoding="utf-8"))
    row = next(row for row in census["experiences"] if row["id"] == 5)
    if row["experience_id"] != "economic-complexity-reading-path" or row["composition_maturity"] != "E0":
        raise SystemExit("R7 expects census #5 at its accepted E0 frontier")
    experience_release = json.loads((TRAIL_ROOT / "release/experience.release.json").read_text(encoding="utf-8"))
    row.update({
        "composition_maturity": "E3", "engineering_status": "proven_real_source_seam",
        "existing_surface": "repo.thesis producer-curated Trail B in docs/intro.md",
        "source_authorities": ["repo.thesis", "human-curation"],
        "code_pins": {"repo.thesis": THESIS_COMMIT},
        "exact_source_release": f"git:{THESIS_COMMIT};authority:docs/intro.md#Trail-B",
        "collection_release": f"experiences/real/economic-complexity-reading-path/release/collection.release.json#{collection_release['release_id']}",
        "renderer_profile": "curated-static-navigator",
        "rendered_artifact": "experiences/real/economic-complexity-reading-path/release/site/index.html",
        "cross_repo_proof": "experiences/real/economic-complexity-reading-path/e3-proof.json + scripts/prove_ordered_thesis_trail.py",
        "operational_evidence": None,
        "capabilities_reused": ["git-markdown-metadata-projection", "ordered-ids-selection", "curated-order-rendering", "static-navigator", "exact-git-cross-repo-proof"],
        "incremental_work": "small V2 capability only: ordered_ids plus curated navigation",
        "blocker": "none for this six-step trail; grouping remains absent until a real grouped case requires it",
        "observed_friction": "V1 ids selection and renderer sorting destroyed producer editorial order; real Thesis Trail B made order semantic",
        "v2_candidate": None,
        "engineering_evidence": [
            "exact producer Trail B has six ordered links",
            f"ordered CollectionRelease {collection_release['release_id']} preserves all six resolved IDs",
            f"ExperienceRelease {experience_release['release_id']} preserves curated order",
            f"persistent exact-source proof pins final artifact {proof['rendered_artifact_sha256']}",
        ],
        "evidence_boundary": "E3 proves the exact six-step Thesis Trail B through ordered selection; no grouping, recurring use, deployment, or E4 operation is claimed",
        "next_real_action": "use/circulate the ordered trail or test a genuinely grouped course source; add groups only if ordered_ids is insufficient",
    })
    counts = Counter(row["composition_maturity"] for row in census["experiences"])
    expected = Counter({"E4": 1, "E3": 5, "E1": 1, "E0": 9})
    if counts != expected:
        raise SystemExit(f"unexpected R7 maturity distribution: {counts}")
    census_path.write_text(json.dumps(census, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    p = ROOT / "SYSTEM.yaml"
    text = p.read_text(encoding="utf-8")
    old = "    E4: 1\n    E3: 4\n    E1: 1\n    E0: 10\n"
    if old not in text:
        raise SystemExit("SYSTEM maturity snapshot changed unexpectedly")
    text = text.replace(old, "    E4: 1\n    E3: 5\n    E1: 1\n    E0: 9\n")
    text = text.replace("    - ordered-groups-and-reading-trails\n", "    - grouped-reading-semantics-if-real-demand\n")
    text = text.replace("  phase: first-operational-experience\n  next_gate: paper-real-corpus-or-independent-operational-use\n", "  phase: first-operational-plus-evidence-pulled-v2\n  next_gate: paper-real-corpus-or-real-grouped-or-multi-source-pressure\n")
    p.write_text(text, encoding="utf-8")

    p = ROOT / "docs/EXPERIENCE_CENSUS.md"
    text = p.read_text(encoding="utf-8")
    text, n1 = re.subn(r"\*\*16 governed experiences:[^\n]+\*\*[^\n]*", "**16 governed experiences: 1 is E4, 5 are E3, 1 is E1, and 9 remain E0.** R7 promotes the previously blocked economic-complexity reading path after a real producer-curated trail proved sequence is semantic.", text, count=1)
    text, n2 = re.subn(r"\| 5 \| Economic-complexity reading path \| \*\*E0\*\* \| blocked_capability \|[^\n]*", f"| 5 | Economic-complexity reading path | **E3** | proven_real_source_seam | six exact Thesis Trail B steps → `{experience_release['release_id']}` with producer order preserved |", text, count=1)
    if n1 != 1 or n2 != 1:
        raise SystemExit(f"human census patch failed: headline={n1}, row5={n2}")
    text += "\n## R7 interpretation\n\nThe first V2 capability was earned by a real representational failure. `repo.thesis` already declares Trail B as a six-step editorial sequence; V1 could select the IDs but canonicalized and re-sorted them, erasing the reading path. R7 adds only `ordered_ids` plus `curated` navigation. Grouping remains deliberately absent. No second E4 is claimed without a second independent operational event.\n"
    p.write_text(text, encoding="utf-8")

    p = ROOT / "docs/BUILD_BUNDLE.md"
    p.write_text(p.read_text(encoding="utf-8") + "\n## R6–R7 frontier extension\n\n- **R6 — first E4:** LCD institutional browsing completed a second governed live refresh, source comparison, deterministic rebuild and downstream validation; its dependent subset remained E3.\n- **R7 — first evidence-pulled V2:** a real six-step Thesis Trail B proved curator order is semantic. KX added only `ordered_ids` selection and `curated` navigation. Group/module semantics remain parked.\n\nCurrent live census after R7: **1×E4 + 5×E3 + 1×E1 + 9×E0**.\n", encoding="utf-8")


def main() -> int:
    implement_core()
    run("python", "-m", "pip", "install", "--no-deps", "-e", ".", cwd=ROOT)
    receipt, collection_release, proof = materialize()
    write_persistent_proof()
    run("python", "-m", "py_compile", str(ROOT / "scripts/prove_ordered_thesis_trail.py"), cwd=ROOT)
    run("python", str(ROOT / "scripts/prove_ordered_thesis_trail.py"), "--thesis-root", str(THESIS_ROOT), cwd=ROOT)
    promote(receipt, collection_release, proof)
    print(json.dumps({"r7": "ready", "collection_release": collection_release["release_id"], "artifact_sha256": proof["rendered_artifact_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
