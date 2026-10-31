"""M1 compatibility tests. All authority/provider data are synthetic fixtures."""
import copy
import unittest
from policy_v002.host_runtime import digest, HostRejected
from policy_v002.m1_bridge import reconcile_reference, VERSION
from test_v002_policy import fixture, FakeAdapter, SHA


class JournalFixture:
    def __init__(self, state, events):
        self.state, self.events = state, events
    def read(self, mission_id):
        return copy.deepcopy(self.state)
    def history(self, mission_id):
        return copy.deepcopy(self.events)


def scenario():
    data = fixture()
    mission = data["mission"]
    mission.update(allowed_teams=["yellow-team"],allowed_actions=["read"],
                   max_handoffs=0)
    intent = dict(mission_id="m1",repository="owner/repo",branch="design/new",
                  source_sha=SHA,allowed_teams=["yellow-team"],
                  required_teams=["yellow-team"],allowed_actions=["read","inspect"],
                  criteria=["criterion1"],max_handoffs=0)
    state = dict(intent,phase="HEAD_DECISION",task=None,revoked=False,
                 consent_id="fixture-grant",head_subject="head-fixture",
                 consent_digest=digest(intent),expires_at=2000000000,
                 used_task_ids=["t1"],used_receipts=["test:1"],revision=5,
                 approved_teams=["yellow-team"],validated_criteria=["criterion1"],
                 gates=[dict(phase=p,subject=role,task_id="t1",
                     criterion="criterion1",sha=SHA,evidence_ref="test:1",verdict="PASS")
                     for p,role in (("VALIDATE","validator-fixture"),
                                    ("INTERNAL_AUDIT","auditor-fixture"))])
    stages=[("grant","CONSENT_GRANTED"),("dispatch","DISPATCH"),
            ("report","WORKER_REPORTED"),("validate","VALIDATION_PASSED"),
            ("audit","AUDIT_PASSED")]
    subjects=("head-fixture", "head-fixture", "worker-fixture",
              "validator-fixture", "auditor-fixture")
    events=[dict(revision=i,event_id=e,kind=k,subject=subjects[i-1],
                 consent_id="fixture-grant" if i==1 else None)
            for i,(e,k) in enumerate(stages,1)]
    links=[dict(transition_id="tr"+str(i),journal_event_id=stages[i][0],
                journal_revision=i+1,task_id="t1",source_sha=SHA)
           for i in range(1,5)]
    return dict(data,journal=JournalFixture(state,events),
                event_links=links,clock=lambda:1700000000)


class M1BridgeTests(unittest.TestCase):
    def setUp(self):
        self.d = scenario()
    def check(self,status,code):
        v = reconcile_reference(**self.d)
        self.assertEqual((v.status,v.code),(status,code),v)
    def test_aligned_reference_remains_unverified(self):
        self.check("UNVERIFIED","REFERENCE_ALIGNED_AUTHORITY_UNVERIFIED")
    def test_even_fake_d2_pass_does_not_certify_host(self):
        self.d["trust"]=FakeAdapter()
        v=reconcile_reference(**self.d)
        self.assertEqual((v.status,v.code,v.policy_verdict),
                         ("UNVERIFIED","D2_REFERENCE_PASS_NOT_PRODUCTION_AUTH","PASS"))
    def test_no_journal(self):
        self.d["journal"]=None
        self.check("UNVERIFIED","JOURNAL_UNAVAILABLE")
    def test_revoked_consent(self):
        self.d["journal"].state["revoked"]=True
        self.check("BLOCKED","GRANT_REVOKED")
    def test_expired_consent(self):
        self.d["journal"].state["expires_at"]=1
        self.check("BLOCKED","GRANT_EXPIRED")
    def test_changed_source(self):
        self.d["journal"].state["source_sha"]="b"*40
        self.check("BLOCKED","MISSION_SCOPE_MISMATCH")
    def test_wrong_consent_digest(self):
        self.d["journal"].state["consent_digest"]="invalid"
        self.check("BLOCKED","CONSENT_MISMATCH")
    def test_missing_event_link(self):
        self.d["event_links"]=[]
        self.check("UNVERIFIED","M1_TRACE_OR_MIGRATION_UNAVAILABLE")
    def test_forged_transition_event(self):
        self.d["event_links"][2]["journal_revision"]=99
        self.check("BLOCKED","TRANSITION_LINK_MISMATCH")
    def test_missing_internal_audit(self):
        self.d["journal"].state["gates"].pop()
        self.check("UNVERIFIED","M1_TRACE_OR_MIGRATION_UNAVAILABLE")
    def test_wrong_gate_receipt(self):
        self.d["journal"].state["gates"][1]["evidence_ref"]="wrong"
        self.check("BLOCKED","GATE_RECEIPT_MISMATCH")
    def test_receipt_replay_or_substitution(self):
        self.d["journal"].state["used_receipts"]=["other"]
        self.check("BLOCKED","TASK_OR_RECEIPT_MISMATCH")
    def test_wrong_worker(self):
        self.d["worker_events"][0]["team"]="red-team"
        self.check("BLOCKED","TASK_OR_RECEIPT_MISMATCH")
    def test_head_not_idle(self):
        self.d["journal"].state["phase"]="WORKER_ACTIVE"
        self.check("BLOCKED","HEAD_PHASE_INVALID")
    def test_after_head_complete_requires_new_gate(self):
        self.d["journal"].state["phase"]="COMPLETE"
        self.check("BLOCKED","HEAD_PHASE_INVALID")
    def test_journal_revision_drift(self):
        self.d["journal"].state["revision"]=4
        self.check("BLOCKED","JOURNAL_TRACE_MISMATCH")
    def test_missing_accepted_team(self):
        self.d["journal"].state["approved_teams"]=[]
        self.check("BLOCKED","WORK_INCOMPLETE")
    def test_forged_aggregate_audit_record(self):
        self.d["gate_records"][1]["evidence_refs"]=["forged"]
        self.check("BLOCKED","AGGREGATE_GATE_INVALID")
    def test_write_requires_real_protected_host(self):
        self.d["mission"]["allowed_actions"]=["write_authorized_branch"]
        self.check("CAPABILITY_BLOCKED","PROTECTED_HOST_REQUIRED")
    def test_global_writer_lock_not_inferred(self):
        self.d["mission"]["requires_global_exclusive_write"]=True
        self.check("CAPABILITY_BLOCKED","PROTECTED_HOST_REQUIRED")
    def test_runner_not_a_runtime_dependency(self):
        self.d["mission"]["runner_required"]=True
        self.check("BLOCKED","INVALID_MISSION_SCOPE")
    def test_d2_failed_provider_remains_blocked(self):
        self.d["trust"]=FakeAdapter()
        self.d["trust"].sha="b"*40
        self.check("BLOCKED","D2_STALE_REVISION")
    def test_d2_unavailable_provider_unverified(self):
        self.d["trust"]=FakeAdapter()
        self.d["trust"].raise_auth=True
        self.assertEqual(reconcile_reference(**self.d).status,"UNVERIFIED")
    def test_journal_unavailable_fails_closed(self):
        def bad(_):
            raise HostRejected("JOURNAL_INTEGRITY_FAILURE")
        self.d["journal"].read=bad
        self.check("UNVERIFIED","JOURNAL_INTEGRITY_UNVERIFIED")
    def test_malformed_work_criterion_fails_closed(self):
        self.d["work_orders"][0]["criteria_ids"]=None
        self.check("BLOCKED","TASK_CRITERION_SCOPE_MISMATCH")
    def test_malformed_journal_event_fails_closed(self):
        self.d["journal"].events[2]=None
        self.check("BLOCKED","MALFORMED_REFERENCE_RECORD")
    def test_bad_head_role_claim_rejected(self):
        self.d["head_decision"]["actor"]="IMPOSTOR"
        self.check("BLOCKED","HEAD_DECISION_MISMATCH")
    def test_wrong_transition_actor_rejected(self):
        self.d["transition_events"][2]["actor"]="HEAD"
        self.check("BLOCKED","TRANSITION_ROLE_MISMATCH")
    def test_gate_actor_not_linked_to_journal_event(self):
        self.d["journal"].state["gates"][0]["subject"]="worker-fixture"
        self.check("BLOCKED","GATE_ACTOR_LINK_MISMATCH")
    def test_inconsistent_completion_flag_rejected(self):
        self.d["journal"].state["completion"]="INTERNAL_READ_ONLY_VERIFIED"
        self.check("BLOCKED","HEAD_PHASE_INVALID")
    def test_forged_head_dispatch_actor_rejected(self):
        self.d["journal"].events[1]["subject"]="impostor"
        self.check("BLOCKED","HEAD_DISPATCH_ACTOR_MISMATCH")
    def test_gate_reference_in_head_decision_rejected(self):
        self.d["head_decision"]["audit_record_ref"]="forged"
        self.check("BLOCKED","HEAD_DECISION_MISMATCH")
    def test_missing_journal_actor_rejected(self):
        self.d["journal"].events[2]["subject"]=""
        self.check("BLOCKED","JOURNAL_ACTOR_MISSING")
    def test_bridge_version_is_pinned(self):
        self.assertEqual(VERSION,"cto-v002-m1-bridge-5")


if __name__=="__main__":
    unittest.main()
