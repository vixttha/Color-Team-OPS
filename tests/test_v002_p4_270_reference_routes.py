"""P4: real source-router executions across 270 concrete synthetic cases.

270 dynamically registered unittest methods exercise M3 reference code, NOT an
installed plugin, actual LLM specialist, independent oracle, or quality score.
"""
import json
import unittest
from dataclasses import replace
from pathlib import Path
from policy_v002.route_advice import RouteIntent, recommend_one
from policy_v002.team_directory import TeamDirectory

ROOT=Path(__file__).resolve().parents[1]
CASES=json.loads((ROOT/"evaluation"/"v0.0.2"/"concrete-domain-fixtures.json").read_text(encoding="utf8"))["cases"]
REG=json.loads((ROOT/"registry"/"v0.0.2"/"teams.json").read_text(encoding="utf8"))
CAPS={x["id"]: x["capabilities"][0] for x in REG["teams"]}
SHA="a"*40

class ReferenceRouteCaseTests(unittest.TestCase):
    def case(self, row):
        team=row["team_id"]
        cap=CAPS[team]
        base=RouteIntent(
            mission_id="ctov002reference",source_sha=SHA,observed_sha=SHA,
            mission_revision=1,observed_revision=1,
            permitted_teams=(team,),required_capabilities=(cap["id"],),
            available_tools=tuple(cap["requires_tools"]),
            task_text=row["user_task"]+" "+row["fixture"]["variant_probe"],
            active_worker=None,prior_gate_status="NOT_REQUIRED",
            dispatch_count=0,max_handoffs=1)
        # This validates source metadata contract for each case; the required
        # capability is supplied from the accepted registry, not independently
        # predicted by a model. It is therefore NOT routing accuracy.
        out=recommend_one(base)
        self.assertEqual((out.status,out.suggested_team),
                         ("SUGGEST_ONLY",team),row["case_id"])
        self.assertEqual(out.code,"CANDIDATE_NOT_AUTHORIZED")
        self.assertEqual(recommend_one(replace(base,observed_sha="b"*40)).code,"STALE_SOURCE")
        self.assertEqual(recommend_one(replace(base,active_worker="yellow-team")).code,
                         "ONE_ACTIVE_WORKER_ENFORCED")
        self.assertEqual(recommend_one(replace(base,dispatch_count=2)).code,
                         "HANDOFF_BUDGET_EXCEEDED")
        if cap["requires_tools"]:
            denied=recommend_one(replace(base,available_tools=()))
            self.assertIn(denied.status,("CAPABILITY_BLOCKED","ABSTAIN"))
    def test_all_270_are_distinct_source_case_definitions(self):
        self.assertEqual(len(CASES),270)
        self.assertEqual(len({r["case_id"] for r in CASES}),270)

def make_case(row):
    def test(self): self.case(row)
    test.__doc__="Reference-only dispatch safety: "+row["case_id"]
    return test

for _row in CASES:
    setattr(ReferenceRouteCaseTests,
            "test_ref_"+_row["case_id"].replace("-","_").replace(":","_"),
            make_case(_row))

if __name__=="__main__": unittest.main()
