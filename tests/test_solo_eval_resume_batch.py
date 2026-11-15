"""No-model synthetic tests of frozen full-evaluation bounded supervisor."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from devtools import cli_eval as e
from devtools import solo_eval_resume_batch as r


class BoundedResumeTests(unittest.TestCase):
    def setUp(self):
        self.cid = lambda i: "yellow-team:normal:" + str(i + 1).zfill(3)
        self.all_pairs = [(self.cid(i), arm) for i in range(270)
                          for arm in e.ARMS]
        self.assertEqual(len(self.all_pairs), 1080)

    def test_two_completed_ungraded_pairs_before_any_new_model_trial(self):
        existing = [
            {"case_id": cid, "arm": arm, "grade": None if i in (22, 40)
             else {"metrics": {"task_correctness": {"status": "PASS"}}}}
            for i, (cid, arm) in enumerate(self.all_pairs[:72])
        ]
        saved, fresh = r.queue_for_full({"full_order": self.all_pairs}, existing)
        self.assertEqual(saved, [self.all_pairs[22], self.all_pairs[40]])
        self.assertEqual(len(fresh), 1008)
        self.assertEqual(fresh[0], self.all_pairs[72])

    def test_graded_pairs_never_queued_again(self):
        existing = [{"case_id": cid, "arm": arm, "grade": {"overall": "PASS"}}
                    for cid, arm in self.all_pairs]
        saved, fresh = r.queue_for_full({"full_order": self.all_pairs}, existing)
        self.assertEqual((saved, fresh), ([], []))

    def test_frozen_order_mutation_and_outside_pair_fail_closed(self):
        frozen = {"full_order": [*self.all_pairs[:-1], self.all_pairs[0]]}
        with self.assertRaisesRegex(e.Invalid, "FULL_ORDER_INTEGRITY"):
            r.queue_for_full(frozen, [])
        with self.assertRaisesRegex(e.Invalid, "UNKNOWN_COMPLETED_PAIR"):
            r.queue_for_full(
                {"full_order": self.all_pairs},
                [{"case_id": "outsider", "arm": "generic", "grade": None}],
            )

    def test_invalid_limits_block_before_local_checkpoints(self):
        with patch.object(r, "validate_frozen",
                          side_effect=AssertionError("must reject before IO")):
            with self.assertRaisesRegex(e.Invalid, "BAD_NEW_PAIR_LIMIT"):
                r.run(Path("freeze.json"), 0, 900)
            with self.assertRaisesRegex(e.Invalid, "BAD_RUNTIME_BUDGET"):
                r.run(Path("freeze.json"), 1, 899)

    def test_frozen_digest_and_policy_are_immutable(self):
        frozen = {
            "evaluation_mode": "SOLO_DEVELOPER", "solo_revision": "solo-eval-v1",
            "candidate_target": 1080, "pilot_target": 36,
            "source_sha": r.EXPECTED_SOURCE_SHA, "grader": {},
        }
        with patch.object(e, "validate_freeze", return_value=frozen):
            with self.assertRaisesRegex(e.Invalid, "FROZEN_V2_SOURCE_OR_MODEL_POLICY_MISMATCH"):
                r.validate_frozen(Path("fake.json"))

    def test_saved_grades_are_attempted_first_and_lock_released(self):
        frozen = {
            "full_order": self.all_pairs,
            "cases": {self.cid(i): {"rubric_sha256": "rubric"} for i in range(270)},
            "source_sha": r.EXPECTED_SOURCE_SHA,
        }
        saved_pairs = self.all_pairs[:2]
        existing = [{"case_id": cid, "arm": arm, "grade": None}
                    for cid, arm in saved_pairs]
        def stats(candidates, grades):
            return {
                "candidate_completed": candidates, "graded": grades,
                "ungraded": candidates - grades,
                "critical_pairs": 0, "contradiction_pairs": 0,
                "high_uncertainty": 0,
                "candidate_attempts": candidates, "grader_invocations": grades,
                "candidate_outcomes": {"COMPLETED": candidates},
                "grader_outcomes": {"GRADED": grades},
            }
        before, after = stats(72, 70), stats(73, 73)
        sample = {"case_id": self.cid(0), "team_id": "yellow-team"}
        auth = MagicMock(returncode=0, stdout=b"Logged in using ChatGPT", stderr=b"")
        calls = []
        def candidate(f, case, arm, exe):
            calls.append((case["case_id"], arm))
            return {"status": "COMPLETED", "raw_sha256": str(len(calls))}, "test response"
        def graded(*args, **kwargs):
            return {"status": "GRADED"}, {
                "overall": "PASS", "critical_violations": [],
                "contradictions": [], "uncertainty": "LOW",
            }
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            with patch.object(r, "validate_frozen", return_value=(frozen, base, existing)), \
                 patch.object(r, "status_snapshot", side_effect=[before, after]), \
                 patch.object(e, "executable", return_value="codex.exe"), \
                 patch.object(r.subprocess, "run", return_value=auth), \
                 patch.object(e, "corpus", return_value=[{
                     "case_id": self.cid(i), "team_id": "yellow-team"
                 } for i in range(270)]), \
                 patch.object(e, "load", return_value={"cases": {
                     self.cid(i): {"required_observable_findings": ["x"]}
                     for i in range(270)
                 }}), \
                 patch.object(r.s, "candidate", side_effect=candidate), \
                 patch.object(r.observed_candidate, "candidate", side_effect=candidate) as fresh, \
                 patch.object(r.g, "grade", side_effect=graded) as grade:
                report = r.run(Path("freeze.json"), 1, 900)
            self.assertEqual(calls, [*saved_pairs, self.all_pairs[2]])
            fresh.assert_called_once()
            self.assertEqual(grade.call_count, 3)
            self.assertEqual(report["saved_responses_graded_this_run"], 2)
            self.assertEqual(report["fresh_candidates_completed_this_run"], 1)
            self.assertEqual(report["status"], "BATCH_LIMIT_REACHED")
            self.assertFalse((base / "supervisor.lock").exists())
            reports = list(base.glob("bounded-full-resume-*.json"))
            self.assertEqual(len(reports), 1)


    def test_verified_recovered_candidate_uses_attempt_two_not_frozen_retry(self):
        frozen = {
            "full_order": self.all_pairs,
            "cases": {self.cid(i): {"rubric_sha256": "rubric"} for i in range(270)},
            "source_sha": r.EXPECTED_SOURCE_SHA,
        }
        cid, arm = self.all_pairs[0]
        existing = [{"case_id": cid, "arm": arm, "grade": None}]
        before = {
            "candidate_completed": 209, "graded": 208, "ungraded": 1,
            "critical_pairs": 0, "contradiction_pairs": 0, "high_uncertainty": 0,
            "candidate_attempts": 210, "grader_invocations": 209,
            "candidate_outcomes": {"COMPLETED": 209, "QUOTA_BLOCKED": 1},
            "grader_outcomes": {"GRADED": 208, "QUOTA_BLOCKED": 1},
        }
        after = dict(before, graded=209, ungraded=0, grader_invocations=210)
        auth = MagicMock(returncode=0, stdout=b"ChatGPT login", stderr=b"")
        recovered_receipt = {"status": "COMPLETED", "raw_sha256": "recovered-raw"}
        grade_result = {"overall": "PASS", "critical_violations": [],
                        "contradictions": [], "uncertainty": "LOW"}
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(r, "validate_frozen",
                              return_value=(frozen, Path(tmp), existing)), \
                 patch.object(r, "status_snapshot", side_effect=[before, after]), \
                 patch.object(e, "executable", return_value="codex.exe"), \
                 patch.object(r.subprocess, "run", return_value=auth), \
                 patch.object(e, "corpus", return_value=[
                     {"case_id": self.cid(i), "team_id": "yellow-team"}
                     for i in range(270)]), \
                 patch.object(e, "load", return_value={"cases": {
                     self.cid(i): {"required_observable_findings": ["synthetic"]}
                     for i in range(270)}}), \
                 patch.object(r.time, "monotonic", side_effect=[0, 1, 600]), \
                 patch.object(r.candidate_recovery, "recovered_for_resume",
                              return_value=(recovered_receipt, "verified response")) as recovered, \
                 patch.object(r.s, "candidate",
                              side_effect=AssertionError("frozen candidate must not be retried")), \
                 patch.object(r.g, "grade", return_value=({"status": "GRADED"}, grade_result)) as grader:
                report = r.run(Path("synthetic-freeze.json"), 1, 900)
        self.assertEqual(recovered.call_count, 1)
        self.assertEqual(grader.call_count, 1)
        self.assertEqual(grader.call_args.args[2], "verified response")
        self.assertEqual(report["saved_responses_graded_this_run"], 1)
        self.assertEqual(report["fresh_candidates_completed_this_run"], 0)
        self.assertEqual(report["status"], "TIME_BUDGET_STOP")


    def test_fresh_candidate_uses_observed_runner_never_frozen_execution(self):
        # Routing/ownership test against the real additive supervisor.
        source = Path(r.__file__).read_text(encoding="utf-8")
        self.assertIn("observed_candidate.candidate(frozen, case, arm, exe)", source)
        self.assertIn("elif existing_candidate:", source)
        self.assertIn("receipt, response = s.candidate(frozen, case, arm, exe)", source)



if __name__ == "__main__":
    unittest.main()
