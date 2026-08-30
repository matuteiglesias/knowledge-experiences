#!/usr/bin/env python3
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
        m=re.search(r"(?m)^slug:\s*/?([^\s]+)\s*$",path.read_text(errors="replace"))
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
        run("kx","doctor",str(trail/"snapshot.experience.json")); run("kx","build",str(trail/"snapshot.experience.json"),"--out",str(trail/"release"))
        for rel in ["collection.release.json","experience.release.json","site/index.html"]:
            if sha(trail/"release"/rel)!=sha(accepted/"release"/rel): raise SystemExit(f"{rel} mismatch")
    print(json.dumps({"case":"economic-complexity-reading-path","source_commit":COMMIT,"ordered_steps":6,"result":"pass"},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
