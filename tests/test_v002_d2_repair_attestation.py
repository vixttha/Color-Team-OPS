"""Orange/D2 hostile repair-transition and prior receipt contract tests.

Synthetic trusted-adapter doubles are NOT actual authenticated host evidence.
"""
import copy
import unittest
from dataclasses import replace

from policy_v002.verifier import evaluate_completion, TransitionAttestation, Observation
from policy_v002.repair_protocol import RepairAttestation, verify_repair_chain
from test_v002_policy import fixture, FakeAdapter, SHA


def scenario():
    d = fixture()
    d["worker_events"][0]["local_repairs"] = 1
    record = dict(schema_version="0.0.2-prototype", repair_id="rep-001",
                  mission_id="m1", task_id="t1", team="yellow-team",
                  source_sha=SHA, repair_number=1, head_transition_id="rep-head",
                  worker_transition_id="rep-worker", head_subject="head-fixture",
                  worker_subject="worker-fixture", prior_receipt="test:0",
                  next_receipt="test:1")
    d["repair_events"] = [record]
    trust = FakeAdapter()
    trust.repairs = {"rep-001": RepairAttestation(**{
        **{k: record[k] for k in ("mission_id", "repair_id", "task_id", "team",
            "source_sha", "repair_number", "head_subject", "worker_subject",
            "prior_receipt", "next_receipt")}, "valid": True
    })}
    trust.authenticate_repair = lambda repair_id: trust.repairs.get(repair_id)
    trust.transitions.update({
        "rep-head": TransitionAttestation("m1", "rep-head",
            "VALIDATION_PENDING", "WORKER_ACTIVE", "HEAD", SHA, "t1", "yellow-team", True),
        "rep-worker": TransitionAttestation("m1", "rep-worker",
            "WORKER_ACTIVE", "VALIDATION_PENDING", "WORKER", SHA, "t1", "yellow-team", True)
    })
    trust.observations[("github", "test:0")] = Observation(
        "m1", "t1", "github", "test:0", SHA, "criterion1", "FAIL")
    return d, trust


class RepairAttestationTests(unittest.TestCase):
    def setUp(self):
        self.d, self.trust = scenario()

    def verdict(self):
        return evaluate_completion(**self.d, trust=self.trust)

    def check(self, status, code):
        v = self.verdict()
        self.assertEqual((v.status, v.code), (status, code), v)

    def test_legitimate_retry_attested_by_synthetic_adapter_only(self):
        self.check("PASS", "INTERNAL_COMPLETION_VERIFIED")

    def test_missing_trusted_repair_attestation(self):
        self.trust.repairs.clear()
        self.check("UNVERIFIED", "REPAIR_ATTESTATION_UNAVAILABLE")

    def test_missing_repair_event_with_positive_worker_count(self):
        self.d["repair_events"] = []
        self.check("UNVERIFIED", "REPAIR_ATTESTATIONS_MISSING")

    def test_extra_forged_repair_event_without_worker_count(self):
        self.d["worker_events"][0]["local_repairs"] = 0
        self.check("BLOCKED", "REPAIR_ATTESTATIONS_UNEXPECTED")

    def test_forged_proof_issuer_refuses(self):
        self.trust.repairs["rep-001"] = replace(
            self.trust.repairs["rep-001"], valid=False)
        self.check("BLOCKED", "REPAIR_ATTESTATION_MISMATCH")

    def test_repair_identity_substitution(self):
        self.trust.repairs["rep-001"] = replace(
            self.trust.repairs["rep-001"], head_subject="impostor")
        self.check("BLOCKED", "REPAIR_ATTESTATION_MISMATCH")

    def test_wrong_task(self):
        self.d["repair_events"][0]["task_id"] = "foreign-task"
        self.check("BLOCKED", "REPAIR_SCOPE_MISMATCH")

    def test_wrong_source(self):
        self.d["repair_events"][0]["source_sha"] = "b" * 40
        self.check("BLOCKED", "REPAIR_SCOPE_MISMATCH")

    def test_wrong_final_receipt(self):
        self.d["repair_events"][0]["next_receipt"] = "not-final"
        self.check("BLOCKED", "REPAIR_FINAL_RECEIPT_MISMATCH")

    def test_missing_prior_receipt_provider_proof(self):
        self.trust.observations.pop(("github", "test:0"))
        self.check("UNVERIFIED", "REPAIR_PRIOR_RECEIPT_UNAVAILABLE")

    def test_cross_task_prior_receipt_substitution(self):
        self.trust.observations[("github", "test:0")] = replace(
            self.trust.observations[("github", "test:0")], task_id="t2")
        self.check("BLOCKED", "REPAIR_PRIOR_RECEIPT_SCOPE_MISMATCH")

    def test_forged_repair_transition_role(self):
        self.trust.transitions["rep-head"] = replace(
            self.trust.transitions["rep-head"], actor="WORKER")
        self.check("BLOCKED", "REPAIR_TRANSITION_SCOPE_MISMATCH")

    def test_worker_transition_missing(self):
        self.trust.transitions.pop("rep-worker")
        self.check("UNVERIFIED", "REPAIR_TRANSITION_UNAUTHENTICATED")

    def test_budget_exhausted(self):
        self.d["work_orders"][0]["max_local_repairs"] = 0
        self.check("BLOCKED", "REPAIR_BUDGET_EXCEEDED")

    def test_revoked_grant(self):
        self.trust.auth = replace(self.trust.auth, valid=False)
        self.check("BLOCKED", "AUTH_REVOKED")

    def test_same_head_and_worker_identity(self):
        self.d["repair_events"][0]["worker_subject"] = "head-fixture"
        self.check("BLOCKED", "REPAIR_SCOPE_MISMATCH")

    def test_schema_rejects_missing_head_transition(self):
        del self.d["repair_events"][0]["head_transition_id"]
        self.check("BLOCKED", "REPAIR_EVENT_SCHEMA_INVALID")

    def test_legacy_zero_repair_remains_valid(self):
        d = fixture()
        self.assertEqual(evaluate_completion(**d, trust=FakeAdapter()).status, "PASS")


if __name__ == "__main__":
    unittest.main()
