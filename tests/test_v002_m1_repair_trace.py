"""M1 conservative repair-trace contradiction checks.

These fixtures are NOT authenticated D2 transition attestations.
A structurally valid trace must still remain UNVERIFIED in the M1 bridge.
"""
import copy
import unittest

from policy_v002.m1_bridge import _check_unattested_repair_history


def baseline():
    state = {
        "head_subject": "head-fixture",
        "max_local_repairs": 2,
        "used_receipts": ["run-1", "run-2"],
        "repair_history": [{
            "task_id": "task-1",
            "prior_receipt": "run-1",
            "repair_number": 1,
            "head_subject": "head-fixture",
            "event_id": "event-3",
        }],
    }
    stages = ("CONSENT_GRANTED", "DISPATCH", "WORKER_REPORTED",
              "REPAIR_ORDERED", "WORKER_REPORTED", "VALIDATION_PASSED", "AUDIT_PASSED")
    actors = ("head-fixture", "head-fixture", "worker-fixture",
              "head-fixture", "worker-fixture", "validator-fixture", "auditor-fixture")
    history = [dict(event_id=f"event-{n}", kind=k, subject=actor)
               for n, (k, actor) in enumerate(zip(stages, actors))]
    orders = [dict(task_id="task-1", max_local_repairs=2)]
    workers = [dict(task_id="task-1", local_repairs=1)]
    return state, history, orders, workers


class ConservativeRepairTraceTests(unittest.TestCase):
    def setUp(self):
        self.state, self.history, self.orders, self.workers = copy.deepcopy(baseline())

    def verdict(self):
        return _check_unattested_repair_history(
            self.state, self.history, self.orders, self.workers)

    def test_consistent_synthetic_trace_remains_non_attested(self):
        # None means no contradiction only; it is never an authenticated PASS.
        self.assertIsNone(self.verdict())

    def test_forged_repair_without_journal_event(self):
        self.history.pop(3)
        self.assertEqual(self.verdict(), "REPAIR_EVENT_JOURNAL_MISMATCH")

    def test_replayed_head_event_id(self):
        self.history[3]["event_id"] = self.history[1]["event_id"]
        self.state["repair_history"][0]["event_id"] = self.history[1]["event_id"]
        self.assertEqual(self.verdict(), "REPAIR_EVENT_REPLAY")

    def test_wrong_repair_event_id(self):
        self.state["repair_history"][0]["event_id"] = "other-event"
        self.assertEqual(self.verdict(), "REPAIR_EVENT_JOURNAL_MISMATCH")

    def test_wrong_head_subject(self):
        self.history[3]["subject"] = "unauthorized-head"
        self.assertEqual(self.verdict(), "REPAIR_EVENT_JOURNAL_MISMATCH")

    def test_wrong_repair_request_subject(self):
        self.state["repair_history"][0]["head_subject"] = "other-head"
        self.assertEqual(self.verdict(), "REPAIR_EVENT_JOURNAL_MISMATCH")

    def test_changed_retry_worker(self):
        self.history[4]["subject"] = "impersonator"
        self.assertEqual(self.verdict(), "REPAIR_EVENT_JOURNAL_MISMATCH")

    def test_stale_unsupported_task(self):
        self.state["repair_history"][0]["task_id"] = "foreign-task"
        self.assertEqual(self.verdict(), "REPAIR_TASK_SCOPE_MISMATCH")

    def test_missing_prior_receipt(self):
        self.state["repair_history"][0]["prior_receipt"] = "unknown-receipt"
        self.assertEqual(self.verdict(), "REPAIR_RECEIPT_REPLAY")

    def test_duplicate_consumed_receipt(self):
        self.state["used_receipts"].append("run-1")
        self.assertEqual(self.verdict(), "REPAIR_RECEIPT_REPLAY")

    def test_wrong_worker_claimed_repair_count(self):
        self.workers[0]["local_repairs"] = 0
        self.assertEqual(self.verdict(), "REPAIR_COUNT_MISMATCH")

    def test_over_budget_number(self):
        self.state["repair_history"][0]["repair_number"] = 2
        self.assertEqual(self.verdict(), "REPAIR_BUDGET_EXCEEDED")

    def test_over_budget_allowed_worker(self):
        self.orders[0]["max_local_repairs"] = 0
        self.assertEqual(self.verdict(), "REPAIR_BUDGET_EXCEEDED")

    def test_repair_outside_journal_stage(self):
        self.history[2]["kind"] = "VALIDATION_PASSED"
        self.assertEqual(self.verdict(), "REPAIR_EVENT_JOURNAL_MISMATCH")


if __name__ == "__main__":
    unittest.main()
