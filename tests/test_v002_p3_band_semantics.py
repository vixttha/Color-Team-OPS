"""Development-only P3 source checks. These are NOT installed host or model trials."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"evaluation"/"v0.0.2"/"concrete-domain-fixtures.json"

def make_candidate_input(row):
    f=row["fixture"]
    return ("Read-only synthetic task: "+row["objective"]+
            "\nFixture: "+f["artifact_text"]+
            "\nRequired condition: "+f["variant_probe"]+
            "\nUse only supplied facts. Separate missing evidence from real tool receipts.")

class P3VariantSemantics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads(DATA.read_text(encoding="utf-8"))["cases"]
        cls.by_id={r["case_id"]:r for r in cls.rows}

    def test_all_270_have_distinct_candidate_inputs_per_variant(self):
        self.assertEqual(len(self.rows),270)
        self.assertEqual(len(self.by_id),270)
        for team in {r["team_id"] for r in self.rows}:
            for i in range(1,11):
                trio=[self.by_id[f"{team}:{band}:{i:02d}"]
                      for band in ("normal","edge","adversarial")]
                self.assertEqual(len({make_candidate_input(c) for c in trio}),3)
                self.assertEqual(len({c["fixture"]["variant_probe"] for c in trio}),3)
                for row in trio:
                    prompt=make_candidate_input(row)
                    self.assertIn(row["fixture"]["variant_probe"],prompt)
                    self.assertIn(row["fixture"]["artifact_text"],prompt)
                    self.assertNotIn(row["team_id"],prompt)
                    self.assertNotIn(row["case_id"],prompt)

    def test_difficulty_proposal_not_interchangeable(self):
        for team in {r["team_id"] for r in self.rows}:
            for i in range(1,11):
                trio=[self.by_id[f"{team}:{band}:{i:02d}"]
                      for band in ("normal","edge","adversarial")]
                self.assertEqual(len({
                    row["task_specific_proposed_oracle"]["variant_proposed_disposition"]
                    for row in trio}),3)

    def test_blue_missing_evidence_and_adversarial_requirements(self):
        for band in ("normal","edge","adversarial"):
            row=self.by_id[f"blue-team:{band}:01"]
            text=" ".join(row["measurement"]["variant_must_address"]+
                          row["measurement"]["variant_fail_if"]).lower()
            self.assertIn("event",text)
            self.assertIn("fabricat",text)
            self.assertIn("no individual event ids",make_candidate_input(row).lower())
            self.assertFalse(row["task_specific_proposed_oracle"]["approved"])
        edge=self.by_id["blue-team:edge:01"]
        self.assertIn("100 authentication denials per minute",make_candidate_input(edge))

    def test_no_unearned_host_or_reviewer_acceptance(self):
        for row in self.rows:
            self.assertEqual(row["outcome_status"],"NOT_RUN")
            self.assertEqual(row["independent_oracle_status"],"NOT_VERIFIED")
            self.assertIsNone(row["observed_host_trial_ref"])
            self.assertFalse(row["holdout_blinded"])
        self.assertEqual(sum(r["holdout_reserved"] for r in self.rows),54)

if __name__=="__main__":unittest.main()
