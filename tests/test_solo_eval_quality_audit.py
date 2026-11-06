"""Regression tests for the additive read-only frozen-v2 audit companion."""
import json
import tempfile
import unittest
from pathlib import Path

from devtools import cli_eval as e
from devtools import solo_eval_quality_audit as a


def graded(cid, arm, status):
    return {"case_id": cid, "arm": arm,
            "grade": {"metrics": {"task_correctness": {"status": status}}}}


class FrozenQualityAuditTests(unittest.TestCase):
    def test_accepted_three_exclusions_bound_to_exact_freeze(self):
        freeze = {"synthetic": "freeze"}
        exclusions = [{"case_id": cid, "metric": "task_correctness"}
                      for cid, metric in sorted(a.REQUIRED_EXCLUSIONS)]
        review = {"freeze_sha256": e.digest(freeze),
                  "accuracy_exclusions": exclusions}
        self.assertEqual(a.verified_exclusions(review, freeze),
                         {cid for cid, metric in a.REQUIRED_EXCLUSIONS})
        with self.assertRaises(e.Invalid):
            a.verified_exclusions(dict(review, freeze_sha256="wrong"), freeze)
        with self.assertRaises(e.Invalid):
            a.verified_exclusions(dict(review, accuracy_exclusions=exclusions[:-1]), freeze)

    def test_exclusions_remove_ambiguous_accuracy_not_honest_failures(self):
        records = [
            graded("black-team:normal:01", "generic", "FAIL"),
            graded("black-team:normal:01", "full", "PASS"),
            graded("blue-team:normal:01", "generic", "PASS"),
            graded("blue-team:normal:01", "full", "FAIL"),
            graded("orange-team:normal:01", "generic", "PASS"),
            graded("orange-team:normal:01", "full", "PASS"),
        ]
        filtered = a.accuracy_after_exclusions(records, {"black-team:normal:01"})
        self.assertEqual(filtered["generic"]["graded_denominator"], 2)
        self.assertEqual(filtered["full"]["graded_denominator"], 2)
        self.assertEqual(filtered["full"]["states"], {"FAIL": 1, "PASS": 1})
        self.assertEqual(filtered["full"]["paired_n"], 2)
        self.assertEqual(filtered["full"]["paired_delta"], -.5)
        self.assertEqual(filtered["generic"]["paired_delta"], 0)

    def test_no_grades_do_not_imply_accuracy(self):
        quality = a.accuracy_after_exclusions(
            [{"case_id": "blue-team:normal:01", "arm": "full", "grade": None}], set())
        self.assertEqual(quality["full"]["graded_denominator"], 0)
        self.assertIsNone(quality["full"]["strict_correctness"])
        self.assertIsNone(quality["full"]["paired_delta"])

    def test_duplicate_pair_or_unknown_arm_fails_closed(self):
        row = graded("orange-team:normal:01", "full", "PASS")
        with self.assertRaises(e.Invalid):
            a.accuracy_after_exclusions([row, row], set())
        with self.assertRaises(e.Invalid):
            a.accuracy_after_exclusions([dict(row, arm="unapproved")], set())

    def test_quota_receipt_requires_inspection_not_fake_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            status = a.local_checkpoint_status(
                {"dummy": "freeze"}, [],
                [{"case_id": "blue-team:normal:02", "arm": "full",
                  "status": "QUOTA_BLOCKED"}], [], p)
            self.assertEqual(status["resume_disposition"], "BLOCKED_INSPECT_LOCALLY")
            self.assertIn("FROZEN_RUNNER_CANNOT_RESUME_TERMINAL_CANDIDATE_CHECKPOINTS",
                          status["resume_blockers"])
            self.assertFalse(status["pilot_acceptance_present_and_bound"])

    def test_pilot_acceptance_bound_and_lock_blocks_resume(self):
        arms = ("generic", "full", "no_directory", "no_handoff")
        pairs = [(f"team-{i}", arm) for i in range(9) for arm in arms]
        freeze = {"dummy": "freeze", "pilot_order": pairs}
        pilot = {"freeze_sha256": e.digest(freeze),
                 "summary": {"candidate_completed": 36, "graded": 36,
                             "critical_pairs": 0, "contradiction_pairs": 0,
                             "high_uncertainty": 0}}
        records = [{"case_id": cid, "arm": arm,
                    "grade": {"critical_violations": [], "contradictions": [],
                              "uncertainty": "LOW"}} for cid, arm in pairs]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "pilot-acceptance.json").write_text(json.dumps(pilot), encoding="utf-8")
            with self.assertRaises(e.Invalid):
                a.local_checkpoint_status(freeze, records[:-1], [], [], p)
            status = a.local_checkpoint_status(freeze, records, [], [], p)
            self.assertEqual(status["resume_disposition"],
                             "PRECHECK_PASS_LOCAL_AUTH_QUOTA_UNVERIFIED")
            (p / "supervisor.lock").write_text("not-authority", encoding="utf-8")
            status = a.local_checkpoint_status(freeze, records, [], [], p)
            self.assertEqual(status["resume_disposition"], "BLOCKED_INSPECT_LOCALLY")
            self.assertTrue(status["supervisor_lock_present"])

    def test_existing_frozen_files_are_never_rewritten(self):
        freeze=e.load(e.ROOT / e.EVAL / "CLI-EVAL-SOLO-FREEZE-v2.json")
        self.assertIn("devtools/solo_eval.py", freeze["file_sha256"])
        self.assertIn("devtools/solo_grader.py", freeze["file_sha256"])
        self.assertIn("evaluation/v0.0.2/reviewer-case-criteria.json", freeze["file_sha256"])
        self.assertNotIn("devtools/solo_eval_quality_audit.py", freeze["file_sha256"])


if __name__ == "__main__":
    unittest.main()
