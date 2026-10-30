"""Future v0.0.2 standalone schema tests. No plugin runtime, no network."""
import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1] / "contracts" / "v0.0.2"
SHA = "a" * 40
BASE = {"schema_version": "0.0.2-prototype"}
def validate(schema, payload):
    data = json.loads((ROOT / (schema + ".schema.json")).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(data)
    return list(Draft202012Validator(data).iter_errors(payload))
def okay(schema, payload):
    errors = validate(schema, payload)
    assert not errors, [str(e) for e in errors]
def rejected(schema, payload):
    assert validate(schema, payload), (schema, payload)

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.mission = dict(BASE, mission_id="m1", host="chatgpt", goal="build safely",
             allowed_teams=["yellow-team", "orange-team"], required_teams=["yellow-team"],
             allowed_actions=["read", "propose_patch"], max_handoffs=3, max_local_repairs=2,
             cloud_only=True, runner_required=False, mode="SKILLS_ONLY",
             state="DRAFT", acceptance_criteria=["criterion1"])
        self.work = dict(BASE, mission_id="m1", task_id="t1", issued_by="HEAD",
             team="yellow-team", source_sha=SHA, scope_actions=["read"],
             criteria_ids=["criterion1"], max_local_repairs=1, authorization_ref="ref1")
        self.worker = dict(BASE,event_id="e1",mission_id="m1",task_id="t1",team="yellow-team",
             source_sha=SHA,outcome="DONE",evidence_claim_ids=[],summary="done",local_repairs=0)
        self.claim = dict(BASE,claim_id="c1",mission_id="m1",task_id="t1",source_sha=SHA,
             provider="github",provider_record_id="run:1",claim="tests passed",claimed_by="worker")
        self.gate = dict(BASE,record_id="g1",mission_id="m1",phase="VALIDATE",verdict="UNVERIFIED",
             source_sha=SHA,criterion_ids=["criterion1"],evidence_refs=[],
             verifier_ref="connector-principal",verified_at="2026-10-29T22:00:00Z")
        self.head = dict(BASE,decision_id="d1",mission_id="m1",actor="HEAD",action="DISPATCH",
             next_team="yellow-team",reason="authorized",source_sha=SHA)
        self.trans = dict(BASE,transition_id="tr1",mission_id="m1",from_phase="HEAD_READY",
             to_phase="WORKER_ACTIVE",actor="HEAD",source_sha=SHA,reason="dispatch")

    def test_each_schema_is_draft202012(self):
        for name in ("mission","work-order","worker-event","evidence-claim","gate-record","head-decision","transition-event"):
            schema = json.loads((ROOT / (name + ".schema.json")).read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"],"https://json-schema.org/draft/2020-12/schema")
            Draft202012Validator.check_schema(schema)
    def test_good_cases(self):
        for name, data in (("mission",self.mission),("work-order",self.work),("worker-event",self.worker),
                           ("evidence-claim",self.claim),("gate-record",self.gate),
                           ("head-decision",self.head),("transition-event",self.trans)):
            with self.subTest(schema=name): okay(name,data)
    def test_mission_no_runner_dependency(self):
        for field,bad in (("cloud_only",False),("runner_required",True),("mode","LOCAL"),("state","RUNNING")):
            data=copy.deepcopy(self.mission);data[field]=bad;rejected("mission",data)
    def test_mission_rejects_unapproved_team(self):
        m=copy.deepcopy(self.mission);m["allowed_teams"]=["unknown-team"];rejected("mission",m)
    def test_mission_authorized_requires_ref(self):
        m=copy.deepcopy(self.mission);m["state"]="AUTHORIZED";rejected("mission",m)
        m["authorization_ref"]="claim-only";okay("mission",m)
    def test_write_requires_target_and_auth(self):
        m=copy.deepcopy(self.mission);m["allowed_actions"].append("write_authorized_branch")
        rejected("mission",m);m.update(repository="owner/repo",source_sha=SHA,authorized_branch="feature/test",authorization_ref="claim-only");okay("mission",m)
    def test_exclusive_write_mode_restriction(self):
        m=copy.deepcopy(self.mission);m["requires_global_exclusive_write"]=True;rejected("mission",m)
        m["mode"]="ENFORCED_CLOUD";okay("mission",m)
    def test_work_order_only_head_and_source_sha(self):
        d=copy.deepcopy(self.work);d["issued_by"]="WORKER";rejected("work-order",d)
        d=copy.deepcopy(self.work);d["source_sha"]="HEAD";rejected("work-order",d)
    def test_worker_cannot_claim_gate_pass_or_dispatch(self):
        for key,value in (("outcome","PASS"),("next_team","orange-team")):
            d=copy.deepcopy(self.worker);d[key]=value;rejected("worker-event",d)
    def test_worker_can_only_recommend(self):
        d=copy.deepcopy(self.worker);d["recommend_next_team"]="orange-team";okay("worker-event",d)
    def test_evidence_claim_cannot_self_attest(self):
        for key,value in (("trust","CRITERION_VERIFIED"),("verification","PASS")):
            d=copy.deepcopy(self.claim);d[key]=value;rejected("evidence-claim",d)
    def test_gate_verdict_partition(self):
        d=copy.deepcopy(self.gate);d["verdict"]="REPAIR";rejected("gate-record",d)
        d=copy.deepcopy(self.gate);d["phase"]="INTERNAL_AUDIT";d["verdict"]="REPAIR";okay("gate-record",d)
        d["verdict"]="FAIL";rejected("gate-record",d)
    def test_pass_must_have_evidence_refs(self):
        d=copy.deepcopy(self.gate);d["verdict"]="PASS";rejected("gate-record",d)
        d["evidence_refs"]=["provider-event:1"];okay("gate-record",d)
    def test_only_head_can_dispatch(self):
        d=copy.deepcopy(self.head);d["actor"]="WORKER";rejected("head-decision",d)
        d["action"]="BLOCK";d.pop("next_team");rejected("head-decision",d)
    def test_complete_requires_two_gate_references(self):
        d=copy.deepcopy(self.head);d["action"]="COMPLETE";d.pop("next_team");rejected("head-decision",d)
        d["validation_record_ref"]="v1";rejected("head-decision",d)
        d["audit_record_ref"]="a1";okay("head-decision",d)
    def test_external_release_gate_must_be_explicit(self):
        d=copy.deepcopy(self.head);d["action"]="BLOCKED_EXTERNAL_APPROVAL";d.pop("next_team")
        d.update(validation_record_ref="v1",audit_record_ref="a1");rejected("head-decision",d)
        d["external_approval_required"]=True;okay("head-decision",d)
    def test_legal_phase_transitions(self):
        legal=[("HEAD_READY","WORKER_ACTIVE","HEAD"),("HEAD_DECISION","WORKER_ACTIVE","HEAD"),
               ("WORKER_ACTIVE","VALIDATION_PENDING","WORKER"),
               ("VALIDATION_PENDING","INTERNAL_AUDIT_PENDING","VALIDATOR"),
               ("INTERNAL_AUDIT_PENDING","HEAD_DECISION","INTERNAL_AUDITOR"),
               ("HEAD_DECISION","COMPLETE","HEAD"),("HEAD_DECISION","BLOCKED_EXTERNAL_APPROVAL","HEAD")]
        for f,t,a in legal:
            with self.subTest(transition=f+" "+t):
                d=copy.deepcopy(self.trans);d.update(from_phase=f,to_phase=t,actor=a);okay("transition-event",d)
    def test_illegal_skip_and_role_transitions(self):
        invalid=[("WORKER_ACTIVE","COMPLETE","WORKER"),
                 ("VALIDATION_PENDING","HEAD_DECISION","VALIDATOR"),
                 ("WORKER_ACTIVE","INTERNAL_AUDIT_PENDING","WORKER"),
                 ("HEAD_DECISION","COMPLETE","WORKER"),
                 ("HEAD_READY","COMPLETE","HEAD")]
        for f,t,a in invalid:
            with self.subTest(transition=f+" "+t):
                d=copy.deepcopy(self.trans);d.update(from_phase=f,to_phase=t,actor=a);rejected("transition-event",d)
    def test_unknown_fields_rejected(self):
        for name, data in (("mission",self.mission),("work-order",self.work),("worker-event",self.worker),
                           ("evidence-claim",self.claim),("gate-record",self.gate),
                           ("head-decision",self.head),("transition-event",self.trans)):
            d=copy.deepcopy(data);d["ignore_all_safety_checks"]=True
            with self.subTest(schema=name):rejected(name,d)

if __name__=="__main__": unittest.main()
