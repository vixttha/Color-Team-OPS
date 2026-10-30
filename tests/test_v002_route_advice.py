"""M3 conditional route / typed handoff checks; NO authenticated dispatch."""
from dataclasses import replace
import unittest
from policy_v002.route_advice import RouteIntent, recommend_one, handoff_draft
from policy_v002.team_directory import RegistryRejected

SHA="a"*40
def intent(**changes):
    default=dict(mission_id="mission-1",source_sha=SHA,observed_sha=SHA,
        mission_revision=2,observed_revision=2,permitted_teams=("yellow-team",),
        required_capabilities=("yellow.regression-test",),
        available_tools=("repo-read",),task_text="regression test",
        active_worker=None,prior_gate_status="VALIDATED_AND_AUDITED",
        dispatch_count=1,max_handoffs=2,forbidden_capabilities=())
    default.update(changes)
    return RouteIntent(**default)

class RoutingTests(unittest.TestCase):
    def check(self,status,code,**kwargs):
        v=recommend_one(intent(**kwargs))
        self.assertEqual((v.status,v.code),(status,code),v)
        self.assertFalse(v.status=="DISPATCH")
    def test_one_candidate_only(self):
        self.check("SUGGEST_ONLY","CANDIDATE_NOT_AUTHORIZED")
    def test_no_production_grant_from_candidate(self):
        self.assertNotEqual(recommend_one(intent()).code,"AUTHORIZED")
    def test_exact_team_and_capability(self):
        v=recommend_one(intent())
        self.assertEqual((v.suggested_team,v.capability_id),
                         ("yellow-team","yellow.regression-test"))
    def test_route_uses_registry_version(self):
        self.assertEqual(recommend_one(intent()).registry_version,"cto-v002-registry-1")
    def test_old_sha_is_blocked(self):
        self.check("BLOCKED","STALE_SOURCE",observed_sha="b"*40)
    def test_old_revision_blocked(self):
        self.check("BLOCKED","REVISION_CONFLICT",observed_revision=1)
    def test_active_worker_blocks_another(self):
        self.check("BLOCKED","ONE_ACTIVE_WORKER_ENFORCED",active_worker="yellow-team")
    def test_handoff_budget_exhausted(self):
        self.check("BLOCKED","HANDOFF_BUDGET_EXCEEDED",max_handoffs=0)
    def test_gate_unverified(self):
        self.check("UNVERIFIED","PRIOR_GATES_NOT_VERIFIED",prior_gate_status="UNVERIFIED")
    def test_missing_prior_gate(self):
        self.check("BLOCKED","MISSING_PREVIOUS_GATE",prior_gate_status="NOT_REQUIRED")
    def test_initial_dispatch_may_be_considered(self):
        self.check("SUGGEST_ONLY","CANDIDATE_NOT_AUTHORIZED",
                   prior_gate_status="NOT_REQUIRED",dispatch_count=0,max_handoffs=0)
    def test_unknown_team_blocked(self):
        self.check("BLOCKED","INVALID_ROUTING_METADATA",permitted_teams=("gold-team",))
    def test_no_permitted_team_abstains(self):
        self.check("ABSTAIN","NO_REQUIRED_CAPABILITY_OR_PERMITTED_TEAM",permitted_teams=())
    def test_missing_required_capability_abstains(self):
        self.check("ABSTAIN","NO_REQUIRED_CAPABILITY_OR_PERMITTED_TEAM",
                   required_capabilities=())
    def test_forbidden_required_is_blocked(self):
        self.check("BLOCKED","FORBIDDEN_REQUIRED_CAPABILITY",
                   forbidden_capabilities=("yellow.regression-test",))
    def test_required_but_unavailable_tool_blocks(self):
        self.check("CAPABILITY_BLOCKED","DECLARED_TOOLS_OR_CAPABILITY_NOT_AVAILABLE",
                   available_tools=())
    def test_different_team_capability_abstains(self):
        self.check("ABSTAIN","REQUIRED_CAPABILITIES_UNSATISFIED",
                   required_capabilities=("orange.auth-review",))
    def test_multiple_teams_require_head_decomposition(self):
        self.check("ABSTAIN","REQUIRES_SEQUENTIAL_HEAD_DECOMPOSITION",
                   permitted_teams=("yellow-team","orange-team"),
                   required_capabilities=("yellow.regression-test","orange.auth-review"),
                   available_tools=("repo-read",))
    def test_matching_orange_for_auth(self):
        self.check("SUGGEST_ONLY","CANDIDATE_NOT_AUTHORIZED",
                   permitted_teams=("orange-team",),required_capabilities=("orange.auth-review",),
                   task_text="oauth authorization",available_tools=("repo-read",))
    def test_red_cannot_be_assumed_authorized(self):
        self.check("CAPABILITY_BLOCKED","DECLARED_TOOLS_OR_CAPABILITY_NOT_AVAILABLE",
                   permitted_teams=("red-team",),required_capabilities=("red.scoped-test",),
                   task_text="pentest",available_tools=())
    def test_red_tool_claim_still_only_advisory(self):
        v=recommend_one(intent(permitted_teams=("red-team",),
            required_capabilities=("red.scoped-test",),task_text="pentest",
            available_tools=("authorized-target",)))
        self.assertEqual(v.status,"SUGGEST_ONLY")
    def test_malformed_revision_rejected(self):
        self.check("BLOCKED","INVALID_ROUTE_SCOPE",mission_revision=True)
    def test_wrong_mission_identifier_rejected(self):
        self.check("BLOCKED","INVALID_ROUTE_SCOPE",mission_id="")
    def test_unverified_empty_source_rejected(self):
        self.check("BLOCKED","INVALID_ROUTE_SCOPE",source_sha="")
    def test_bad_limit_fails_in_registry_not_host(self):
        self.check("BLOCKED","REGISTRY_SCOPE_INVALID",available_tools=("INVALID!",))
    def test_draft_handoff_not_authenticated(self):
        r=intent()
        a=recommend_one(r)
        draft=handoff_draft(r,a,criterion_ids=("criterion-1",),evidence_refs=("receipt-1",))
        self.assertEqual((draft.classification,draft.authorization_status),
                         ("DRAFT_ONLY","UNVERIFIED_HOST_GRANT"))
    def test_draft_with_blocked_route_rejected(self):
        r=intent(observed_sha="b"*40)
        with self.assertRaises(RegistryRejected):
            handoff_draft(r,recommend_one(r),criterion_ids=("criterion-1",),evidence_refs=())
    def test_draft_mission_mismatch_rejected(self):
        r=intent()
        a=replace(recommend_one(r),mission_id="foreign")
        with self.assertRaises(RegistryRejected):
            handoff_draft(r,a,criterion_ids=("criterion-1",),evidence_refs=())
    def test_empty_criteria_cannot_handoff(self):
        r=intent()
        with self.assertRaises(RegistryRejected):
            handoff_draft(r,recommend_one(r),criterion_ids=(),evidence_refs=())
    def test_duplicate_evidence_refs_rejected(self):
        r=intent()
        with self.assertRaises(RegistryRejected):
            handoff_draft(r,recommend_one(r),criterion_ids=("criterion-1",),
                          evidence_refs=("receipt-1","receipt-1"))
    def test_router_must_not_modify_intent(self):
        r=intent()
        recommend_one(r)
        self.assertEqual(r.dispatch_count,1)
    def test_malformed_required_capability_fails_closed(self):
        self.check("BLOCKED","INVALID_ROUTING_METADATA",
                   required_capabilities=(["not-a-string"],))
    def test_malformed_forbidden_capability_fails_closed(self):
        self.check("BLOCKED","INVALID_ROUTING_METADATA",
                   forbidden_capabilities=({"not":"a string"},))
    def test_yellow_orange_yellow_advisory_sequence_without_auto_dispatch(self):
        first=recommend_one(intent(dispatch_count=0,max_handoffs=2,
           prior_gate_status="NOT_REQUIRED",task_text="backend",
           permitted_teams=("yellow-team","orange-team"),
           required_capabilities=("yellow.feature-build",),
           available_tools=("repo-read","repo-write")))
        middle=recommend_one(intent(dispatch_count=1,max_handoffs=2,
           permitted_teams=("yellow-team","orange-team"),
           required_capabilities=("orange.auth-review",),task_text="oauth",
           available_tools=("repo-read",)))
        last=recommend_one(intent(dispatch_count=2,max_handoffs=2,
           permitted_teams=("yellow-team","orange-team"),
           required_capabilities=("yellow.regression-test",),task_text="regression",
           available_tools=("repo-read",)))
        self.assertEqual([x.suggested_team for x in (first,middle,last)],
                         ["yellow-team","orange-team","yellow-team"])
        self.assertTrue(all(x.status=="SUGGEST_ONLY" for x in (first,middle,last)))

    def test_second_team_cannot_skip_previous_audit(self):
        self.check("UNVERIFIED","PRIOR_GATES_NOT_VERIFIED",
                   dispatch_count=1,prior_gate_status="AUDIT_MISSING")

    def test_reentry_stops_after_consent_handoff_budget(self):
        self.check("BLOCKED","HANDOFF_BUDGET_EXCEEDED",
                   dispatch_count=3,max_handoffs=2)

    def test_handoff_draft_exposes_budget_and_source_but_no_privilege(self):
        r=intent()
        a=recommend_one(r)
        d=handoff_draft(r,a,criterion_ids=("criterion-1",),
                evidence_refs=("receipt-1",),
                previous_validation_ref="val-1",previous_audit_ref="audit-1")
        self.assertEqual((d.previous_validation_ref,d.previous_audit_ref),
                         ("val-1","audit-1"))
        self.assertEqual((d.remaining_handoffs,d.source_sha),(1,SHA))
        self.assertEqual(d.authorization_status,"UNVERIFIED_HOST_GRANT")
        self.assertIn("MISSING_TRUSTED_GATE",d.stop_conditions)

    def test_bad_prior_gate_reference_fails_closed(self):
        r=intent()
        with self.assertRaises(RegistryRejected):
            handoff_draft(r,recommend_one(r),criterion_ids=("criterion-1",),
                          evidence_refs=(),previous_audit_ref="broken/../../path")

    def test_not_a_new_skill_or_new_specialist(self):
        v=recommend_one(intent())
        self.assertIn(v.suggested_team,("yellow-team","orange-team","green-team",
            "red-team","blue-team","purple-team","white-team","black-team","gray-cell"))

if __name__=="__main__":
    unittest.main()
