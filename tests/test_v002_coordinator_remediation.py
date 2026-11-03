"""R-01..R-05 portable coordinator acceptance, source-only development tests.

Synthetic grants and logical event traces NEVER authenticate ChatGPT host actions.
"""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator
from policy_v002.coordinator_trace import (
    HostObservation, assess_external_action, validate_logical_chain,
)
from policy_v002.route_advice import RouteIntent, recommend_one
from policy_v002.team_directory import TeamDirectory, EXPECTED_TEAMS

ROOT = Path(__file__).resolve().parents[1]
SHA = "a" * 40
OTHER_SHA = "b" * 40
TEAMS = sorted(EXPECTED_TEAMS)
COORD = ("mission-control", "ops-director", "verification-gate")
SCHEMA_ROOT = ROOT / "schemas"

def schema(name):
    doc = json.loads((SCHEMA_ROOT / (name + ".schema.json")).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(doc)
    return Draft202012Validator(doc)

def mission():
    doc = json.loads((ROOT / "examples/mission.json").read_text(encoding="utf-8"))
    doc.update(repository="demo/repo", authorized_branch="feature/safe",
               source_sha=SHA, authority_claim_classification="DECLARED_ONLY",
               max_handoffs=2, max_retries=1)
    doc["allowed_actions"].append("write_authorized_branch")
    return doc

def receipt(**changes):
    fields = dict(mission_id="demo-m-001", task_id="task-1", repository="demo/repo",
                  branch="feature/safe", source_sha=SHA,
                  permitted_actions=frozenset(("read", "write_authorized_branch")),
                  tool_connected=True, owner_approved=True,
                  revoked=False, host_verified=True)
    fields.update(changes)
    return HostObservation(**fields)

def routing(stage="INITIAL"):
    row = dict(action="DISPATCH", reason="bounded single-worker head assignment",
               mission_id="demo-m-001", next_team="yellow-team",
               task_id="task-1", source_sha=SHA, head_decision_ref="head-1",
               assignment_stage=stage, authorization_ref="owner-claim",
               authority_claim_status="UNVERIFIED_HOST_AUTHORITY",
               authorization_effect="LOGICAL_ONLY_NO_HOST_GRANT",
               execution_authorized=False, active_worker_count=0,
               remaining_handoffs=1, evidence_refs=["mission-declared-scope"])
    if stage == "AFTER_REVIEW":
        row.update(prior_validation_ref="validate-1", prior_audit_ref="audit-1",
                   verification="PASS", verifier_identity="logical-review-only",
                   verification_time="2026-11-03T20:00:00Z")
    return row

def event(task, team, phase, preceding, idx, *, attempt=0, verdict=None):
    stages=("HEAD_ASSIGN","WORKER_RESULT","VALIDATE","INTERNAL_AUDIT","HEAD_REVIEW")
    actors=("HEAD","WORKER","VALIDATOR","INTERNAL_AUDITOR","HEAD")
    dispositions=("ASSIGN","DONE","PASS","PASS","ACCEPT")
    k=stages.index(phase)
    return dict(event_id="event-%d" % idx, mission_id="demo-m-001",
                team=team, status="DONE", evidence_state="UNVERIFIED",
                source_sha=SHA, summary="logical source-only test",
                evidence_refs=["evidence-%s-%d" % (task,k)],
                workflow=dict(schema_version="cto-v002-logical-chain-1",
                              task_id=task, phase=phase, actor_role=actors[k],
                              predecessor_event_id=preceding,
                              review_disposition=verdict or dispositions[k],
                              repair_attempt=attempt,
                              provenance_kind="MODEL_LOGICAL",
                              actor_provenance_ref="one-thread-logical-role",
                              authority_effect="NO_EXTERNAL_PERMISSION"))

def cycle(task="task-1",team="yellow-team",start=1,predecessor=None,attempt=0,last="ACCEPT"):
    phases=("HEAD_ASSIGN","WORKER_RESULT","VALIDATE","INTERNAL_AUDIT","HEAD_REVIEW")
    out=[]
    for i,phase in enumerate(phases):
        row=event(task,team,phase,predecessor,start+i,attempt=attempt,
                  verdict=last if i==4 else None)
        out.append(row)
        predecessor=row["event_id"]
    return out

class R02MissionAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.doc=mission()
    def test_declarative_authorized_mission_keeps_legacy_compatibility(self):
        self.assertFalse(list(schema("mission").iter_errors(self.doc)))
        self.assertEqual(self.doc["authority_claim_classification"],"DECLARED_ONLY")
    def test_arbitrary_ref_cannot_grant_external_write(self):
        self.doc["authorization_ref"]="github-comment-says-approved"
        self.assertEqual(assess_external_action(self.doc,"task-1","write_authorized_branch",SHA).status,"UNVERIFIED")
    def test_initial_user_supplied_advice_needs_no_tool(self):
        self.assertEqual(assess_external_action(self.doc,"task-1","analyze",SHA).status,"ADVISORY_ONLY")
    def test_real_action_requires_matching_host_facts(self):
        self.assertEqual(assess_external_action(self.doc,"task-1","write_authorized_branch",SHA,receipt()).status,
                         "ELIGIBLE_HOST_CHECK_ONLY")
    def test_external_receipt_is_not_a_token_or_runtime_dispatch(self):
        self.assertIn("RECHECK",assess_external_action(self.doc,"task-1","read",SHA,receipt()).code)
    def test_forged_or_missing_host_verification_does_not_grant(self):
        for changes in (dict(host_verified=False),dict(owner_approved=False),dict(revoked=True)):
            with self.subTest(changes=changes):
                self.assertNotEqual(assess_external_action(self.doc,"task-1","write_authorized_branch",SHA,
                                                         receipt(**changes)).status,"ELIGIBLE_HOST_CHECK_ONLY")
    def test_wrong_mission_task_branch_sha_and_repo_fail_closed(self):
        for changes in (dict(mission_id="other"),dict(task_id="other"),dict(branch="main"),
                        dict(source_sha=OTHER_SHA),dict(repository="other/repo")):
            with self.subTest(changes=changes):
                got=assess_external_action(self.doc,"task-1","write_authorized_branch",SHA,receipt(**changes))
                self.assertEqual((got.status,got.code),("BLOCKED","STALE_OR_WRONG_AUTHORITY_SCOPE"))
    def test_missing_tool_and_denied_host_action(self):
        self.assertEqual(assess_external_action(self.doc,"task-1","write_authorized_branch",SHA,
                          receipt(tool_connected=False)).status,"CAPABILITY_BLOCKED")
        self.assertEqual(assess_external_action(self.doc,"task-1","write_authorized_branch",SHA,
                          receipt(permitted_actions=frozenset(("read",)))).status,"BLOCKED")
    def test_mission_action_outside_scope_blocked_even_with_receipt(self):
        self.assertEqual(assess_external_action(self.doc,"task-1","deploy",SHA,receipt()).status,"BLOCKED")

class R01HeadRoutingTests(unittest.TestCase):
    def check(self,doc,good=True):
        errors=list(schema("routing-decision").iter_errors(doc))
        if good: self.assertFalse(errors,[str(e) for e in errors])
        else: self.assertTrue(errors,doc)
    def test_suggest_only_never_claims_execution(self):
        self.check(dict(mission_id="demo-m-001",action="SUGGEST_ONLY",
                        reason="propose analysis",next_team="yellow-team"))
    def test_bare_dispatch_without_proof_is_invalid(self):
        self.check(dict(mission_id="demo-m-001",action="DISPATCH",
                        reason="model said yes",next_team="yellow-team"),False)
    def test_first_worker_has_no_invented_prior_gate(self):
        self.check(routing("INITIAL"))
    def test_later_dispatch_requires_gates_and_head_decision(self):
        self.check(routing("AFTER_REVIEW"))
    def test_stale_or_unverified_after_review_cannot_pass_schema(self):
        d=routing("AFTER_REVIEW");d["verification"]="UNVERIFIED";self.check(d,False)
    def test_missing_head_task_source_and_receipts_rejected(self):
        for key in ("head_decision_ref","task_id","source_sha","evidence_refs"):
            d=routing();d.pop(key);self.check(d,False)
    def test_dispatch_cannot_mint_permission_or_overlap(self):
        for key,value in (("execution_authorized",True),("active_worker_count",1),
                          ("authorization_effect","GRANT"),("authority_claim_status","AUTHORIZED")):
            d=routing();d[key]=value;self.check(d,False)
    def test_forged_prior_audit_or_nonfirst_stage_invalid(self):
        d=routing("AFTER_REVIEW");d.pop("prior_audit_ref");self.check(d,False)
        d=routing("INITIAL");d["prior_audit_ref"]="fictitious";self.check(d,False)
    def test_dispatch_budget_cannot_be_negative(self):
        d=routing();d["remaining_handoffs"]=-1;self.check(d,False)
    def test_json_is_not_a_host_trust_anchor(self):
        self.assertFalse(list(schema("routing-decision").iter_errors(routing())))
        self.assertFalse(routing()["execution_authorized"])

class R03LogicalEventTests(unittest.TestCase):
    def setUp(self):
        self.doc=mission()
        self.steps=cycle()
    def check(self,events=None):
        return validate_logical_chain(self.doc,events if events is not None else self.steps,SHA)
    def test_legacy_worker_event_is_still_schema_valid(self):
        old=json.loads((ROOT/"examples/completion-event.json").read_text(encoding="utf-8"))
        self.assertFalse(list(schema("completion-event").iter_errors(old)))
    def test_all_five_new_portable_events_have_valid_shape(self):
        for e in self.steps:
            self.assertFalse(list(schema("completion-event").iter_errors(e)))
    def test_initial_then_full_cycle_is_logically_valid_only(self):
        self.assertEqual((self.check().status,self.check().code),
                         ("LOGICAL_VALID_UNVERIFIED","NO_INDEPENDENT_HOST_AUTHENTICATION"))
    def test_following_specialist_after_head_accept_is_allowed(self):
        all_events=self.steps+cycle("task-2","orange-team",6,self.steps[-1]["event_id"])
        self.assertEqual(self.check(all_events).status,"LOGICAL_VALID_UNVERIFIED")
    def test_legitimate_same_worker_repair_is_bounded(self):
        self.steps[-1]["workflow"]["review_disposition"]="REPAIR"
        rep=cycle("task-1","yellow-team",6,self.steps[-1]["event_id"],attempt=1)
        self.assertEqual(self.check(self.steps+rep).status,"LOGICAL_VALID_UNVERIFIED")
    def test_duplicate_event_id_rejected(self):
        self.steps[2]["event_id"]=self.steps[1]["event_id"]
        self.assertEqual(self.check().status,"BLOCKED")
    def test_out_of_order_audit_before_validation_rejected(self):
        self.steps[2],self.steps[3]=self.steps[3],self.steps[2]
        self.assertEqual(self.check().status,"BLOCKED")
    def test_skipped_validate_or_audit_is_rejected(self):
        for index in (2,3):
            rows=deepcopy(self.steps);rows.pop(index)
            self.assertEqual(self.check(rows).status,"BLOCKED")
    def test_wrong_predecessor_fails_closed(self):
        self.steps[2]["workflow"]["predecessor_event_id"]="fake-replayed-event"
        self.assertEqual(self.check().status,"BLOCKED")
    def test_cross_mission_and_stale_source_rejected(self):
        for key,value in (("mission_id","foreign"),("source_sha",OTHER_SHA)):
            rows=deepcopy(self.steps);rows[2][key]=value
            self.assertEqual(self.check(rows).status,"BLOCKED")
    def test_overlapping_worker_and_cross_task_rejected(self):
        rows=deepcopy(self.steps);rows[2]["workflow"]["task_id"]="other-task"
        self.assertEqual(self.check(rows).status,"BLOCKED")
        rows=deepcopy(self.steps);rows[2]["team"]="orange-team"
        self.assertEqual(self.check(rows).status,"BLOCKED")
    def test_wrong_role_self_attestation_does_not_pass(self):
        self.steps[3]["workflow"]["actor_role"]="WORKER"
        self.assertEqual(self.check().status,"BLOCKED")
    def test_cross_task_receipt_replay_rejected(self):
        second=cycle("task-2","orange-team",6,self.steps[-1]["event_id"])
        second[0]["evidence_refs"]=self.steps[0]["evidence_refs"][:]
        self.assertEqual(self.check(self.steps+second).code,"CROSS_TASK_EVIDENCE_REPLAY")
    def test_missing_evidence_and_forged_observation_fails_closed(self):
        rows=deepcopy(self.steps);rows[1].pop("evidence_refs")
        self.assertTrue(list(schema("completion-event").iter_errors(rows[1])))
        self.assertEqual(self.check(rows).status,"BLOCKED")
        rows=deepcopy(self.steps);rows[2]["evidence_state"]="OBSERVED"
        self.assertEqual(self.check(rows).status,"UNVERIFIED")
    def test_insufficient_head_review_or_forged_pass_labels_rejected(self):
        self.steps[3]["workflow"]["review_disposition"]="UNVERIFIED"
        self.assertEqual(self.check().status,"BLOCKED")
    def test_retry_budget_exhausted(self):
        self.doc["max_retries"]=0
        self.steps[-1]["workflow"]["review_disposition"]="REPAIR"
        rep=cycle("task-1","yellow-team",6,self.steps[-1]["event_id"],attempt=1)
        self.assertEqual(self.check(self.steps+rep).code,"RETRY_BUDGET_EXCEEDED")
    def test_handoff_budget_exhausted(self):
        self.doc["max_handoffs"]=0
        second=cycle("task-2","orange-team",6,self.steps[-1]["event_id"])
        self.assertEqual(self.check(self.steps+second).code,"HANDOFF_BUDGET_EXCEEDED")
    def test_new_task_must_not_reuse_old_task_id(self):
        second=cycle("task-1","orange-team",6,self.steps[-1]["event_id"])
        self.assertEqual(self.check(self.steps+second).status,"BLOCKED")
    def test_observed_source_revision_must_match(self):
        self.assertEqual(validate_logical_chain(self.doc,self.steps,OTHER_SHA).code,"STALE_SOURCE")
    def test_failed_worker_status_cannot_be_promoted_by_later_pass(self):
        rows=deepcopy(self.steps);rows[1]["status"]="FAILED"
        self.assertEqual(self.check(rows).code,"FAILED_OR_BLOCKED_PHASE")
    def test_missing_evidence_cannot_be_promoted_by_pass_label(self):
        rows=deepcopy(self.steps);rows[2]["evidence_state"]="MISSING"
        self.assertEqual(self.check(rows).code,"MISSING_EVIDENCE_CANNOT_PASS")
    def test_schema_events_never_authorize_external_operation(self):
        self.assertTrue(all(x["workflow"]["authority_effect"]=="NO_EXTERNAL_PERMISSION" for x in self.steps))
        self.assertEqual(self.check().status,"LOGICAL_VALID_UNVERIFIED")

class R04AdvisoryFallbackTests(unittest.TestCase):
    CANDIDATES={
      "yellow-team":("yellow.feature-build","python handler"),
      "orange-team":("orange.auth-review","authorization code"),
      "green-team":("green.ci-evidence","ci log"),
      "red-team":("red.scoped-test","fictional red simulation"),
      "blue-team":("blue.detection","log sample"),
      "purple-team":("purple.correlation","attack defense report"),
      "white-team":("white.exercise-rules","exercise rules"),
      "black-team":("black.threat-research","dated advisory"),
      "gray-cell":("gray.user-journey","synthetic ux"),
    }
    def route(self,team,cap,text,**kw):
        params=dict(mission_id="m1",source_sha=SHA,observed_sha=SHA,
             mission_revision=1,observed_revision=1,
             permitted_teams=(team,),required_capabilities=(cap,),
             available_tools=(),task_text=text,active_worker=None,
             prior_gate_status="NOT_REQUIRED",dispatch_count=0,
             max_handoffs=0,advisory_only=True,
             supplied_context_ref="user-supplied-case",synthetic_only=True)
        params.update(kw)
        return recommend_one(RouteIntent(**params))
    def test_all_nine_can_advise_without_cloud_connectors(self):
        for team,(cap,text) in self.CANDIDATES.items():
            with self.subTest(team=team):
                ans=self.route(team,cap,text)
                self.assertEqual((ans.status,ans.code,ans.suggested_team),
                                 ("SUGGEST_ONLY","ADVISORY_WITH_SUPPLIED_CONTEXT",team))
    def test_missing_context_never_claims_advice(self):
        ans=self.route("yellow-team","yellow.feature-build","backend",supplied_context_ref=None)
        self.assertEqual(ans.status,"UNVERIFIED")
    def test_red_requires_explicit_synthetic_only_scope(self):
        ans=self.route("red-team","red.scoped-test","pentest",synthetic_only=False)
        self.assertEqual(ans.status,"CAPABILITY_BLOCKED")
    def test_original_real_tool_requirement_remains_blocked(self):
        ans=self.route("yellow-team","yellow.feature-build","backend",advisory_only=False)
        self.assertEqual(ans.status,"CAPABILITY_BLOCKED")
    def test_directory_advice_keeps_missing_live_tool_flags(self):
        d=TeamDirectory().search(query="backend",permitted_teams=("yellow-team",),
                                 required_capabilities=("yellow.feature-build",),
                                 available_tools=(),advisory_only=True,
                                 supplied_context_ref="user-supplied-case")
        self.assertEqual(d.status,"CANDIDATES_ADVISORY_ONLY")
        self.assertIn("repo-write",d.matches[0].missing_tools)
        self.assertEqual(d.matches[0].status,"ADVISORY_ONLY")
    def test_untrusted_or_missing_context_does_not_grant(self):
        d=TeamDirectory().search(query="backend",permitted_teams=("yellow-team",),
                                 required_capabilities=("yellow.feature-build",),
                                 advisory_only=True)
        self.assertEqual(d.status,"ABSTAIN")
    def test_references_for_all_nine_mark_no_fabricated_live_evidence(self):
        for team in TEAMS:
            text=(ROOT/"skills"/team/"references/v002-competencies.md").read_text(encoding="utf-8")
            self.assertIn("R-04",text,team)
            self.assertIn("NOT_RUN",text,team)
            self.assertIn("owner permission",text,team)

class R05MarkdownAndCompatibilityTests(unittest.TestCase):
    def test_all_three_coordinators_have_unescaped_inline_code(self):
        for team in COORD:
            text=(ROOT/"skills"/team/"SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn(chr(92)+chr(96),text,team)
            self.assertTrue(text.startswith("---\nname: "+team+"\n"))
            self.assertIn("docs/CONSTITUTION.md",text)
    def test_exactly_nine_specialists_three_coordinators(self):
        dirs={p.parent.name for p in (ROOT/"skills").glob("*/SKILL.md")}
        self.assertEqual(dirs,set(TEAMS)|set(COORD))
        self.assertEqual(len(list((ROOT/"skills").glob("*/references/v002-competencies.md"))),9)
        self.assertEqual(sum(len(x["capabilities"]) for x in
                             json.loads((ROOT/"registry/v0.0.2/teams.json").read_text())["teams"]),18)
    def test_two_descriptors_keep_production_startup_prompt(self):
        left=json.loads((ROOT/"plugin.json").read_text())
        right=json.loads((ROOT/".codex-plugin/plugin.json").read_text())
        a=left["extensions"]["com.openai"]["interface"]["defaultPrompt"]
        self.assertEqual(a,right["interface"]["defaultPrompt"])
        self.assertIn("bounded cloud-only software development mission",a)
        self.assertEqual((left["version"],right["version"]),("0.0.2","0.0.2"))
    def test_original_three_schema_and_example_count_still_portable(self):
        self.assertEqual(len(list((ROOT/"schemas").glob("*.json"))),3)
        self.assertEqual(len(list((ROOT/"examples").glob("*.json"))),3)
        for name in ("mission","routing-decision","completion-event"):
            schema(name)

if __name__=="__main__":
    unittest.main()
