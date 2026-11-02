"""Candidate preregistration integrity, NOT model evaluation or oracle authentication."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"evaluation"/"v0.0.2"/"preregistration-draft.json"
S=ROOT/"evaluation"/"v0.0.2"/"candidate-scenarios.json"


class PreregistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(P.read_text(encoding="utf-8"))
        cls.source=json.loads(S.read_text(encoding="utf-8"))

    def test_exact_270_ids_and_9x30(self):
        rows=self.data["cases"]
        self.assertEqual(len(rows),270)
        self.assertEqual({r["case_id"] for r in rows},
                         {r["case_id"] for r in self.source["cases"]})
        for t in {r["team_id"] for r in rows}:
            self.assertEqual(sum(r["team_id"]==t for r in rows),30)

    def test_each_stratum_and_topics(self):
        for t in {r["team_id"] for r in self.data["cases"]}:
            for band in ("normal","edge","adversarial"):
                relevant=[r for r in self.data["cases"]
                          if r["team_id"]==t and r["band"]==band]
                self.assertEqual(len(relevant),10)
                self.assertEqual(len({r["topic"] for r in relevant}),10)

    def test_holdouts_preallocated_not_oracle_verified(self):
        rows=self.data["cases"]
        expected={r["case_id"] for r in rows
                  if int(r["case_id"].split(":")[-1]) >= 9}
        self.assertEqual(set(self.data["holdout_ids"]),expected)
        self.assertEqual(len(expected),54)
        self.assertEqual({r["case_id"] for r in rows if r["holdout"]},expected)

    def test_no_false_independent_labels_or_executions(self):
        self.assertEqual(self.data["independent_oracle_count"],0)
        self.assertEqual(self.data["actual_executed_count"],0)
        self.assertEqual(self.data["release_evaluation_verdict"],"BLOCKED")
        self.assertTrue(all(r["independent_reviewer_ref"] is None
                            and r["trial_receipt"] is None
                            and r["outcome_status"]=="NOT_RUN"
                            and r["label_status"]=="DRAFT_NOT_INDEPENDENT"
                            for r in self.data["cases"]))

    def test_every_case_has_specific_objective_and_first_criterion(self):
        for r in self.data["cases"]:
            self.assertEqual(r["input"]["task"],r["objective"])
            self.assertTrue(r["preliminary_measurable_criteria"][0])
            self.assertNotEqual(r["input"]["scenario_constraint"],"")
            self.assertIn(r["band"],("normal","edge","adversarial"))

    def test_no_model_fixture_masquerades_as_host_run(self):
        self.assertTrue(all(r["input"]["auth"]=="NO_EXTERNAL_WRITE_GRANT"
                            for r in self.data["cases"]))
        self.assertIn("actual hosted model/tool observation",
                      self.data["scoring_spec"]["execution_requirement"])


if __name__=="__main__":
    unittest.main()
