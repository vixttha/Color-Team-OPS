"""D2 deterministic policy regression suite.

FakeAdapter is intentionally UNTRUSTED/synthetic; no production authentication
or GitHub/cloud integration is claimed by these tests.
"""
import copy
from dataclasses import replace
import unittest

from policy_v002.verifier import (
    Authorization, GateAttestation, Observation, TransitionAttestation, MissionSnapshot, evaluate_completion
)

SHA = "a" * 40
OTHER_SHA = "b" * 40
V = "0.0.2-prototype"


class FakeAdapter:
    """Synthetic test double, NOT a real authenticated provider adapter."""
    def __init__(self):
        self.auth = Authorization(
            "m1", "ref1", "owner/repo", "design/new", SHA,
            "verified-host-principal", frozenset(("yellow-team", "orange-team")),
            frozenset(("read", "propose_patch")), frozenset(("d1",)),
            frozenset(("t1",)), True
        )
        self.sha = SHA
        self.reads = 0
        self.advance_after_first = False
        self.dispatches = {("m1", "t1", "yellow-team", SHA)}
        self.observations = {
            ("github", "test:1"): Observation("m1", "t1", "github", "test:1", SHA, "criterion1", "PASS")
        }
        self.gates = {
            "v1": GateAttestation("m1", "v1", "VALIDATE", "PASS", SHA,
                                 frozenset(("criterion1",)), frozenset(("c1",)), "VALIDATOR", True),
            "a1": GateAttestation("m1", "a1", "INTERNAL_AUDIT", "PASS", SHA,
                                 frozenset(("criterion1",)), frozenset(("c1",)), "INTERNAL_AUDITOR", True),
        }
        self.exclusive = False
        self.snapshot = MissionSnapshot("m1", "HEAD_DECISION", None, None, SHA, True)
        self.transitions = {
            ("tr" + str(i)): TransitionAttestation(
                "m1", "tr" + str(i), before, after, who, SHA, "t1", "yellow-team", True
            )
            for i, (before, after, who) in enumerate((
                ("HEAD_READY", "WORKER_ACTIVE", "HEAD"),
                ("WORKER_ACTIVE", "VALIDATION_PENDING", "WORKER"),
                ("VALIDATION_PENDING", "INTERNAL_AUDIT_PENDING", "VALIDATOR"),
                ("INTERNAL_AUDIT_PENDING", "HEAD_DECISION", "INTERNAL_AUDITOR"),
            ), 1)
        }
        self.raise_auth = False

    def authorization(self, mission_id, authorization_ref):
        if self.raise_auth:
            raise TimeoutError("synthetic provider unavailable")
        return self.auth
    def current_sha(self, repository, branch):
        self.reads += 1
        if self.advance_after_first and self.reads > 1:
            return OTHER_SHA
        return self.sha
    def authorized_dispatch(self, mission_id, task_id, team, source_sha):
        return (mission_id, task_id, team, source_sha) in self.dispatches
    def resolve_observation(self, provider, provider_record_id):
        return self.observations.get((provider, provider_record_id))
    def authenticate_gate(self, record_id):
        return self.gates.get(record_id)
    def exclusive_write_enforced(self, mission_id, repository, branch):
        return self.exclusive
    def authenticate_transition(self, transition_id):
        return self.transitions.get(transition_id)
    def mission_snapshot(self, mission_id):
        return self.snapshot


def fixture():
    mission = dict(schema_version=V, mission_id="m1", host="chatgpt", goal="implement",
        repository="owner/repo", source_sha=SHA, authorized_branch="design/new",
        authorization_ref="ref1", allowed_teams=["yellow-team", "orange-team"],
        required_teams=["yellow-team"], allowed_actions=["read", "propose_patch"],
        max_handoffs=4, max_local_repairs=2, cloud_only=True,
        runner_required=False, mode="SKILLS_ONLY", state="AUTHORIZED",
        acceptance_criteria=["criterion1"])
    work = [dict(schema_version=V, mission_id="m1", task_id="t1", issued_by="HEAD",
        team="yellow-team", source_sha=SHA, scope_actions=["read"],
        criteria_ids=["criterion1"], max_local_repairs=2, authorization_ref="ref1")]
    workers = [dict(schema_version=V,event_id="e1",mission_id="m1",task_id="t1",
        team="yellow-team",source_sha=SHA,outcome="DONE",
        evidence_claim_ids=["c1"],summary="done",local_repairs=0)]
    claims = [dict(schema_version=V,claim_id="c1",mission_id="m1",task_id="t1",
        source_sha=SHA,provider="github",provider_record_id="test:1",
        claim="test ran",claimed_by="worker")]
    gates = [
        dict(schema_version=V,record_id="v1",mission_id="m1",phase="VALIDATE",
             verdict="PASS",source_sha=SHA,criterion_ids=["criterion1"],
             evidence_refs=["c1"],verifier_ref="trusted:validator",
             verified_at="2026-10-30T01:00:00Z"),
        dict(schema_version=V,record_id="a1",mission_id="m1",phase="INTERNAL_AUDIT",
             verdict="PASS",source_sha=SHA,criterion_ids=["criterion1"],
             evidence_refs=["c1"],verifier_ref="trusted:auditor",
             verified_at="2026-10-30T01:00:01Z")
    ]
    decision = dict(schema_version=V,decision_id="d1",mission_id="m1",actor="HEAD",
         action="COMPLETE",reason="verified",source_sha=SHA,
         validation_record_ref="v1",audit_record_ref="a1")
    transitions = [
        dict(schema_version=V, transition_id="tr" + str(i),
             mission_id="m1", from_phase=before, to_phase=after,
             actor=who, source_sha=SHA, reason="bounded stage")
        for i, (before, after, who) in enumerate((
            ("HEAD_READY", "WORKER_ACTIVE", "HEAD"),
            ("WORKER_ACTIVE", "VALIDATION_PENDING", "WORKER"),
            ("VALIDATION_PENDING", "INTERNAL_AUDIT_PENDING", "VALIDATOR"),
            ("INTERNAL_AUDIT_PENDING", "HEAD_DECISION", "INTERNAL_AUDITOR"),
        ), 1)
    ]
    return dict(transition_events=transitions,mission=mission,work_orders=work,worker_events=workers,
                evidence_claims=claims,gate_records=gates,head_decision=decision)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()
        self.trust = FakeAdapter()

    def result(self):
        return evaluate_completion(**self.data, trust=self.trust)

    def assert_outcome(self, status, code=None):
        v = self.result()
        self.assertEqual(v.status, status, v)
        if code:
            self.assertEqual(v.code, code, v)

    def test_live_mission_phase_must_be_head_decision(self):
        self.trust.snapshot = replace(self.trust.snapshot, phase="WORKER_ACTIVE",
                                      active_team="yellow-team", active_task_id="t1")
        self.assert_outcome("BLOCKED", "MISSION_STATE_MISMATCH")
    def test_snapshot_missing_unverified(self):
        self.trust.snapshot = None
        self.assert_outcome("UNVERIFIED", "MISSION_STATE_UNAVAILABLE")
    def test_stale_active_worker_at_finish_rejected(self):
        self.trust.snapshot = replace(self.trust.snapshot, active_team="orange-team")
        self.assert_outcome("BLOCKED", "MISSION_STATE_MISMATCH")
    def test_missing_transition_rejected(self):
        self.data["transition_events"].pop()
        self.assert_outcome("BLOCKED", "MISSION_TRACE_INVALID")
    def test_worker_skips_validation_rejected(self):
        self.data["transition_events"][1]["to_phase"] = "HEAD_DECISION"
        self.assert_outcome("BLOCKED", "INVALID_SHAPE")
    def test_reordered_transition_rejected(self):
        a=self.data["transition_events"]
        a[1],a[2] = a[2],a[1]
        self.assert_outcome("BLOCKED", "MISSION_TRACE_INVALID")
    def test_fabricated_transition_unverified(self):
        self.trust.transitions.pop("tr2")
        self.assert_outcome("UNVERIFIED", "TRANSITION_UNAUTHENTICATED")
    def test_attested_worker_team_mismatch(self):
        self.trust.transitions["tr2"] = replace(self.trust.transitions["tr2"], team="orange-team")
        self.assert_outcome("BLOCKED", "TRANSITION_ATTESTATION_MISMATCH")
    def test_attested_actor_role_mismatch(self):
        self.trust.transitions["tr3"] = replace(self.trust.transitions["tr3"], actor="WORKER")
        self.assert_outcome("BLOCKED", "TRANSITION_ATTESTATION_MISMATCH")
    def test_claimless_required_worker_rejected(self):
        self.data["worker_events"][0]["evidence_claim_ids"] = []
        self.assert_outcome("BLOCKED", "REQUIRED_WORK_UNVERIFIED")
    def test_clean_internal_completion(self):
        self.assert_outcome("PASS", "INTERNAL_COMPLETION_VERIFIED")
    def test_external_approval_separate_from_internal_completion(self):
        d = self.data["head_decision"]
        d["action"] = "BLOCKED_EXTERNAL_APPROVAL"
        d["external_approval_required"] = True
        self.assert_outcome("BLOCKED_EXTERNAL_APPROVAL", "RELEASE_APPROVAL_OUTSTANDING")
    def test_no_mission_authorization(self):
        self.trust.auth = None
        self.assert_outcome("UNVERIFIED", "AUTH_UNAVAILABLE")
    def test_revoked_authorization(self):
        self.trust.auth = replace(self.trust.auth, valid=False)
        self.assert_outcome("BLOCKED", "AUTH_REVOKED")
    def test_wrong_authorized_repository(self):
        self.trust.auth = replace(self.trust.auth, repository="other/repo")
        self.assert_outcome("BLOCKED", "AUTH_SCOPE_MISMATCH")
    def test_forged_head_label_has_no_trusted_decision(self):
        self.trust.auth = replace(self.trust.auth, approved_head_decisions=frozenset())
        self.assert_outcome("BLOCKED", "NOT_AUTHORIZED")
    def test_draft_mission_cannot_be_completed(self):
        self.data["mission"]["state"] = "DRAFT"
        self.assert_outcome("BLOCKED", "MISSION_NOT_AUTHORIZED")
    def test_wrong_source_revision_from_provider(self):
        self.trust.sha = OTHER_SHA
        self.assert_outcome("BLOCKED", "STALE_REVISION")
    def test_revision_changes_during_verification(self):
        self.trust.advance_after_first = True
        self.assert_outcome("BLOCKED", "REVISION_CHANGED_DURING_CHECK")
    def test_repair_budget_exceeded(self):
        self.data["worker_events"][0]["local_repairs"] = 3
        self.assert_outcome("BLOCKED", "WORKER_RESULT_INVALID")
    def test_wrong_worker_team(self):
        self.data["worker_events"][0]["team"] = "orange-team"
        self.assert_outcome("BLOCKED", "WORKER_RESULT_INVALID")
    def test_required_team_absent(self):
        self.data["mission"]["required_teams"] = ["orange-team"]
        self.assert_outcome("BLOCKED", "REQUIRED_WORK_INCOMPLETE")
    def test_required_teams_must_be_allowed(self):
        self.data["mission"]["required_teams"] = ["red-team"]
        self.assert_outcome("BLOCKED", "TEAM_SET_INVALID")
    def test_dispatch_cannot_be_fabricated_from_issued_by(self):
        self.trust.dispatches = set()
        self.assert_outcome("BLOCKED", "DISPATCH_NOT_AUTHORIZED")
    def test_untrusted_task_not_in_authorization(self):
        self.trust.auth = replace(self.trust.auth, approved_task_ids=frozenset())
        self.assert_outcome("BLOCKED", "WORK_SCOPE_MISMATCH")
    def test_unapproved_task_action(self):
        self.data["work_orders"][0]["scope_actions"] = ["open_draft_pr"]
        self.assert_outcome("BLOCKED", "WORK_SCOPE_MISMATCH")
    def test_duplicate_work_events(self):
        self.data["worker_events"].append(copy.deepcopy(self.data["worker_events"][0]))
        self.assert_outcome("BLOCKED", "DUPLICATE_RECORD")
    def test_two_events_one_task_even_different_ids(self):
        e = copy.deepcopy(self.data["worker_events"][0]); e["event_id"] = "e2"
        self.data["worker_events"].append(e)
        self.assert_outcome("BLOCKED", "MULTIPLE_TASK_RESULTS")
    def test_missing_worker_event(self):
        self.data["worker_events"] = []
        self.assert_outcome("BLOCKED", "MISSING_WORK")
    def test_false_worker_done_not_enough_without_claim(self):
        self.data["worker_events"][0]["evidence_claim_ids"] = []
        self.assert_outcome("BLOCKED", "REQUIRED_WORK_UNVERIFIED")
    def test_missing_provider_observation(self):
        self.trust.observations = {}
        self.assert_outcome("UNVERIFIED", "EVIDENCE_UNAVAILABLE")
    def test_provider_observation_old_sha(self):
        old = self.trust.observations[("github", "test:1")]
        self.trust.observations[("github", "test:1")] = replace(old, source_sha=OTHER_SHA)
        self.assert_outcome("BLOCKED", "EVIDENCE_SCOPE_MISMATCH")
    def test_provider_fails_criterion(self):
        old = self.trust.observations[("github", "test:1")]
        self.trust.observations[("github", "test:1")] = replace(old, outcome="FAIL")
        self.assert_outcome("BLOCKED", "CRITERION_FAILED")
    def test_provider_cannot_confirm_criterion(self):
        old = self.trust.observations[("github", "test:1")]
        self.trust.observations[("github", "test:1")] = replace(old, outcome="UNVERIFIED")
        self.assert_outcome("UNVERIFIED", "CRITERION_UNVERIFIED")
    def test_criterion_not_covered(self):
        self.data["mission"]["acceptance_criteria"].append("criterion2")
        self.assert_outcome("UNVERIFIED", "CRITERIA_NOT_COVERED")
    def test_missing_audit_gate(self):
        self.data["gate_records"] = self.data["gate_records"][:1]
        self.assert_outcome("BLOCKED", "MISSING_GATE")
    def test_gate_reference_spoof(self):
        self.data["head_decision"]["audit_record_ref"] = "fabricated"
        self.assert_outcome("BLOCKED", "GATE_REF_MISMATCH")
    def test_forged_gate_pass_record_not_attested(self):
        self.trust.gates["a1"] = None
        self.assert_outcome("UNVERIFIED", "GATE_UNAUTHENTICATED")
    def test_wrong_attested_auditor_role(self):
        self.trust.gates["a1"] = replace(self.trust.gates["a1"], role="VALIDATOR")
        self.assert_outcome("BLOCKED", "GATE_ATTESTATION_MISMATCH")
    def test_attested_gate_wrong_sha(self):
        self.trust.gates["a1"] = replace(self.trust.gates["a1"], source_sha=OTHER_SHA)
        self.assert_outcome("BLOCKED", "GATE_ATTESTATION_MISMATCH")
    def test_worker_cannot_set_gate_verdict(self):
        self.data["worker_events"][0]["outcome"] = "PASS"
        self.assert_outcome("BLOCKED", "INVALID_SHAPE")
    def test_head_decision_wrong_mission(self):
        self.data["head_decision"]["mission_id"] = "other"
        self.assert_outcome("BLOCKED", "DECISION_MISMATCH")
    def test_missing_exclusive_write_gateway(self):
        self.data["mission"]["mode"] = "ENFORCED_CLOUD"
        self.data["mission"]["requires_global_exclusive_write"] = True
        self.assert_outcome("CAPABILITY_BLOCKED", "EXCLUSIVE_WRITE_NOT_ENFORCED")
    def test_exclusive_write_fixture_cannot_make_production_claim(self):
        self.data["mission"]["mode"] = "ENFORCED_CLOUD"
        self.data["mission"]["requires_global_exclusive_write"] = True
        self.trust.exclusive = True  # Synthetic capability only; result simulated.
        self.assert_outcome("PASS", "INTERNAL_COMPLETION_VERIFIED")
    def test_trusted_provider_timeout(self):
        self.trust.raise_auth = True
        self.assert_outcome("UNVERIFIED", "TRUST_ADAPTER_ERROR")
    def test_fake_complete_with_no_gates_fails(self):
        self.data["gate_records"] = []
        self.assert_outcome("BLOCKED", "MISSING_GATE")
    def test_missing_acceptance_criteria_rejected_by_schema(self):
        self.data["mission"]["acceptance_criteria"] = []
        self.assert_outcome("BLOCKED", "INVALID_SHAPE")
    def test_json_shape_does_not_authenticate_provenance(self):
        # Same syntactically correct record; remove actual provider truth.
        self.trust.observations = {}
        self.assert_outcome("UNVERIFIED", "EVIDENCE_UNAVAILABLE")
    def test_unrequested_head_action_never_completes(self):
        self.data["head_decision"]["action"] = "BLOCK"
        self.assert_outcome("BLOCKED", "NOT_COMPLETION_ACTION")
    def test_wrong_authorization_ref_on_task(self):
        self.data["work_orders"][0]["authorization_ref"] = "worker-made-up-ref"
        self.assert_outcome("BLOCKED", "WORK_SCOPE_MISMATCH")
    def test_worker_mismatched_revision(self):
        self.data["worker_events"][0]["source_sha"] = OTHER_SHA
        self.assert_outcome("BLOCKED", "WORKER_RESULT_INVALID")
    def test_gate_mismatched_revision(self):
        self.data["gate_records"][1]["source_sha"] = OTHER_SHA
        self.assert_outcome("BLOCKED", "GATE_INVALID")
    def test_evidence_claim_id_mismatch(self):
        self.data["evidence_claims"][0]["claim_id"] = "other-claim"
        self.assert_outcome("BLOCKED", "CLAIM_LINKAGE_INVALID")

if __name__ == "__main__":
    unittest.main()
