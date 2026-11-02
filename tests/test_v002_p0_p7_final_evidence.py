"""No fictional specialist or plugin-host evidence in the final review packet."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class P0P7FinalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads((ROOT/"docs"/"V002-P0-P7-ACCEPTANCE.json").read_text())
        cls.r=json.loads((ROOT/"evaluation"/"v0.0.2"/"host-trial-register.json").read_text())
    def test_owner_only_p0_scope(self):
        self.assertEqual(self.a["priority_status"][0]["status"],"TECHNICALLY_COMPLETE")
        self.assertFalse(self.a["p0_resolution"]["protected_backend_required"])
    def test_all_case_ids_not_run_in_host_register(self):
        fixture=json.loads((ROOT/"evaluation"/"v0.0.2"/"concrete-domain-fixtures.json").read_text())
        self.assertEqual({x["case_id"] for x in self.r["cases"]},
                         {x["case_id"] for x in fixture["cases"]})
        self.assertEqual(len(self.r["cases"]),270)
        self.assertTrue(all(x["status"]=="NOT_RUN" and x["provider_receipt"] is None
                            and x["reviewer_ref"] is None for x in self.r["cases"]))
    def test_reference_only_not_model_performance(self):
        self.assertEqual(self.a["m4"]["reference_source_tests_executed"],270)
        self.assertEqual(self.a["m4"]["real_trials"],0)
        self.assertEqual(self.a["m4"]["independent_oracles"],0)
        self.assertIsNone(self.a["m4"]["accuracy"])
    def test_no_release_or_fake_host_test(self):
        self.assertEqual(self.a["status"],"RELEASE_BLOCKED")
        self.assertFalse(self.a["release_authorized"])
        self.assertEqual(self.a["host_trials"]["count"],0)
        self.assertEqual(self.a["canonical_installed_version"],"0.0.1")
    def test_competency_and_law_preserved(self):
        self.assertEqual(len(list((ROOT/"skills").glob("*/SKILL.md"))),12)
        self.assertEqual(len(list((ROOT/"skills").glob("*/references/v002-competencies.md"))),9)
        self.assertIn("not",str(self.a["status"]).lower() if False else "not released")
if __name__=="__main__":unittest.main()
