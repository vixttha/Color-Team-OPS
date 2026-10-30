#!/usr/bin/env python3
"""Optional stdlib structural validation; DOES NOT authenticate evidence or certify release."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
IDEA_RE=re.compile(r"IDEA-[0-9]{6}$")
FEAT_RE=re.compile(r"FEAT-[0-9]{6}$")
SHA_RE=re.compile(r"[a-f0-9]{40}$")
IDEA_STATES={"captured","triaged","exploring","decision_ready","adopted","parked","rejected","superseded","duplicate","retired"}
FEATURE_STATES={"proposed","planned","in_progress","implemented","verified","deprecated","retired"}

def validate():
    failures=[]
    def records(section):
        entries={}
        for p in sorted((ROOT/section/"records").glob("*.json")):
            try: d=json.loads(p.read_text(encoding="utf-8"))
            except (ValueError,OSError) as e: failures.append(f"{p}: invalid JSON: {e}");continue
            ident=d.get("id","")
            if not isinstance(ident,str) or not (IDEA_RE if section=="ideas" else FEAT_RE).fullmatch(ident): failures.append(f"{p}: bad ID");continue
            if p.stem!=ident or ident in entries: failures.append(f"{p}: duplicate/mismatched ID")
            entries[ident]=d
        return entries
    ideas=records("ideas"); features=records("features")
    if len(ideas)!=36: failures.append(f"Expected 36 migrated source ideas, found {len(ideas)}")
    if len(features)!=5: failures.append(f"Expected 5 initial feature candidates, found {len(features)}")
    for ident,d in ideas.items():
        if d.get("schema_version")!=1 or d.get("lifecycle_status") not in IDEA_STATES:failures.append(f"{ident}: schema/lifecycle")
        if d.get("implementation_status") not in {"not_planned","planned","in_progress","implemented","removed","not_applicable"}:failures.append(f"{ident}: implementation")
        if d.get("testing",{}).get("status") not in {"untested","planned","in_progress","tested"}:failures.append(f"{ident}: testing status")
        if d.get("testing",{}).get("status")=="tested" and (d.get("testing",{}).get("outcome") not in {"pass","fail","mixed","inconclusive"} or not d.get("testing",{}).get("refs")):failures.append(f"{ident}: missing completed-test evidence")
        if d.get("lifecycle_status")=="adopted" and d.get("decision",{}).get("decision_scope")!="idea_direction_only":failures.append(f"{ident}: ungrounded decision")
        if any(t not in ideas or t==ident for t in d.get("related_ideas",[])):failures.append(f"{ident}: missing/self relation")
        for ev in d.get("evidence",[]):
            if not SHA_RE.fullmatch(str(ev.get("source_sha",""))):failures.append(f"{ident}: invalid source SHA")
            if ".." in Path(str(ev.get("path",""))).parts or str(ev.get("path","")).startswith("/"):failures.append(f"{ident}: unsafe path")
    for ident,d in features.items():
        if d.get("schema_version")!=1 or d.get("lifecycle_status") not in FEATURE_STATES:failures.append(f"{ident}: schema/lifecycle")
        if d.get("release_membership")!="NOT_ASSERTED":failures.append(f"{ident}: false release inclusion")
        if d.get("lifecycle_status")=="verified" and not d.get("verified_evidence"):failures.append(f"{ident}: no verification receipt")
        if any(z not in ideas for z in d.get("idea_ids",[])):failures.append(f"{ident}: missing idea relation")
    return failures

if __name__=="__main__":
    problems=validate()
    if problems:
        for line in problems: print("FAIL",line)
        raise SystemExit(1)
    print("PASS: idea and candidate-feature structural integrity; NO authority or execution claimed")
