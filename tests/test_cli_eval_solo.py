"""Owner-approved solo-development evaluation gate tests.

No tests here are actual model runs, human/AI grades or release acceptance.
"""
import unittest
from devtools import cli_eval as e


class SoloDeveloperEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.pairs=[(t,a) for t in
                    ("yellow-team:normal:01","orange-team:normal:01",
                     "green-team:normal:01","red-team:normal:01",
                     "blue-team:normal:01","purple-team:normal:01",
                     "white-team:normal:01","black-team:normal:01",
                     "gray-cell:normal:01")
                    for a in ("generic","full","no_directory","no_handoff")]
        self.f={"evaluation_mode":"SOLO_DEVELOPER","pilot_order":self.pairs,
                "oracle_independent_approvals":0,"oracle_review_receipts":[]}
        self.receipts=[{"case_id":cid,"arm":arm,"status":"COMPLETED"}
                       for cid,arm in self.pairs]

    def test_solo_accepts_only_complete_36_real_receipt_shapes(self):
        self.assertEqual(e.validate_solo_full_gate(self.f,self.receipts),
                         "SOLO_PILOT_EXECUTION_COMPLETE_NOT_QUALITY_CERTIFIED")

    def test_solo_rejects_missing_failed_duplicate_and_wrong_pairs(self):
        bads=[self.receipts[:-1],
              [*self.receipts[:-1],dict(self.receipts[-1],status="INVALID_TRACE")],
              [*self.receipts[:-1],self.receipts[0]],
              [*self.receipts[:-1],{"case_id":"unlisted:normal:01",
                                   "arm":"full","status":"COMPLETED"}]]
        for bad in bads:
            with self.subTest(bad=bad[-1]),self.assertRaises(e.Invalid):
                e.validate_solo_full_gate(self.f,bad)

    def test_cannot_self_sign_as_independent_or_combine_modes(self):
        for bad in [dict(self.f,evaluation_mode="EXTERNAL_INDEPENDENT"),
                    dict(self.f,oracle_independent_approvals=270),
                    dict(self.f,oracle_review_receipts=[{"fake":"yes"}])]:
            with self.subTest(bad=bad),self.assertRaises(e.Invalid):
                e.validate_solo_full_gate(bad,self.receipts)

    def test_existing_historical_freeze_is_not_solo(self):
        f=e.load(e.ROOT/e.EVAL/"CLI-EVAL-FREEZE-2026-11-04.json")
        self.assertNotEqual(f.get("evaluation_mode"),"SOLO_DEVELOPER")
        self.assertEqual(f["oracle_independent_approvals"],0)

    def test_ungraded_outputs_remain_unknown(self):
        case=e.corpus(e.ROOT)[0]
        metrics=e.ungraded(case)
        self.assertEqual(metrics["task_correctness"],"UNVERIFIED")
        self.assertEqual(metrics["unhinted_routing"],"NOT_OBSERVABLE")
        self.assertFalse(metrics["independent_grade"])
