"""Isolated, no-Codex tests for the append-only frozen candidate retry."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from devtools import cli_eval as e
from devtools import solo_eval as s
from devtools import solo_eval_resume_batch as supervisor
from devtools import solo_eval_candidate_recovery as recovery


class CandidateQuotaRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.case = {"case_id": recovery.TARGET_CASE, "team_id": "blue-team",
                     "holdout_reserved": False,
                     "user_task": "Audit the supplied synthetic blue-team event.",
                     "fixture": {"artifact_text": "synthetic telemetry", "variant_probe": "edge",
                                 "classification": "SYNTHETIC",
                                 "external_target_authorized": False}}
        self.material = "unchanged original no_handoff arm material"
        self.prompt = e.candidate_input(self.case)
        self.freeze = {
            "source_sha": recovery.EXPECTED_SOURCE_SHA,
            "functional_source_sha": "0e9561fd06034674eca4fcf07ceef9381f8249a2",
            "environment": {"model_requested": e.MODEL, "effort_requested": e.EFFORT,
                            "permissions": "read-only", "tools": "NONE_AUTHORIZED",
                            "timeout_seconds": 180, "max_attempts_per_pair": 2},
            "environment_digest": e.digest("original environment"),
            "full_order": [[recovery.TARGET_CASE, recovery.TARGET_ARM]],
            "cases": {recovery.TARGET_CASE: {"input_sha256": e.digest(self.prompt)}},
            "arm_material_sha256": {"blue-team": {recovery.TARGET_ARM: e.digest(self.material)}},
            "cli_version": "0.0.0-synthetic",
        }
        self.parent = self.base / "candidates" / e.digest(recovery.TARGET_CASE + "|" + recovery.TARGET_ARM)[:24]
        self.first = self.parent / "1"
        self.first.mkdir(parents=True)
        self.raw = b'{"type":"error","message":"quota exhausted"}\n'
        self.err = b"quota exhausted"
        (self.first / "input.json").write_text(self.prompt, encoding="utf-8")
        (self.first / "stdout.jsonl").write_bytes(self.raw)
        (self.first / "stderr.txt").write_bytes(self.err)
        self.receipt = {
            "host": "CLI_TEST", "evaluation_mode": "SOLO_DEVELOPER",
            "case_id": recovery.TARGET_CASE, "arm": recovery.TARGET_ARM,
            "attempt": 1, "source_sha": recovery.EXPECTED_SOURCE_SHA,
            "functional_source_sha": self.freeze["functional_source_sha"],
            "environment_digest": self.freeze["environment_digest"],
            "freeze_sha256": recovery.EXPECTED_FREEZE_SHA,
            "input_sha256": e.digest(self.prompt), "arm_sha256": e.digest(self.material),
            "raw_sha256": e.digest(self.raw), "stderr_sha256": e.digest(self.err),
            "started_at": "2026-11-06T05:47:00+00:00",
            "ended_at": "2026-11-06T05:47:01+00:00",
            "latency_seconds": 1.0, "exit_code": 1,
            "cli_version": self.freeze["cli_version"],
            "model_requested": e.MODEL, "effort_requested": e.EFFORT,
            "model_observed": "NOT_EXPOSED_BY_JSONL",
            "model_identity_provenance": "CLI_REQUEST_NOT_PROVIDER_ATTESTED",
            "status": "QUOTA_BLOCKED", "metrics": e.ungraded(self.case),
        }
        e.save_new(self.first / "receipt.json", self.receipt)
        original_digest = e.digest
        def bound_digest(value):
            return (recovery.EXPECTED_FREEZE_SHA if value is self.freeze
                    else original_digest(value))
        self.patches = [
            patch.object(e, "digest", side_effect=bound_digest),
            patch.object(e, "corpus", return_value=[self.case]),
            patch.object(e, "arm_material", return_value={recovery.TARGET_ARM: self.material}),
            patch.object(supervisor, "validate_frozen", return_value=(self.freeze, self.base, [])),
            patch.object(s, "location", return_value=self.base),
        ]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def test_read_only_check_preserves_original_bytes(self):
        before = {p.name: p.read_bytes() for p in self.first.iterdir()}
        status = recovery.plan(Path("synthetic-freeze.json"))
        self.assertEqual(status["previous_status"], "QUOTA_BLOCKED")
        self.assertEqual(status["candidate_model_calls"], 0)
        self.assertFalse(status["runner_execution_authorized"])
        self.assertFalse((self.parent / "2").exists())
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.first.iterdir()})

    def test_missing_original_receipt_is_rejected(self):
        (self.first / "receipt.json").unlink()
        with self.assertRaisesRegex(e.Invalid, "FIRST_RECEIPT_MISSING_OR_SYMLINKED"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_tampered_original_raw_trace_is_rejected(self):
        (self.first / "stdout.jsonl").write_bytes(b"forged")
        with self.assertRaisesRegex(e.Invalid, "BLOCKED_CANDIDATE_EVIDENCE_TAMPERED"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_tampered_original_stderr_is_rejected(self):
        (self.first / "stderr.txt").write_bytes(b"forged")
        with self.assertRaisesRegex(e.Invalid, "BLOCKED_CANDIDATE_EVIDENCE_TAMPERED"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_input_and_arm_binding_rejected_if_changed(self):
        old = dict(self.receipt, arm_sha256=e.digest("different"))
        (self.first / "receipt.json").write_bytes(e.encode(old) + b"\n")
        with self.assertRaisesRegex(e.Invalid, "BLOCKED_CANDIDATE_BINDING_MISMATCH"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_attempt_one_must_be_quota_blocked(self):
        old = dict(self.receipt, status="EXECUTION_BLOCKED")
        (self.first / "receipt.json").write_bytes(e.encode(old) + b"\n")
        with self.assertRaisesRegex(e.Invalid, "BLOCKED_CANDIDATE_BINDING_MISMATCH"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_successful_pair_must_not_be_retried(self):
        with patch.object(supervisor, "validate_frozen", return_value=(
            self.freeze, self.base, [{"case_id": recovery.TARGET_CASE,
                                      "arm": recovery.TARGET_ARM, "grade": None}])):
            with self.assertRaisesRegex(e.Invalid, "TARGET_ALREADY_COMPLETED"):
                recovery.check(Path("synthetic-freeze.json"))

    def test_duplicate_quota_record_refused(self):
        other = self.base / "candidates" / "other" / "1"
        other.mkdir(parents=True)
        e.save_new(other / "receipt.json", dict(self.receipt))
        with self.assertRaisesRegex(e.Invalid, "UNEXPECTED_QUOTA_BLOCKED_PAIR"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_attempt_two_existence_refused_without_mutation(self):
        (self.parent / "2").mkdir()
        with self.assertRaisesRegex(e.Invalid, "CANDIDATE_ATTEMPT_2_ALREADY_EXISTS"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_locked_supervisor_refused(self):
        with patch.object(supervisor, "validate_frozen",
                          side_effect=e.Invalid("SUPERVISOR_LOCK_ALREADY_PRESENT")):
            with self.assertRaisesRegex(e.Invalid, "SUPERVISOR_LOCK_ALREADY_PRESENT"):
                recovery.check(Path("synthetic-freeze.json"))

    def test_no_model_call_without_explicit_auth(self):
        with patch.object(e, "executable", side_effect=AssertionError("must not run")):
            with self.assertRaisesRegex(e.Invalid, "EXPLICIT_CANDIDATE_CALL_APPROVAL_REQUIRED"):
                recovery.execute_one(Path("synthetic-freeze.json"), None)
        self.assertFalse((self.parent / "2").exists())

    def test_recovered_for_resume_is_absent_before_retry(self):
        self.assertIsNone(recovery.recovered_for_resume(
            self.freeze, self.case, recovery.TARGET_ARM))
        self.assertIsNone(recovery.recovered_for_resume(
            self.freeze, {"case_id": "other"}, "full"))

    def test_recovered_for_resume_refuses_incomplete_attempt(self):
        second = self.parent / "2"
        second.mkdir()
        e.save_new(second / "receipt.json", dict(self.receipt, attempt=2))
        with self.assertRaisesRegex(e.Invalid, "RECOVERED_ATTEMPT_NOT_COMPLETED"):
            recovery.recovered_for_resume(self.freeze, self.case, recovery.TARGET_ARM)

    def test_append_only_candidate_attempt_two_success(self):
        original = {p.name: p.read_bytes() for p in self.first.iterdir()}
        auth = MagicMock(returncode=0, stdout=b"Logged in using ChatGPT", stderr=b"")
        trace = b'{"type":"synthetic-test"}\n'
        parsed = {"status": "COMPLETED", "response": "safe synthetic output",
                  "session_sha256": e.digest("session"), "usage": {"input_tokens": 4, "output_tokens": 6},
                  "tool_events": [], "grading": "SOLO_DEVELOPER_UNGRADED"}
        result_row = {"case_id": recovery.TARGET_CASE, "arm": recovery.TARGET_ARM,
                      "grade": None}
        with patch.object(e, "executable", return_value="codex.exe"), \
             patch.object(recovery.subprocess, "run", return_value=auth), \
             patch.object(e, "invoke", return_value=(trace, b"", 0,
                          "2026-11-06T05:48:00+00:00", "2026-11-06T05:48:01+00:00",
                          1.0, True)) as invoked, \
             patch.object(e, "parse_trace", return_value=parsed), \
             patch.object(s, "verify_candidate", return_value={"response": parsed["response"]}), \
             patch.object(s, "rows", return_value=[result_row]):
            status = recovery.execute_one(Path("synthetic-freeze.json"),
                                          recovery.ONE_CALL_ACK)
        self.assertEqual(status["disposition"], "COMPLETED")
        self.assertEqual(status["grade"], "NOT_RUN")
        self.assertEqual(invoked.call_count, 1)
        self.assertEqual(invoked.call_args.args[1], self.prompt)
        self.assertEqual(invoked.call_args.args[2], self.material)
        self.assertEqual(invoked.call_args.args[3], 180)
        self.assertEqual({p.name: p.read_bytes() for p in self.first.iterdir()}, original)
        self.assertFalse((self.base / "supervisor.lock").exists())
        receipt = e.load(self.parent / "2" / "receipt.json")
        self.assertEqual(receipt["attempt"], 2)
        self.assertEqual(receipt["status"], "COMPLETED")
        self.assertEqual((self.parent / "2" / "response.txt").read_text(), parsed["response"])

    def test_forged_model_provenance_is_rejected(self):
        altered = dict(self.receipt, model_identity_provenance="FABRICATED")
        (self.first / "receipt.json").write_bytes(e.encode(altered) + b"\n")
        with self.assertRaisesRegex(e.Invalid, "BLOCKED_CANDIDATE_BINDING_MISMATCH"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_changed_frozen_model_is_rejected(self):
        self.freeze["environment"]["model_requested"] = "unauthorized-model"
        with self.assertRaisesRegex(e.Invalid, "FROZEN_CANDIDATE_CONTRACT_CHANGED"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_changed_arm_material_is_rejected(self):
        with patch.object(e, "arm_material", return_value={recovery.TARGET_ARM: "changed"}):
            with self.assertRaisesRegex(e.Invalid, "FROZEN_INPUT_OR_ARM_CHANGED"):
                recovery.check(Path("synthetic-freeze.json"))

    def test_stale_frozen_environment_binding_is_rejected(self):
        bad = dict(self.receipt, environment_digest=e.digest("different"))
        (self.first / "receipt.json").write_bytes(e.encode(bad) + b"\n")
        with self.assertRaisesRegex(e.Invalid, "BLOCKED_CANDIDATE_BINDING_MISMATCH"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_extra_original_response_for_blocked_candidate_is_rejected(self):
        (self.first / "response.txt").write_text("unexpected fake response", encoding="utf-8")
        with self.assertRaisesRegex(e.Invalid, "BLOCKED_CANDIDATE_HAS_RESPONSE"):
            recovery.check(Path("synthetic-freeze.json"))

    def test_recovered_attempt_is_reusable_without_running_frozen_candidate(self):
        second = self.parent / "2"
        second.mkdir()
        candidate = dict(self.receipt, attempt=2, status="COMPLETED",
                         raw_sha256=e.digest(b"completed trace"),
                         exit_code=0, session_sha256=e.digest("distinct session"),
                         usage={"input_tokens": 1, "output_tokens": 2},
                         tool_events=[], grading="SOLO_DEVELOPER_UNGRADED")
        e.save_new(second / "receipt.json", candidate)
        with patch.object(s, "verify_candidate", return_value={"response": "real recovered response"}) as verify:
            result = recovery.recovered_for_resume(self.freeze, self.case, recovery.TARGET_ARM)
        self.assertEqual(result[0]["attempt"], 2)
        self.assertEqual(result[1], "real recovered response")
        self.assertEqual(verify.call_count, 1)
        self.assertFalse((self.base / "supervisor.lock").exists())

    def test_second_quota_is_terminal_and_not_auto_retried(self):
        auth = MagicMock(returncode=0, stdout=b"ChatGPT login", stderr=b"")
        with patch.object(e, "executable", return_value="codex.exe"), \
             patch.object(recovery.subprocess, "run", return_value=auth), \
             patch.object(e, "invoke", return_value=(self.raw, self.err, 1,
                          "2026-11-06T05:48:00+00:00", "2026-11-06T05:48:01+00:00",
                          1.0, True)) as invoked:
            status = recovery.execute_one(Path("synthetic-freeze.json"),
                                          recovery.ONE_CALL_ACK)
        self.assertEqual(status["disposition"], "QUOTA_BLOCKED")
        self.assertEqual(invoked.call_count, 1)
        self.assertFalse((self.base / "supervisor.lock").exists())
        self.assertEqual(e.load(self.parent / "2" / "receipt.json")["status"], "QUOTA_BLOCKED")
        with self.assertRaisesRegex(e.Invalid, "CANDIDATE_ATTEMPT_2_ALREADY_EXISTS"):
            recovery.check(Path("synthetic-freeze.json"))


if __name__ == "__main__":
    unittest.main()
