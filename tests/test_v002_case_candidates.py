"""M4 authored scenario specification checks; NEVER a performance benchmark PASS."""
import json
from collections import Counter, defaultdict
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"evaluation"/"v0.0.2"/"candidate-scenarios.json"
TEAMS={"yellow-team","orange-team","green-team","red-team","blue-team",
       "purple-team","white-team","black-team","gray-cell"}
BANDS={"normal","edge","adversarial"}

def candidates():
    return json.loads(FILE.read_text(encoding="utf-8"))

class CandidateScenarioTests(unittest.TestCase):
    def setUp(self):
        self.data=candidates()
        self.cases=self.data["cases"]

    def test_270_unique_draft_case_ids(self):
        self.assertEqual(len(self.cases),270)
        self.assertEqual(len({x["case_id"] for x in self.cases}),270)

    def test_exactly_nine_teams(self):
        self.assertEqual({x["team_id"] for x in self.cases},TEAMS)

    def test_thirty_per_team(self):
        counts=Counter(x["team_id"] for x in self.cases)
        self.assertEqual(set(counts.values()),{30})

    def test_ten_per_team_per_band(self):
        counts=Counter((x["team_id"],x["band"]) for x in self.cases)
        self.assertEqual(len(counts),27)
        self.assertEqual(set(counts.values()),{10})
        self.assertEqual({x["band"] for x in self.cases},BANDS)

    def test_distinct_case_prompts(self):
        self.assertEqual(len({x["prompt"] for x in self.cases}),270)

    def test_oracles_are_not_forged(self):
        self.assertEqual({x["label_status"] for x in self.cases},
                         {"DRAFT_NEEDS_INDEPENDENT_ORACLE"})
        self.assertTrue(all(x["independent_reviewer_ref"] is None
                            and x["oracle_digest"] is None for x in self.cases))

    def test_not_one_trial_has_been_run(self):
        self.assertTrue(all(x["outcome_status"]=="NOT_RUN" and
             x["observed_provider_receipts"]==[] for x in self.cases))
        self.assertEqual(self.data["source_classification"],"DRAFT_UNLABELED_NOT_EVALUATED")

    def test_success_and_critical_cases_are_explicit_proposals(self):
        self.assertTrue(all(len(x["proposed_success_criteria"])>=3
             and x["proposed_critical_failure"] for x in self.cases))

    def test_no_unapproved_live_red_target(self):
        red=[x for x in self.cases if x["team_id"]=="red-team"]
        self.assertTrue(red and all(x["task_auth"]=="SYNTHETIC_NO_EXTERNAL_TARGET" for x in red))

    def test_each_team_has_ten_distinct_objectives(self):
        groups=defaultdict(set)
        for x in self.cases:
            groups[x["team_id"]].add(x["objective"])
        self.assertTrue(all(len(group)==10 for group in groups.values()))

    def test_no_measured_99_percent_claim(self):
        self.assertNotIn("99%",FILE.read_text())
        self.assertEqual(self.data["case_authority"],"NONE")

if __name__=="__main__":
    unittest.main()
