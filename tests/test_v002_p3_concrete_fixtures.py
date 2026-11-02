"""P3: concrete domain probes exist; no independent model evaluation claimed."""
import json, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"evaluation"/"v0.0.2"
class ConcreteFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads((P/"concrete-domain-fixtures.json").read_text(encoding="utf-8"))
        cls.original=json.loads((P/"candidate-scenarios.json").read_text(encoding="utf-8"))
    def test_complete_ids_and_specialist_distribution(self):
        rows=self.a["cases"]
        self.assertEqual(len(rows),270)
        self.assertEqual({r["case_id"] for r in rows},{r["case_id"] for r in self.original["cases"]})
        self.assertEqual(len({(r["team_id"],r["topic"]) for r in rows}),90)
        for t in {r["team_id"] for r in rows}:
            self.assertEqual(sum(r["team_id"]==t for r in rows),30)
    def test_each_band_has_nonidentical_probe(self):
        rows={r["case_id"]:r for r in self.a["cases"]}
        for team in {r["team_id"] for r in rows.values()}:
            for i in range(1,11):
                variants=[rows[f"{team}:{band}:{i:02d}"] for band in
                          ("normal","edge","adversarial")]
                self.assertEqual(len({r["fixture"]["variant_probe"] for r in variants}),3)
                self.assertTrue(all(len(r["fixture"]["artifact_text"])>65 for r in variants))
                self.assertTrue(all(len(r["task_specific_proposed_oracle"]["expected_core_finding"])>40
                                    for r in variants))
    def test_holdouts_not_blinded(self):
        self.assertEqual(self.a["holdout_reservations"],54)
        self.assertFalse(self.a["holdout_blinded"])
        self.assertEqual(sum(r["holdout_reserved"] for r in self.a["cases"]),54)
        self.assertTrue(all(not r["holdout_blinded"] for r in self.a["cases"]))
    def test_not_falsely_labeled_or_executed(self):
        self.assertEqual((self.a["independent_oracle_count"],self.a["actual_host_trial_count"]),(0,0))
        self.assertTrue(all(not r["task_specific_proposed_oracle"]["approved"]
            and r["external_reviewer_ref"] is None and r["observed_host_trial_ref"] is None
            and r["outcome_status"]=="NOT_RUN"
            and r["independent_oracle_status"]=="NOT_VERIFIED"
            for r in self.a["cases"]))
    def test_no_hidden_live_tools(self):
        self.assertTrue(all(not r["fixture"]["external_target_authorized"]
            and r["fixture"]["classification"]=="SYNTHETIC_SAFE_REFERENCE_ONLY"
            and r["measurement"]["tool_requirement"]=="NO_EXTERNAL_TOOLS_REQUIRED_FOR_DRAFT_STATIC_ANALYSIS"
            for r in self.a["cases"]))
    def test_output_requirements_and_retests(self):
        for r in self.a["cases"]:
            self.assertEqual(r["measurement"]["required_output_fields"],
                             ["status","finding","source_scope","evidence_refs","next_action"])
            self.assertEqual(len(r["retest"]["baseline_arms"]),4)

if __name__=="__main__":unittest.main()
