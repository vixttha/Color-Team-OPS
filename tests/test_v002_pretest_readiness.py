"""PF-01..PF-05 source-only readiness assertions; NOT hosted ChatGPT execution."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE="0e9561fd06034674eca4fcf07ceef9381f8249a2"
PLUGIN="plugins_6ae9238966508191b3402640e65217bf"
RELEASE="pluginrel_6aea9f63eee88191ba42a906ae04049d"

def read_json(path):
    return json.loads((ROOT/path).read_text(encoding="utf8"))

class PretestReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.smoke=(ROOT/"evaluation/v0.0.2/STAGING-SMOKE-CASES.md").read_text(encoding="utf8")
        cls.freeze=read_json("evaluation/v0.0.2/SMOKE-PROMPT-FREEZE.json")
        cls.host=read_json("docs/V002-P2-P5-HOST-TRIALS.json")
    def test_two_smoke_prompts_match_frozen_candidate_text(self):
        for section,start,end in (
            ("SMOKE_A","## Smoke A — unhinted routing from ordinary task","**Reviewer observations"),
            ("SMOKE_B","## Smoke B — genuine task work requiring a security correction","**Reviewer observations")
        ):
            with self.subTest(case=section):
                self.assertEqual(self.smoke.split(start,1)[1].split(end,1)[0].strip(),
                                 self.freeze["prompts"][section])
                self.assertNotIn("yellow-team",self.freeze["prompts"][section])
                self.assertNotIn("orange-team",self.freeze["prompts"][section])
    def test_correct_installed_release_binding_not_old_staging(self):
        self.assertIn(RELEASE,self.smoke)
        self.assertIn(SOURCE,self.smoke)
        self.assertEqual(self.host["staging_plugin"]["release_id"],RELEASE)
        self.assertEqual(self.host["staging_plugin"]["source_sha"],SOURCE)
        self.assertNotIn("pluginrel_6ae9238a",self.smoke.split("## Smoke A")[0])
    def test_eleven_unique_fixed_candidate_prompts(self):
        rows=self.host["scenarios"]
        self.assertEqual([r["scenario_id"] for r in rows],
                         ["H-%02d"%x for x in range(1,12)])
        self.assertEqual(len({r["candidate_prompt"] for r in rows}),11)
        self.assertTrue(all(len(r["candidate_prompt"])>75 for r in rows))
    def test_H_case_fixtures_and_positive_negative_rubrics(self):
        for row in self.host["scenarios"]:
            with self.subTest(row=row["scenario_id"]):
                self.assertEqual(row["fixture"]["classification"],"FICTIONAL_TEXT_ONLY")
                self.assertEqual(row["setup"]["manifest_sha"],SOURCE)
                self.assertEqual(len(row["reviewer_checklist"]),4)
                self.assertEqual(len(row["critical_failures"]),2)
                self.assertEqual(row["criteria_status"],
                                 "DEVELOPMENT_DRAFT_NOT_INDEPENDENTLY_APPROVED")
    def test_no_fabricated_host_execution_or_receipts(self):
        self.assertEqual(self.host["host_trial_count"],0)
        self.assertIsNone(self.host["tested_candidate_source_sha"])
        self.assertTrue(all(x["status"]=="NOT_RUN" and
                            x["actual_host_session_ref"] is None and
                            x["tool_receipt"] is None and x["verified_by"] is None
                            for x in self.host["scenarios"]))
        receipt=read_json("evaluation/v0.0.2/HOST-TEST-RECEIPT-TEMPLATE.json")
        self.assertIsNone(receipt["chat"]["session_url"])
        self.assertFalse(receipt["provenance"]["actual_trial_executed"])
        self.assertEqual(receipt["review"]["result"],"NOT_RUN")
    def test_no_development_self_approval_of_270(self):
        c=read_json("evaluation/v0.0.2/reviewer-case-criteria.json")
        p=read_json("evaluation/v0.0.2/preregistration-draft.json")
        self.assertEqual(c["independently_approved"],0)
        self.assertEqual(c["host_trials"],0)
        self.assertEqual(p["holdout_total"],54)
        self.assertEqual(p["independent_oracle_count"],0)
        self.assertIn("NOT BLINDED",(ROOT/"evaluation/v0.0.2/INDEPENDENT-EVALUATION-PREREGISTRATION.md").read_text())
    def test_all_active_trackers_are_bound_to_same_staging_identity(self):
        docs=[read_json("docs/"+n) for n in (
            "V002-P0-P7-ACCEPTANCE.json","V002-MASTER-RELEASE-GATES.json",
            "V002-REMAINING-TASK-LEDGER.json")]
        for x in docs:
            with self.subTest(doc=x.get("schema_version",x["mission_id"])):
                self.assertEqual(x["staging_plugin"]["release_id"],RELEASE)
                self.assertEqual(x["staging_plugin"]["source_sha"],SOURCE)
                self.assertTrue(x["current_pretest_readiness"]["source_reference_is_not_docs_git_sha"])
    def test_no_release_promoted_by_documentation(self):
        x=read_json("docs/V002-P0-P7-ACCEPTANCE.json")
        self.assertEqual(x["status"],"RELEASE_BLOCKED")
        self.assertFalse(x["release_authorized"])
        self.assertEqual(x["m4"]["independent_oracles"],0)
        self.assertEqual(x["host_trials"]["count"],0)
        self.assertEqual(x["canonical_installed_version"],"0.0.1")
    def test_preflight_describes_truthful_capture_limits(self):
        doc=(ROOT/"docs/V002-HOST-TEST-OPERATOR-PREFLIGHT.md").read_text()
        for token in ("NOT_OBSERVABLE","LOGICAL_ONLY","fresh ChatGPT","verbatim",
                      "Plugin Creator","separate Purple","RELEASE_BLOCKED"):
            self.assertIn(token,doc)

if __name__=="__main__": unittest.main()
