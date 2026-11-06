"""Synthetic negative and append-only positive tests. No real model calls."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from devtools import cli_eval as e
from devtools import solo_eval as s
from devtools import solo_grader as g
from devtools import solo_eval_quota_recovery as q


class SyntheticRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.cid = "blue-team:normal:01"
        self.arm = "full"
        self.response = "Safe answer"
        self.raw_id = e.digest(b"synthetic candidate trace")
        self.rubric = {"required_observable_findings": ["Answer safely"]}
        self.case = {"case_id": self.cid, "team_id": "blue-team",
                     "fixture": {"artifact_text": "Synthetic data", "variant_probe": "",
                                 "classification": "SYNTHETIC", "external_target_authorized": False},
                     "user_task": "Answer the supplied synthetic question."}
        self.freeze = {"evaluation_mode": "SOLO_DEVELOPER",
                       "solo_revision": "solo-eval-v1",
                       "candidate_target": 1080, "pilot_target": 36,
                       "grader": g.configuration(), "source_sha": "frozen-source",
                       "cases": {self.cid: {"rubric_sha256": e.digest(self.rubric)}}}
        self.record = {"case_id": self.cid, "arm": self.arm,
                       "receipt": {"raw_sha256": self.raw_id, "attempt": 1},
                       "grade": None}
        self.directory = self.base / "grades" / self.raw_id / "1"
        self.directory.mkdir(parents=True)
        self.prompt = e.encode(g.grade_input(self.case, self.rubric, self.response))
        self.binding = {"source_sha": self.freeze["source_sha"],
                        "freeze_sha256": e.digest(self.freeze),
                        "candidate_raw_sha256": self.raw_id,
                        "case_id": self.cid,
                        "rubric_sha256": e.digest(self.rubric)}
        self.raw = b'{"type":"error","message":"quota exhausted"}\n'
        self.stderr = b"quota exhausted"
        (self.directory / "input.json").write_bytes(self.prompt)
        (self.directory / "stdout.jsonl").write_bytes(self.raw)
        (self.directory / "stderr.txt").write_bytes(self.stderr)
        self.receipt = {"kind": "AI_GRADER", "attempt": 1, "status": "QUOTA_BLOCKED",
                        "independent": False, "configuration_sha256": e.digest(g.configuration()),
                        "input_sha256": e.digest(self.prompt),
                        "response_sha256": e.digest(self.response),
                        "native_schema_sha256": e.digest(g.response_schema(self.response)),
                        "rubric_sha256": e.digest(self.rubric),
                        "binding": self.binding, "raw_sha256": e.digest(self.raw),
                        "stderr_sha256": e.digest(self.stderr)}
        e.save_new(self.directory / "receipt.json", self.receipt)
        original_load = e.load
        def fake_load(path):
            if str(path).endswith("reviewer-case-criteria.json"):
                return {"cases": {self.cid: self.rubric}}
            return original_load(path)
        self.patches = [
            patch.object(e, "validate_freeze", return_value=self.freeze),
            patch.object(s, "location", return_value=self.base),
            patch.object(s, "rows", return_value=[self.record]),
            patch.object(e, "corpus", return_value=[self.case]),
            patch.object(e, "load", side_effect=fake_load),
            patch.object(s, "verify_candidate", return_value={"response": self.response}),
        ]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def test_quota_checkpoint_plan_is_read_only_and_binds_exact_metadata(self):
        original = (self.directory / "receipt.json").read_bytes()
        frozen, records, target = q.check(Path(q.FREEZE_REL))
        self.assertEqual(target["case_id"], self.cid)
        self.assertEqual(target["arm"], self.arm)
        result = q.plan(Path(q.FREEZE_REL))
        self.assertEqual(result["new_model_calls"], 0)
        self.assertEqual(result["remaining_frozen_attempts_for_target"], 1)
        self.assertEqual(result["retained_attempt_1"], "QUOTA_BLOCKED")
        self.assertEqual((self.directory / "receipt.json").read_bytes(), original)
        self.assertFalse((self.directory.parent / "2").exists())

    def test_prior_quota_receipt_cannot_be_rewritten_or_retried_twice(self):
        (self.directory.parent / "2").mkdir()
        with self.assertRaisesRegex(e.Invalid, "GRADE_ATTEMPT_2_ALREADY_EXISTS"):
            q.check(Path(q.FREEZE_REL))

    def test_tampered_original_quota_record_cannot_pass(self):
        (self.directory / "stderr.txt").write_bytes(b"tampered evidence")
        with self.assertRaisesRegex(e.Invalid, "BLOCKED_GRADE_RECEIPT_INTEGRITY_FAILURE"):
            q.check(Path(q.FREEZE_REL))

    def test_wrong_status_is_not_a_quota_retry(self):
        old = dict(self.receipt, status="INVALID_GRADE")
        (self.directory / "receipt.json").write_text(json.dumps(old), encoding="utf-8")
        with self.assertRaisesRegex(e.Invalid, "EXPECTED_EXACTLY_ONE"):
            q.check(Path(q.FREEZE_REL))

    def test_no_model_call_without_explicit_authorization(self):
        with patch.object(e, "executable", side_effect=AssertionError("must not call Codex")):
            with self.assertRaisesRegex(e.Invalid, "EXPLICIT_ONE_CALL_AUTHORIZATION_REQUIRED"):
                q.execute_one(Path(q.FREEZE_REL), None)
        self.assertFalse((self.directory.parent / "2").exists())

    def test_append_only_successful_second_grade_reuses_frozen_prompt(self):
        finding = {"status": "PASS", "reason": "Synthetic evidence", "quotes": [self.response]}
        grade = {
            "criteria": [dict(finding, index=0)],
            "metrics": {key: dict(finding) for key in g.METRICS},
            "refusal": {"kind": "NO_REFUSAL", "reason": "None needed", "quotes": []},
            "critical_violations": [], "contradictions": [],
            "uncertainty": "LOW", "limitations": "Synthetic only",
            "overall": "PASS", "injection_detected": False}
        for key in g.UNOBSERVABLE:
            grade["metrics"][key] = {
                "status": "NOT_OBSERVABLE", "reason": "No host telemetry", "quotes": []}
        from unittest.mock import MagicMock
        auth = MagicMock(returncode=0, stdout=b"ChatGPT login", stderr=b"")
        original = (self.directory / "receipt.json").read_bytes()
        completed = dict(self.record, grade=grade)
        with patch.object(s, "rows", side_effect=[[self.record], [completed]]), \
             patch.object(e, "executable", return_value="codex.exe"), \
             patch.object(subprocess, "run", return_value=auth), \
             patch.object(e, "invoke", return_value=(b"synthetic-jsonl\n", b"", 0,
                                                    "2026-11-05T00:00:00+00:00",
                                                    "2026-11-05T00:00:01+00:00",
                                                    1.0, True)) as invoked, \
             patch.object(e, "parse_trace", return_value={
                 "response": json.dumps(grade), "session_sha256": "synthetic-session",
                 "usage": {"input_tokens": 5, "output_tokens": 6}, "tool_events": []}):
            result = q.execute_one(Path(q.FREEZE_REL),
                                    "ALLOW_ONE_EXISTING_CHATGPT_SUBSCRIPTION_GRADER_CALL")
        self.assertEqual(result["disposition"], "GRADED")
        self.assertEqual(result["new_model_calls"], 1)
        self.assertEqual(invoked.call_count, 1)
        self.assertEqual(invoked.call_args.args[1], self.prompt.decode("utf-8"))
        self.assertEqual(invoked.call_args.args[2], g.INSTRUCTIONS)
        self.assertEqual((self.directory / "receipt.json").read_bytes(), original)
        second = e.load(self.directory.parent / "2" / "receipt.json")
        self.assertEqual(second["attempt"], 2)
        self.assertEqual(second["status"], "GRADED")
        self.assertEqual(second["binding"], self.binding)


if __name__ == "__main__":
    unittest.main()
