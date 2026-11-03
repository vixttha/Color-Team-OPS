"""P0-P7 release blocker inventory: no synthetic host/eval promotion."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs"/"V002-P0-P7-ACCEPTANCE.json"
HOST=ROOT/"docs"/"V002-P2-P5-HOST-TRIALS.json"


class ReleaseBlockerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(DOC.read_text(encoding="utf-8"))
        cls.h=json.loads(HOST.read_text(encoding="utf-8"))

    def test_exactly_eight_priorities(self):
        self.assertEqual([x["priority"] for x in self.a["priority_status"]],
                         ["P0","P1","P2","P3","P4","P5","P6","P7"])

    def test_release_still_blocked_without_real_host_evidence(self):
        self.assertEqual(self.a["status"],"RELEASE_BLOCKED")
        self.assertFalse(self.a["release_authorized"])
        self.assertEqual(self.a["host_trials"]["count"],0)
        self.assertEqual(self.a["m4"]["independent_oracles"],0)
        self.assertEqual(self.a["m4"]["real_trials"],0)
        self.assertIsNone(self.a["m4"]["accuracy"])

    def test_all_host_cases_are_unrun_without_fake_receipts(self):
        self.assertEqual(len(self.h["scenarios"]),11)
        self.assertEqual(len({x["scenario_id"] for x in self.h["scenarios"]}),11)
        self.assertTrue(all(x["status"]=="NOT_RUN" and x["tool_receipt"] is None
                            and x["actual_host_session_ref"] is None
                            for x in self.h["scenarios"]))

    def test_canonical_version_untouched_and_no_publication(self):
        self.assertEqual(self.a["canonical_installed_version"],"0.0.1")
        self.assertEqual(self.a["version"],"0.0.2")
        self.assertIn("publish-plugin",self.a["authority_not_granted"])

    def test_owner_resolved_initial_skills_only_scope(self):
        statuses={x["priority"]:x["status"] for x in self.a["priority_status"]}
        self.assertEqual(statuses["P0"],"TECHNICALLY_COMPLETE")
        self.assertEqual(self.a["p0_resolution"]["status"],"OWNER_SCOPE_CONFIRMED_SKILLS_ONLY")
        self.assertFalse(self.a["p0_resolution"]["protected_backend_required"])
        self.assertTrue(self.a["p0_resolution"]["host_trials_still_required"])
        self.assertEqual(statuses["P2"],"BLOCKED_EXTERNAL_CAPABILITY")
        self.assertEqual(statuses["P7"],"BLOCKED_EXTERNAL_CAPABILITY")
        self.assertTrue(self.a["staging_plugin"]["installed"])
        self.assertEqual(self.h["staging_plugin"]["discoverability"],"PRIVATE")
        self.assertEqual(self.h["approval_gates"]["staging_identity"],"OWNER_APPROVED_AND_CREATED_ONE_PRIVATE_IDENTITY")


if __name__=="__main__":
    unittest.main()
