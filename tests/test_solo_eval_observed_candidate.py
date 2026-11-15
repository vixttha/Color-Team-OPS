"""No-model tests for future SOLO matrix candidate CLI-version provenance."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from devtools import cli_eval as e
from devtools import solo_eval as s
from devtools import solo_eval_candidate_recovery as recovery
from devtools import solo_eval_observed_candidate as observed


class ObservedCandidateTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.case = {"case_id": "blue-team:edge:05", "team_id": "blue-team",
                     "holdout_reserved": False}
        self.arm = "no_handoff"
        self.prompt = "synthetic test input"
        self.material = "synthetic frozen specialist pack"
        self.frozen = {
            "source_sha": "f" * 40,
            "environment_digest": "a" * 64,
            "cli_version": "codex-cli 0.166.0",
            "cases": {self.case["case_id"]: {"input_sha256": e.digest(self.prompt)}},
            "arm_material_sha256": {"blue-team": {self.arm: e.digest(self.material)}},
            "environment": {"max_attempts_per_pair": 2, "timeout_seconds": 180},
            "source": "SYNTHETIC",
        }
        self.parent = self.base / "candidates" / e.digest(
            self.case["case_id"] + "|" + self.arm)[:24]
        self.patches = [
            patch.object(s, "location", return_value=self.base),
            patch.object(e, "candidate_input", return_value=self.prompt),
            patch.object(e, "arm_material", return_value={self.arm: self.material}),
        ]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def test_new_candidate_uses_observed_cli_not_frozen_value(self):
        answer = "synthetic safe answer"
        events = [
            {"type": "thread.started", "thread_id": "synthetic-session"},
            {"type": "turn.started"},
            {"type": "item.completed", "item": {
                "id": "synthetic-message", "type": "agent_message", "text": answer,
            }},
            {"type": "turn.completed", "usage": {"input_tokens": 3, "output_tokens": 4}},
        ]
        trace = b"".join(e.encode(event) + b"\n" for event in events)
        for label in ("codex-cli 0.100.0", "codex-cli 0.166.0", "codex-cli 0.169.0",
                      "codex-cli 3.1.0-beta.1+build.7"):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp, \
                 patch.object(s, "location", return_value=Path(tmp)), \
                 patch.object(recovery.subprocess, "check_output",
                              return_value=(label + "\r\n").encode()) as version, \
                 patch.object(e, "invoke", return_value=(
                     trace, b"", 0, "2026-11-14T00:00:00+00:00",
                     "2026-11-14T00:00:01+00:00", 1.0, True)) as invoked:
                receipt, response = observed.candidate(
                    self.frozen, self.case, self.arm, "codex-native.exe")
                trial = Path(tmp) / self.parent.relative_to(self.base) / "1"
                self.assertEqual(response, answer)
                self.assertEqual(receipt["status"], "COMPLETED")
                self.assertEqual(receipt["cli_version"], label)
                self.assertEqual(e.load(trial / "receipt.json")["cli_version"], label)
                self.assertEqual(s.verify_candidate(self.frozen, trial, set(), set())["response"],
                                 answer)
                version.assert_called_once()
                self.assertEqual(version.call_args.args[0], ["codex-native.exe", "--version"])
                invoked.assert_called_once()
        self.assertEqual(self.frozen["cli_version"], "codex-cli 0.166.0")

    def test_invalid_version_stops_before_writing_or_calling_model(self):
        with patch.object(observed, "observed_cli_version",
                          side_effect=e.Invalid("CODEX_EXECUTOR_VERSION_UNVERIFIED")), \
             patch.object(e, "invoke",
                          side_effect=AssertionError("model must not run")):
            with self.assertRaisesRegex(e.Invalid, "CODEX_EXECUTOR_VERSION_UNVERIFIED"):
                observed.candidate(self.frozen, self.case, self.arm, "codex-native.exe")
        self.assertFalse(self.parent.exists())

    def test_old_completed_candidate_read_without_runtime_version_probe(self):
        self.parent.joinpath("1").mkdir(parents=True)
        e.save_new(self.parent / "1" / "receipt.json", {
            "status": "COMPLETED", "cli_version": "codex-cli 0.166.0"})
        with patch.object(observed, "observed_cli_version",
                          side_effect=AssertionError("must not probe")), \
             patch.object(s, "verify_candidate",
                          return_value={"response": "existing immutable answer"}), \
             patch.object(e, "invoke",
                          side_effect=AssertionError("model must not run")):
            receipt, response = observed.candidate(
                self.frozen, self.case, self.arm, "codex-native.exe")
        self.assertEqual(receipt["cli_version"], "codex-cli 0.166.0")
        self.assertEqual(response, "existing immutable answer")

    def test_original_quota_obstruction_does_not_retry_or_probe(self):
        self.parent.joinpath("1").mkdir(parents=True)
        e.save_new(self.parent / "1" / "receipt.json", {"status": "QUOTA_BLOCKED"})
        with patch.object(observed, "observed_cli_version",
                          side_effect=AssertionError("must not probe")), \
             patch.object(e, "invoke",
                          side_effect=AssertionError("model must not run")):
            receipt, response = observed.candidate(
                self.frozen, self.case, self.arm, "codex-native.exe")
        self.assertEqual(receipt["status"], "QUOTA_BLOCKED")
        self.assertIsNone(response)

    def test_original_frozen_arm_cannot_be_changed(self):
        with patch.object(e, "arm_material", return_value={self.arm: "changed"}), \
             patch.object(observed, "observed_cli_version",
                          side_effect=AssertionError("must not probe")), \
             patch.object(e, "invoke",
                          side_effect=AssertionError("model must not run")):
            with self.assertRaisesRegex(e.Invalid, "CANDIDATE_ARM_CHANGED"):
                observed.candidate(self.frozen, self.case, self.arm, "codex-native.exe")
        self.assertFalse(self.parent.exists())


if __name__ == "__main__":
    unittest.main()
