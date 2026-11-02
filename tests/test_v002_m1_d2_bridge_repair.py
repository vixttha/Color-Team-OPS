"""M1 journal + D2 attested retry bridge (synthetic, not production authority)."""
import unittest
from policy_v002.m1_bridge import reconcile_reference
from policy_v002.host_runtime import digest
from policy_v002.repair_protocol import RepairAttestation
from policy_v002.verifier import TransitionAttestation, Observation
from test_v002_m1_bridge import scenario
from test_v002_policy import FakeAdapter, SHA


def one_repair():
    d = scenario()
    state = d["journal"].state
    state["max_local_repairs"] = 1
    keys = ("mission_id","repository","branch","source_sha",
            "allowed_teams","required_teams","allowed_actions",
            "criteria","max_handoffs","max_local_repairs")
    state["consent_digest"] = digest({key:state[key] for key in keys})
    state["repair_history"] = [dict(
        task_id="t1",prior_receipt="test:pre",repair_number=1,
        head_subject="head-fixture",event_id="repair-log-1")]
    state["used_receipts"] = ["test:pre","test:1"]
    state["revision"] = 7
    d["worker_events"][0]["local_repairs"] = 1
    events=d["journal"].events
    events.insert(2,dict(revision=3,event_id="report-pre",
                         kind="WORKER_REPORTED",subject="worker-fixture",receipt="test:pre"))
    events.insert(3,dict(revision=4,event_id="repair-log-1",
                         kind="REPAIR_ORDERED",subject="head-fixture"))
    # Original final report now occurs after the actual Head repair.
    for i,e in enumerate(events):
        e["revision"]=i+1
    record=dict(schema_version="0.0.2-prototype",repair_id="r1",
                mission_id="m1",task_id="t1",team="yellow-team",
                source_sha=SHA,repair_number=1,journal_event_id="repair-log-1",
                head_transition_id="h1",worker_transition_id="w1",
                head_subject="head-fixture",worker_subject="worker-fixture",
                prior_receipt="test:pre",next_receipt="test:1")
    d["repair_events"]=[record]
    trust=FakeAdapter()
    trust.authenticate_repair = lambda rid: RepairAttestation(
        "m1","r1","t1","yellow-team",SHA,1,"repair-log-1",
        "head-fixture","worker-fixture","test:pre","test:1",True) if rid=="r1" else None
    trust.transitions.update({
        "h1":TransitionAttestation("m1","h1","VALIDATION_PENDING","WORKER_ACTIVE","HEAD",
                                   SHA,"t1","yellow-team",True),
        "w1":TransitionAttestation("m1","w1","WORKER_ACTIVE","VALIDATION_PENDING","WORKER",
                                   SHA,"t1","yellow-team",True)
    })
    trust.observations[("github","test:pre")]=Observation(
        "m1","t1","github","test:pre",SHA,"criterion1","FAIL")
    return d,trust


class RepairBridgeTests(unittest.TestCase):
    def test_repaired_reference_remains_unverified_without_trusted_adapter(self):
        d,_ = one_repair()
        v = reconcile_reference(**d)
        self.assertEqual((v.status,v.code),
                         ("UNVERIFIED","REPAIR_EVENT_TRACE_UNAVAILABLE"))

    def test_all_consistent_attestations_still_not_production_authority(self):
        d,trust = one_repair()
        v = reconcile_reference(**d,trust=trust)
        self.assertEqual((v.status,v.code,v.policy_verdict),
                         ("UNVERIFIED","D2_REPAIR_REFERENCE_NOT_PRODUCTION_AUTH","PASS"))

    def test_wrong_journal_repair_event_cannot_be_rebound(self):
        d,trust = one_repair()
        d["repair_events"][0]["journal_event_id"]="foreign-event"
        v=reconcile_reference(**d,trust=trust)
        self.assertEqual((v.status,v.code),
                         ("BLOCKED","REPAIR_JOURNAL_PROOF_MISMATCH"))

    def test_different_worker_forgery_rejected_before_reference_pass(self):
        d,trust=one_repair()
        d["repair_events"][0]["worker_subject"]="foreign-worker"
        v=reconcile_reference(**d,trust=trust)
        self.assertEqual((v.status,v.code),
                         ("BLOCKED","REPAIR_WORKER_PROOF_MISMATCH"))


if __name__=="__main__":
    unittest.main()
