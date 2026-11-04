"""Reviewer onboarding packet tests: no signatures, identities, or approvals invented."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from devtools import cli_eval
from devtools import cli_eval_reviewer_intake as intake


class IndependentReviewerIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.freeze_path = cli_eval.ROOT / cli_eval.EVAL / "CLI-EVAL-FREEZE-2026-11-04.json"
        cls.freeze = cli_eval.load(cls.freeze_path)
        cls.cases = cli_eval.corpus(cli_eval.ROOT)
        cls.criteria = cli_eval.load(
            cli_eval.ROOT / cli_eval.EVAL / "reviewer-case-criteria.json")["cases"]

    def test_270_review_packets_no_outputs_no_approval(self):
        packets, templates = intake.assemble(
            self.freeze, self.cases, self.criteria)
        self.assertEqual(len(packets), 270)
        self.assertEqual(len(templates), 270)
        self.assertEqual(len({p["case_id"] for p in packets}), 270)
        self.assertEqual(sum(p["holdout_classification"] ==
                             "NONBLIND_REGRESSION_ONLY" for p in packets), 54)
        self.assertTrue(all(p["candidate_output"] is None and
                            p["independent_score"] is None for p in packets))
        self.assertTrue(all(t["decision"] == "PENDING_NOT_APPROVED" and
                            t["reviewer_principal"] is None and
                            t["reviewed_at"] is None for t in templates))
        self.assertEqual(self.freeze["oracle_independent_approvals"], 0)

    def test_candidate_input_and_rubric_pinned_to_freeze(self):
        packets, templates = intake.assemble(
            self.freeze, self.cases, self.criteria)
        first = packets[0]
        cid = first["case_id"]
        self.assertEqual(first["frozen_rubric_sha256"],
                         self.freeze["cases"][cid]["rubric_sha256"])
        self.assertEqual(first["frozen_candidate_input_sha256"],
                         self.freeze["cases"][cid]["input_sha256"])
        original = next(c for c in self.cases if c["case_id"] == cid)
        self.assertEqual(first["candidate_input"],
                         json.loads(cli_eval.candidate_input(original)))
        self.assertIn("technical_outcome", templates[0])

    def test_changed_rubric_fails_closed(self):
        bad = copy.deepcopy(self.criteria)
        cid = self.cases[0]["case_id"]
        bad[cid]["required_observable_findings"].append("injected change")
        with self.assertRaisesRegex(ValueError, "SOURCE_OR_RUBRIC_CHANGED"):
            intake.assemble(self.freeze, self.cases, bad)

    def test_missing_case_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "EXPECTED_EXACT_270"):
            intake.assemble(self.freeze, self.cases[:-1], self.criteria)

    def test_requires_fresh_private_output(self):
        with tempfile.TemporaryDirectory() as t:
            with patch.object(intake, "PRIVATE", Path(t)):
                self.assertEqual(intake.ensure_private_destination(
                    Path(t) / "new"), (Path(t) / "new").resolve())
                with self.assertRaisesRegex(ValueError, "OUTPUT_MUST_BE"):
                    intake.ensure_private_destination(Path(t).parent / "outside")
                with self.assertRaises(FileExistsError):
                    intake.ensure_private_destination(Path(t))

    def test_prepare_writes_only_unsigned_local_material(self):
        with tempfile.TemporaryDirectory() as t:
            with patch.object(intake, "PRIVATE", Path(t)):
                dest = Path(t) / "new"
                report = intake.prepare(self.freeze_path, dest)
                packets = json.loads((dest / "reviewer-packets.json").read_text())
                templates = json.loads((dest / "UNSIGNED-REVIEW-TEMPLATES.json").read_text())
                self.assertEqual(report["case_count"], 270)
                self.assertEqual(report["nonblind_source_visible_cases"], 54)
                self.assertFalse(report["real_independent_reviewer_enrolled"])
                self.assertFalse(report["candidate_responses_included"])
                self.assertEqual(report["independent_oracle_approvals"], 0)
                self.assertEqual(len(packets), len(templates))
                self.assertEqual(intake.sha256((dest / "reviewer-packets.json").read_bytes()),
                                 report["reviewer_packets_sha256"])
                with self.assertRaises(FileExistsError):
                    intake.prepare(self.freeze_path, dest)


if __name__ == "__main__":
    unittest.main()
