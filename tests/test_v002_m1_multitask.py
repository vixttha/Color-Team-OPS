"""M1 multi-assignment Yellow -> Orange -> Yellow source/journal correlation.

All principals, journal events and D2 attestations here are synthetic.
"""
import copy
from dataclasses import replace
import unittest

from policy_v002.m1_bridge import reconcile_reference, VERSION
from policy_v002.host_runtime import digest
from policy_v002.verifier import Observation, GateAttestation, TransitionAttestation
from test_v002_m1_bridge import scenario
from test_v002_policy import FakeAdapter, V, SHA

TEAMS=("yellow-team","orange-team","yellow-team")
TASKS=("t1","t2","t3")
CRITERIA=("criterion1","criterion2","criterion3")
CLAIMS=("c1","c2","c3")
RECEIPTS=("test:1","test:2","test:3")
PHASES=("VALIDATE","INTERNAL_AUDIT")
STAGES=(
 ("HEAD_READY","WORKER_ACTIVE","HEAD"),
 ("WORKER_ACTIVE","VALIDATION_PENDING","WORKER"),
 ("VALIDATION_PENDING","INTERNAL_AUDIT_PENDING","VALIDATOR"),
 ("INTERNAL_AUDIT_PENDING","HEAD_DECISION","INTERNAL_AUDITOR"),
)

def three_tasks():
    d=scenario()
    m=d["mission"]
    m.update(allowed_teams=["yellow-team","orange-team"],
             required_teams=["yellow-team","orange-team"],
             acceptance_criteria=list(CRITERIA),max_handoffs=2)
    state=d["journal"].state
    state.update(allowed_teams=list(m["allowed_teams"]),required_teams=list(m["required_teams"]),
        criteria=list(CRITERIA),max_handoffs=2,used_task_ids=list(TASKS),
        used_receipts=list(RECEIPTS),approved_teams=["yellow-team","orange-team"],
        validated_criteria=list(CRITERIA),revision=13)
    keys=("mission_id","repository","branch","source_sha","allowed_teams",
          "required_teams","allowed_actions","criteria","max_handoffs")
    state["consent_digest"]=digest({k:state[k] for k in keys})
    gates=[]; history=[d["journal"].events[0]]; links=[]; transitions=[]
    orders=[]; workers=[]; claims=[]
    for n,(team,task,criterion,claimid,receipt) in enumerate(
            zip(TEAMS,TASKS,CRITERIA,CLAIMS,RECEIPTS)):
        orders.append(dict(schema_version=V,mission_id=m["mission_id"],task_id=task,
            issued_by="HEAD",team=team,source_sha=SHA,scope_actions=["read"],
            criteria_ids=[criterion],max_local_repairs=2,
            authorization_ref=m["authorization_ref"]))
        workers.append(dict(schema_version=V,event_id="worker-"+task,mission_id=m["mission_id"],
            task_id=task,team=team,source_sha=SHA,outcome="DONE",
            evidence_claim_ids=[claimid],summary="completed",local_repairs=0))
        claims.append(dict(schema_version=V,claim_id=claimid,mission_id=m["mission_id"],
            task_id=task,source_sha=SHA,provider="github",
            provider_record_id=receipt,claim="verified in fixture",claimed_by="worker"))
        for i,phase in enumerate(PHASES):
            subject=("validator-fixture" if i==0 else "auditor-fixture")
            gates.append(dict(phase=phase,subject=subject,task_id=task,
                criterion=criterion,sha=SHA,evidence_ref=receipt,verdict="PASS"))
        for i,(prior,after,who) in enumerate(STAGES):
            if n and i==0: prior="HEAD_DECISION"
            revision=2+4*n+i
            kind=("DISPATCH","WORKER_REPORTED","VALIDATION_PASSED","AUDIT_PASSED")[i]
            subject=("head-fixture","worker-fixture","validator-fixture","auditor-fixture")[i]
            eid=f"e-{task}-{i}"
            tid=f"tr-{task}-{i}"
            history.append(dict(revision=revision,event_id=eid,kind=kind,subject=subject))
            links.append(dict(transition_id=tid,journal_event_id=eid,
                journal_revision=revision,task_id=task,source_sha=SHA))
            transitions.append(dict(schema_version=V,transition_id=tid,
                mission_id=m["mission_id"],from_phase=prior,to_phase=after,
                actor=who,source_sha=SHA,reason="synthetic staged flow"))
    state["gates"]=gates
    d["journal"].events=history
    d.update(work_orders=orders,worker_events=workers,evidence_claims=claims,
             transition_events=transitions,event_links=links)
    for g in d["gate_records"]:
        g["criterion_ids"]=list(CRITERIA)
        g["evidence_refs"]=list(CLAIMS)
    return d

def fake_for_three(d):
    fake=FakeAdapter()
    fake.auth=replace(fake.auth,
        approved_task_ids=frozenset(TASKS),
        teams=frozenset(("yellow-team","orange-team")))
    fake.dispatches={(d["mission"]["mission_id"],task,team,SHA)
                     for task,team in zip(TASKS,TEAMS)}
    for n in range(3):
        fake.observations[("github",RECEIPTS[n])]=Observation("m1",TASKS[n],"github",
                        RECEIPTS[n],SHA,CRITERIA[n],"PASS")
    for p,ref in (("VALIDATE","v1"),("INTERNAL_AUDIT","a1")):
        old=fake.gates[ref]
        fake.gates[ref]=replace(old,criterion_ids=frozenset(CRITERIA),
                             evidence_refs=frozenset(CLAIMS))
    fake.transitions={
        step["transition_id"]:TransitionAttestation("m1",step["transition_id"],
          step["from_phase"],step["to_phase"],step["actor"],SHA,
          TASKS[i//4],TEAMS[i//4],True)
        for i,step in enumerate(d["transition_events"])
    }
    return fake

class MultiTaskBridgeTests(unittest.TestCase):
    def setUp(self):
        self.d=three_tasks()

    def check(self,status,code):
        v=reconcile_reference(**self.d)
        self.assertEqual((v.status,v.code),(status,code),v)

    def test_three_tasks_repeat_yellow_structurally_aligned(self):
        self.check("UNVERIFIED","REFERENCE_ALIGNED_AUTHORITY_UNVERIFIED")
    def test_fake_d2_pass_never_establishes_production_auth(self):
        self.d["trust"]=fake_for_three(self.d)
        v=reconcile_reference(**self.d)
        self.assertEqual((v.status,v.code,v.policy_verdict),
            ("UNVERIFIED","D2_REFERENCE_PASS_NOT_PRODUCTION_AUTH","PASS"),v)
    def test_second_dispatch_comes_from_head_decision(self):
        self.d["transition_events"][4]["from_phase"]="HEAD_READY"
        self.check("BLOCKED","TRANSITION_ROLE_MISMATCH")
    def test_duplicate_team_identity_not_added_twice(self):
        self.assertEqual(self.d["journal"].state["approved_teams"],["yellow-team","orange-team"])
        self.check("UNVERIFIED","REFERENCE_ALIGNED_AUTHORITY_UNVERIFIED")
    def test_replay_second_receipt(self):
        self.d["evidence_claims"][1]["provider_record_id"]=RECEIPTS[0]
        self.check("BLOCKED","TASK_OR_RECEIPT_MISMATCH")
    def test_replay_task_id(self):
        self.d["work_orders"][2]["task_id"]="t1"
        self.check("BLOCKED","TASK_OR_RECEIPT_MISMATCH")
    def test_replayed_event_id_rejected(self):
        # Keep the transition link internally consistent; otherwise a broken
        # link (correctly) rejects before the duplicate-event guard is reached.
        replayed=self.d["journal"].events[1]["event_id"]
        self.d["journal"].events[9]["event_id"]=replayed
        self.d["event_links"][8]["journal_event_id"]=replayed
        self.check("BLOCKED","JOURNAL_EVENT_REPLAY")
    def test_wrong_second_task_audit_subject(self):
        self.d["journal"].state["gates"][3]["subject"]="impostor"
        self.check("BLOCKED","GATE_ACTOR_LINK_MISMATCH")
    def test_second_task_wrong_claim_mission(self):
        self.d["evidence_claims"][1]["mission_id"]="other"
        self.check("BLOCKED","TASK_OR_RECEIPT_MISMATCH")
    def test_third_task_stale_sha(self):
        self.d["transition_events"][11]["source_sha"]="b"*40
        self.check("BLOCKED","TRANSITION_LINK_MISMATCH")
    def test_active_worker_refuses_closure(self):
        self.d["journal"].state["phase"]="WORKER_ACTIVE"
        self.check("BLOCKED","HEAD_PHASE_INVALID")
    def test_handoff_budget_exhausted(self):
        self.d["mission"]["max_handoffs"]=1
        self.d["journal"].state["max_handoffs"]=1
        self.d["journal"].state["consent_digest"]=digest({
            k:self.d["journal"].state[k] for k in (
              "mission_id","repository","branch","source_sha","allowed_teams",
              "required_teams","allowed_actions","criteria","max_handoffs")})
        self.check("BLOCKED","HANDOFF_BUDGET_EXCEEDED")
    def test_third_task_missing_audit(self):
        self.d["journal"].state["gates"].pop()
        self.check("UNVERIFIED","M1_TRACE_OR_MIGRATION_UNAVAILABLE")
    def test_missing_second_task_event(self):
        self.d["journal"].events.pop(8)
        self.check("UNVERIFIED","M1_TRACE_OR_MIGRATION_UNAVAILABLE")
    def test_third_task_receipt_mismatch(self):
        self.d["journal"].state["gates"][-1]["evidence_ref"]="wrong-receipt"
        self.check("BLOCKED","GATE_RECEIPT_MISMATCH")
    def test_approved_team_summary_cannot_list_yellow_twice(self):
        self.d["journal"].state["approved_teams"]=["yellow-team","orange-team","yellow-team"]
        self.check("BLOCKED","TEAM_SUMMARY_MISMATCH")
    def test_recorded_local_repairs_cannot_be_implied_by_label(self):
        self.d["worker_events"][1]["local_repairs"]=1
        self.check("UNVERIFIED","REPAIR_EVENT_TRACE_UNAVAILABLE")
    def test_overbudget_local_repairs_rejected(self):
        self.d["worker_events"][1]["local_repairs"]=3
        self.check("BLOCKED","REPAIR_BUDGET_EXCEEDED")
    def test_wrong_aggregate_audit_receipt(self):
        self.d["gate_records"][1]["evidence_refs"]=["c1"]
        self.check("BLOCKED","AGGREGATE_GATE_INVALID")
    def test_revoked_mission_stops(self):
        self.d["journal"].state["revoked"]=True
        self.check("BLOCKED","GRANT_REVOKED")
    def test_expired_grant_stops(self):
        self.d["journal"].state["expires_at"]=1
        self.check("BLOCKED","GRANT_EXPIRED")
    def test_optional_repair_grant_digest_is_checked(self):
        self.d["journal"].state["max_local_repairs"]=2
        keys=("mission_id","repository","branch","source_sha","allowed_teams",
              "required_teams","allowed_actions","criteria","max_handoffs",
              "max_local_repairs")
        self.d["journal"].state["consent_digest"]=digest(
            {k:self.d["journal"].state[k] for k in keys})
        self.check("UNVERIFIED","REFERENCE_ALIGNED_AUTHORITY_UNVERIFIED")
    def test_forged_repair_history_without_journal_event_blocked(self):
        self.d["journal"].state["repair_history"]=[dict(task_id="t2",
            prior_receipt="test:pre",repair_number=1)]
        self.check("BLOCKED","REPAIR_EVENT_JOURNAL_MISMATCH")
    def test_signed_repair_budget_cannot_exceed_d2_scope(self):
        self.d["journal"].state["max_local_repairs"]=3
        keys=("mission_id","repository","branch","source_sha","allowed_teams",
              "required_teams","allowed_actions","criteria","max_handoffs",
              "max_local_repairs")
        self.d["journal"].state["consent_digest"]=digest(
            {k:self.d["journal"].state[k] for k in keys})
        self.check("BLOCKED","REPAIR_CONSENT_SCOPE_MISMATCH")
    def test_version(self):
        self.assertEqual(VERSION,"cto-v002-m1-bridge-6")

if __name__=="__main__":
    unittest.main()
