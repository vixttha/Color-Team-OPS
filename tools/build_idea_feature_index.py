#!/usr/bin/env python3
"""Optional developer-only deterministic registry-view generator; never a plugin runtime dependency."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(kind):
    docs = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT/kind/"records").glob("*.json"))]
    return docs

def build():
    ideas=load("ideas")
    rows=["# Color-Team-OPS — Idea Index (generated)","","> Generated from `ideas/records/*.json` in this exact branch; do not edit manually. Source status and adoption are not implementation evidence.","","| ID | Idea | Lifecycle | Implementation | Source |","| --- | --- | --- | --- | --- |"]
    for d in ideas:
        rows.append("| {} | {} | {} | {} | {} |".format(d["id"],d["title"].replace("|","/"),d["lifecycle_status"],d["implementation_status"],d["origin"]["source_catalog_id"]))
    (ROOT/"ideas"/"INDEX.md").write_text("\n".join(rows)+"\n",encoding="utf-8")
    features=load("features")
    rows=["# Color-Team-OPS — Candidate Features (generated)","","> Generated view only; no verified implementation or release membership is asserted.","","| ID | Feature | Proposed milestone | State |","| --- | --- | --- | --- |"]
    for d in features:
        rows.append("| {} | {} | {} | {} / {} |".format(d["id"],d["title"].replace("|","/"),d["planned_milestone"],d["lifecycle_status"],d["release_membership"]))
    (ROOT/"features"/"INDEX.md").write_text("\n".join(rows)+"\n",encoding="utf-8")
if __name__=="__main__": build()
