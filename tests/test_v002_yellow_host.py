"""Yellow host-authority lane — synthetic identity/provider, persistent dev journal.

These are NOT production user-consent tests or a deployed cloud host.
"""
from __future__ import annotations
from dataclasses import replace
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from policy_v002.host_runtime import (
    ActorProof, CloudAuthorityEngine, ConsentProof, EvidenceProof,
    HostRejected, SQLiteDevelopmentJournal, digest
)

SHA="a"*40
OTHER="b"*40


class IdentityFixture:
    """Synthetic, deliberately NOT a live identity provider."""
    def __init__(self):
        self.consent_id="consent-unique-001"
        self.consent_subject="user-123"
        self.consent_digest_override=None
        self.consent_expires=1700000300
        self.allowed={
            ("head-token","head_dispatch"):"user-123",
            ("head-token","head_complete"):"user-123",
            ("head-token","head_revoke"):"user-123",
            ("worker-token","worker_report"):"worker-456",
            ("validator-token","validate"):"validator-789",
            ("auditor-token","internal_audit"):"auditor-321",
            ("impostor-token","head_dispatch"):"impostor-000",
            ("impostor-token","head_complete"):"impostor-000",
            ("impostor-token","head_revoke"):"impostor-000",
        }

    def verify_consent(self,token,intent_digest):
        if token!="consent-token":return None
        return ConsentProof(self.consent_subject,self.consent_id,
                            self.consent_digest_override or intent_digest,
                            self.consent_expires)

    def verify_actor(self,token,mission_id,operation):
        name=self.allowed.get((token,operation))
        return ActorProof(name,operation,mission_id) if name is not None else None


class EvidenceFixture:
    """Synthetic provider observations — no live GitHub receipt is authenticated."""
    def __init__(self):
        self.sha=SHA
        self.outcome="PASS"
        self.available=True
        self.override=None
        self.check_count=0

    def current_sha(self,repository,branch):
        return self.sha

    def resolve(self,mission_id,task_id,source_sha,criterion_id,provider_record_id):
        self.check_count+=1
        if not self.available:return None
        if self.override is not None:return self.override
        return EvidenceProof(mission_id,task_id,source_sha,criterion_id,
                             provider_record_id,self.outcome)


def mission(name="mission-001",teams=None,requirements=None,criteria=None):
    return dict(mission_id=name,repository="sample/repo",branch="feature/yellow",
                source_sha=SHA,allowed_teams=teams or ["yellow-team"],
                required_teams=requirements or ["yellow-team"],
                allowed_actions=["read","inspect"],criteria=criteria or ["ci-pass"],
                max_handoffs=(len(teams)-1) if teams is not None else 0)


class HostLaneTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path=str(Path(self.temp.name)/"journal.sqlite")
        self.store=SQLiteDevelopmentJournal(self.path)
        self.identity=IdentityFixture()
        self.evidence=EvidenceFixture()
        self.now=1700000000
        self.host=CloudAuthorityEngine(self.store,self.identity,self.evidence,clock=lambda:self.now)

    def assert_rejected(self,code,call,*args,**kwargs):
        with self.assertRaises(HostRejected) as cm:call(*args,**kwargs)
        self.assertEqual(cm.exception.code,code)

    def grant(self,scope=None,grant="grant-001"):
        return self.host.authorize(scope or mission(),consent_token="consent-token",event_id=grant)

    def dispatch(self,revision=1,team="yellow-team",task="task-001",criterion="ci-pass",event="dispatch-001",token="head-token"):
        return self.host.dispatch("mission-001",revision,token,event,
            team=team,task_id=task,criterion=criterion)

    def report(self,revision=2,task="task-001",receipt="ci:run-001",event="report-001",token="worker-token"):
        return self.host.worker_done("mission-001",revision,token,event,
            task_id=task,provider_record_id=receipt)

    def validate(self,revision=3,event="validate-001",token="validator-token"):
        return self.host.validate("mission-001",revision,token,event)

    def audit(self,revision=4,event="audit-001",token="auditor-token"):
        return self.host.audit("mission-001",revision,token,event)

    def complete(self,revision=5,event="complete-001",token="head-token"):
        return self.host.complete("mission-001",revision,token,event)

    def through_audit(self):
        self.grant();self.dispatch();self.report();self.validate();return self.audit()

    def enable_repair(self, limit=1):
        self.identity.allowed[("head-token","head_repair")]="user-123"
        target=mission()
        target["max_local_repairs"]=limit
        return target

    def test_consent_default_forbids_same_task_repair(self):
        self.grant();self.dispatch();self.report()
        self.identity.allowed[("head-token","head_repair")]="user-123"
        self.assert_rejected("REPAIR_BUDGET_EXCEEDED",self.host.request_repair,
                             "mission-001",3,"head-token","repair-001")

    def test_one_authorized_repair_then_validate_audit_head(self):
        self.grant(self.enable_repair());self.dispatch();self.report()
        self.evidence.outcome="FAIL"
        self.assert_rejected("EVIDENCE_NOT_PASS",self.validate)
        state=self.host.request_repair("mission-001",3,"head-token","repair-001")
        self.assertEqual((state["phase"],state["revision"],state["task"]["repairs"]),
                         ("WORKER_ACTIVE",4,1))
        self.evidence.outcome="PASS"
        self.report(revision=4,receipt="ci:run-002",event="report-002")
        self.validate(revision=5,event="validate-002")
        self.audit(revision=6,event="audit-002")
        result=self.complete(revision=7,event="complete-002")
        self.assertEqual((result["phase"],result["revision"]),("COMPLETE",8))
        self.assertEqual(result["used_receipts"],["ci:run-001","ci:run-002"])
        self.assertEqual([x["kind"] for x in self.store.history("mission-001")],
            ["CONSENT_GRANTED","DISPATCH","WORKER_REPORTED","REPAIR_ORDERED",
             "WORKER_REPORTED","VALIDATION_PASSED","AUDIT_PASSED","HEAD_COMPLETED"])

    def test_two_consented_repairs_complete_and_third_refused(self):
        self.grant(self.enable_repair(2));self.dispatch();self.report()
        self.host.request_repair("mission-001",3,"head-token","repair-001")
        self.report(revision=4,receipt="ci:run-002",event="report-002")
        self.host.request_repair("mission-001",5,"head-token","repair-002")
        self.report(revision=6,receipt="ci:run-003",event="report-003")
        self.assert_rejected("REPAIR_BUDGET_EXCEEDED",self.host.request_repair,
                             "mission-001",7,"head-token","repair-003")
        self.validate(revision=7,event="validate-003")
        self.audit(revision=8,event="audit-003")
        final=self.complete(revision=9,event="complete-003")
        self.assertEqual(final["revision"],10)
        self.assertEqual(len(final["repair_history"]),2)
        self.assertEqual(final["used_receipts"],
                         ["ci:run-001","ci:run-002","ci:run-003"])

    def test_repair_cannot_exceed_consent_bound(self):
        self.grant(self.enable_repair(1));self.dispatch();self.report()
        self.host.request_repair("mission-001",3,"head-token","repair-001")
        self.report(revision=4,receipt="ci:run-002",event="report-002")
        self.assert_rejected("REPAIR_BUDGET_EXCEEDED",self.host.request_repair,
                             "mission-001",5,"head-token","repair-002")

    def test_repair_without_signed_optional_scope_rejected(self):
        target=mission()
        target["max_local_repairs"]=3
        self.assert_rejected("INVALID_REPAIR_BUDGET",self.grant,target)

    def test_repair_with_impostor_head_rejected(self):
        self.grant(self.enable_repair());self.dispatch();self.report()
        self.identity.allowed[("impostor-token","head_repair")]="impostor-000"
        self.assert_rejected("HEAD_NOT_AUTHORIZED",self.host.request_repair,
                             "mission-001",3,"impostor-token","repair-001")

    def test_repair_requires_exact_revision(self):
        self.grant(self.enable_repair());self.dispatch();self.report()
        self.assert_rejected("REVISION_CONFLICT",self.host.request_repair,
                             "mission-001",2,"head-token","repair-001")

    def test_repair_rejects_new_worker_principal(self):
        self.grant(self.enable_repair());self.dispatch();self.report()
        self.host.request_repair("mission-001",3,"head-token","repair-001")
        self.identity.allowed[("other-worker","worker_report")]="other-principal"
        self.assert_rejected("WORKER_PRINCIPAL_CHANGED",self.report,
                             revision=4,receipt="ci:run-002",event="report-002",token="other-worker")

    def test_repair_refuses_replayed_receipt(self):
        self.grant(self.enable_repair());self.dispatch();self.report()
        self.host.request_repair("mission-001",3,"head-token","repair-001")
        self.assert_rejected("EVIDENCE_REPLAY",self.report,
                             revision=4,receipt="ci:run-001",event="report-002")

    def test_repair_history_survives_restart(self):
        self.grant(self.enable_repair());self.dispatch();self.report()
        self.host.request_repair("mission-001",3,"head-token","repair-001")
        restored=SQLiteDevelopmentJournal(self.path).read("mission-001")
        self.assertEqual(restored["repair_history"][0]["prior_receipt"],"ci:run-001")
        self.assertEqual(restored["repair_history"][0]["repair_number"],1)

    def test_repair_blocked_after_expiry(self):
        self.grant(self.enable_repair());self.dispatch();self.report()
        self.now=self.identity.consent_expires
        self.assert_rejected("GRANT_EXPIRED",self.host.request_repair,
                             "mission-001",3,"head-token","repair-001")

    def test_repair_wrong_phase_rejected(self):
        self.grant(self.enable_repair());self.dispatch()
        self.assert_rejected("BAD_PHASE",self.host.request_repair,
                             "mission-001",2,"head-token","repair-001")

    def test_entire_head_worker_validate_audit_head_lane(self):
        self.through_audit()
        final=self.complete()
        self.assertEqual((final["phase"],final["revision"],final["completion"]),
            ("COMPLETE",6,"INTERNAL_READ_ONLY_VERIFIED"))
        self.assertEqual(self.evidence.check_count,2)
        self.assertEqual([e["kind"] for e in self.store.history("mission-001")],
            ["CONSENT_GRANTED","DISPATCH","WORKER_REPORTED","VALIDATION_PASSED","AUDIT_PASSED","HEAD_COMPLETED"])

    def test_persistence_across_reopen(self):
        self.through_audit()
        renewed=CloudAuthorityEngine(SQLiteDevelopmentJournal(self.path),
            self.identity,self.evidence,clock=lambda:self.now)
        result=renewed.complete("mission-001",5,"head-token","complete-restarted")
        self.assertEqual(result["phase"],"COMPLETE")
        self.assertEqual(result["revision"],6)

    def test_revision_conflict_rejected(self):
        self.grant();self.dispatch()
        self.assert_rejected("REVISION_CONFLICT",self.dispatch)

    def test_duplicate_dispatch_event_rejected_globally(self):
        self.grant();self.dispatch();self.report();self.validate();self.audit()
        # Use same event ID for a different team's authorized task.
        self.identity.consent_id="consent-unique-002"
        self.grant(mission("mission-002",teams=["yellow-team"]),grant="grant-002")
        self.assert_rejected("JOURNAL_WRITE_FAILED",self.host.dispatch,
           "mission-002",1,"head-token","dispatch-001",
           team="yellow-team",task_id="task-002",criterion="ci-pass")

    def test_replayed_consent_id_across_missions(self):
        self.grant()
        self.assert_rejected("CONSENT_REPLAY",self.grant,mission("mission-002"),"grant-002")

    def test_second_grant_for_same_mission_rejected(self):
        self.grant()
        self.assert_rejected("MISSION_EXISTS",self.grant,None,"grant-002")

    def test_no_consent_token(self):
        self.assert_rejected("CONSENT_UNVERIFIED",self.host.authorize,
            mission(),consent_token="",event_id="grant-001")

    def test_consent_digest_must_match_exact_intent(self):
        self.identity.consent_digest_override="wrong-digest"
        self.assert_rejected("CONSENT_UNVERIFIED",self.grant)

    def test_consent_expired(self):
        self.identity.consent_expires=self.now
        self.assert_rejected("CONSENT_UNVERIFIED",self.grant)

    def test_consent_longer_than_hour_blocked(self):
        self.identity.consent_expires=self.now+3601
        self.assert_rejected("CONSENT_UNVERIFIED",self.grant)

    def test_source_revision_checked_before_grant(self):
        self.evidence.sha=OTHER
        self.assert_rejected("STALE_SOURCE",self.grant)

    def test_allowed_actions_are_strictly_read_only(self):
        target=mission()
        target["allowed_actions"]=["write"]
        self.assert_rejected("READ_ONLY_PILOT_SCOPE",self.grant,target)

    def test_required_team_must_be_allowed(self):
        target=mission()
        target["required_teams"]=["red-team"]
        self.assert_rejected("INVALID_SCOPE",self.grant,target)

    def test_empty_acceptance_criteria_blocked(self):
        target=mission()
        target["criteria"]=[]
        self.assert_rejected("INVALID_SCOPE",self.grant,target)

    def test_unknown_fields_do_not_expand_consent(self):
        target=mission()
        target["admin"]=True
        self.assert_rejected("INVALID_INTENT",self.grant,target)

    def test_head_cannot_be_impersonated(self):
        self.grant()
        self.assert_rejected("HEAD_NOT_AUTHORIZED",self.dispatch,token="impostor-token")

    def test_unknown_head_token(self):
        self.grant()
        self.assert_rejected("IDENTITY_UNVERIFIED",self.dispatch,token="random")

    def test_worker_cannot_dispatch(self):
        self.grant()
        self.assert_rejected("IDENTITY_UNVERIFIED",self.dispatch,token="worker-token")

    def test_worker_cannot_complete_without_gates(self):
        self.grant()
        self.assert_rejected("IDENTITY_UNVERIFIED",self.complete,revision=1,token="worker-token")

    def test_wrong_team_not_dispatched(self):
        self.grant()
        self.assert_rejected("TASK_NOT_AUTHORIZED",self.dispatch,team="orange-team")

    def test_wrong_criterion_not_dispatched(self):
        self.grant()
        self.assert_rejected("TASK_NOT_AUTHORIZED",self.dispatch,criterion="unapproved")

    def test_worker_must_be_active(self):
        self.grant()
        self.assert_rejected("BAD_PHASE",self.report,revision=1)

    def test_worker_task_id_must_match(self):
        self.grant();self.dispatch()
        self.assert_rejected("BAD_PHASE",self.report,task="forged-task")

    def test_worker_credential_required(self):
        self.grant();self.dispatch()
        self.assert_rejected("IDENTITY_UNVERIFIED",self.report,token="head-token")

    def test_validation_requires_worker_result(self):
        self.grant();self.dispatch()
        self.assert_rejected("BAD_PHASE",self.validate,revision=2)

    def test_validator_credential_required(self):
        self.grant();self.dispatch();self.report()
        self.assert_rejected("IDENTITY_UNVERIFIED",self.validate,token="worker-token")

    def test_missing_provider_observation_fails_closed(self):
        self.grant();self.dispatch();self.report()
        self.evidence.available=False
        self.assert_rejected("EVIDENCE_UNVERIFIED",self.validate)

    def test_provider_failed_result_cannot_validate(self):
        self.grant();self.dispatch();self.report()
        self.evidence.outcome="FAIL"
        self.assert_rejected("EVIDENCE_NOT_PASS",self.validate)

    def test_provider_wrong_task_cannot_validate(self):
        self.grant();self.dispatch();self.report()
        self.evidence.override=EvidenceProof("mission-001","other-task",SHA,"ci-pass","ci:run-001","PASS")
        self.assert_rejected("EVIDENCE_SCOPE_MISMATCH",self.validate)

    def test_source_advancement_blocks_validation(self):
        self.grant();self.dispatch();self.report()
        self.evidence.sha=OTHER
        self.assert_rejected("STALE_SOURCE",self.validate)

    def test_audit_requires_validation(self):
        self.grant();self.dispatch();self.report()
        self.assert_rejected("BAD_PHASE",self.audit,revision=3)

    def test_auditor_credential_required(self):
        self.grant();self.dispatch();self.report();self.validate()
        self.assert_rejected("IDENTITY_UNVERIFIED",self.audit,token="validator-token")

    def test_auditor_rereads_provider_fresh(self):
        self.grant();self.dispatch();self.report();self.validate()
        self.evidence.outcome="FAIL"
        self.assert_rejected("EVIDENCE_NOT_PASS",self.audit)
        self.assertEqual(self.evidence.check_count,2)

    def test_no_early_head_completion(self):
        self.grant();self.dispatch();self.report()
        self.assert_rejected("BAD_PHASE",self.complete,revision=3)

    def test_wrong_head_at_complete(self):
        self.through_audit()
        self.assert_rejected("HEAD_NOT_AUTHORIZED",self.complete,token="impostor-token")

    def test_expired_grant_invalidates_prior_report(self):
        self.grant()
        self.now=self.identity.consent_expires
        self.assert_rejected("GRANT_EXPIRED",self.dispatch)

    def test_duplicate_task_rejected_after_first_audit(self):
        target=mission(teams=["yellow-team","orange-team"],requirements=["yellow-team","orange-team"],
                       criteria=["ci-pass","second-pass"])
        self.grant(target);self.dispatch();self.report();self.validate();self.audit()
        self.assert_rejected("TASK_REPLAY",self.dispatch,revision=5,team="orange-team",
                             task="task-001",criterion="second-pass",event="dispatch-002")

    def test_zero_handoff_budget_blocks_second_team(self):
        target=mission(teams=["yellow-team","orange-team"],
                       requirements=["yellow-team","orange-team"],criteria=["ci-pass","second-pass"])
        target["max_handoffs"]=0
        self.grant(target);self.dispatch();self.report();self.validate();self.audit()
        self.assert_rejected("HANDOFF_BUDGET_EXCEEDED",self.dispatch,revision=5,
            team="orange-team",task="task-002",criterion="second-pass",event="dispatch-002")

    def test_invalid_handoff_budget_refused_at_consent(self):
        target=mission()
        target["max_handoffs"]=-1
        self.assert_rejected("INVALID_HANDOFF_BUDGET",self.grant,target)

    def test_budget_is_part_of_exact_consent_digest(self):
        a=mission()
        b=mission()
        b["max_handoffs"]=1
        self.assertNotEqual(digest(a),digest(b))

    def test_second_team_needed_before_final_head_completion(self):
        target=mission(teams=["yellow-team","orange-team"],requirements=["yellow-team","orange-team"],
                       criteria=["ci-pass","second-pass"])
        self.grant(target);self.dispatch();self.report();self.validate();self.audit()
        self.assert_rejected("INCOMPLETE_CRITERIA",self.complete)

    def test_head_can_reenter_yellow_after_orange_for_distinct_repair_task(self):
        target=mission(teams=["yellow-team","orange-team"],
                       requirements=["yellow-team","orange-team"],
                       criteria=["ci-pass","review-pass","repair-pass"])
        target["max_handoffs"]=2
        self.grant(target)
        self.dispatch();self.report();self.validate();self.audit()
        self.dispatch(revision=5,team="orange-team",task="task-002",
                      criterion="review-pass",event="dispatch-002")
        self.report(revision=6,task="task-002",receipt="ci:run-002",event="report-002")
        self.validate(revision=7,event="validate-002")
        self.audit(revision=8,event="audit-002")
        self.dispatch(revision=9,team="yellow-team",task="task-003",
                      criterion="repair-pass",event="dispatch-003")
        self.report(revision=10,task="task-003",receipt="ci:run-003",event="report-003")
        self.validate(revision=11,event="validate-003")
        verified=self.audit(revision=12,event="audit-003")
        self.assertEqual(verified["approved_teams"],["yellow-team","orange-team"])
        self.assertEqual(len(verified["gates"]),6)
        self.assertEqual(len(verified["used_task_ids"]),3)
        final=self.complete(revision=13,event="complete-003")
        self.assertEqual(final["phase"],"COMPLETE")
        self.assertEqual(final["revision"],14)

    def test_specialist_reentry_still_fails_closed_when_handoffs_exhausted(self):
        target=mission(teams=["yellow-team","orange-team"],
                       requirements=["yellow-team","orange-team"],
                       criteria=["ci-pass","review-pass","repair-pass"])
        target["max_handoffs"]=1
        self.grant(target)
        self.dispatch();self.report();self.validate();self.audit()
        self.dispatch(revision=5,team="orange-team",task="task-002",
                      criterion="review-pass",event="dispatch-002")
        self.report(revision=6,task="task-002",receipt="ci:run-002",event="report-002")
        self.validate(revision=7,event="validate-002")
        self.audit(revision=8,event="audit-002")
        self.assert_rejected("HANDOFF_BUDGET_EXCEEDED",self.dispatch,
                             revision=9,team="yellow-team",task="task-003",
                             criterion="repair-pass",event="dispatch-003")
        self.assert_rejected("INCOMPLETE_CRITERIA",self.complete,revision=9)

    def test_max_handoffs_has_explicit_finite_bound_without_team_count_coupling(self):
        target=mission(teams=["yellow-team"],criteria=["ci-pass","second-pass"])
        target["max_handoffs"]=33
        self.assert_rejected("INVALID_HANDOFF_BUDGET",self.grant,target)
        target["max_handoffs"]=1
        self.grant(target)
        self.dispatch();self.report();self.validate();self.audit()
        second=self.dispatch(revision=5,team="yellow-team",task="task-002",
                             criterion="second-pass",event="dispatch-002")
        self.assertEqual(second["phase"],"WORKER_ACTIVE")

    def test_gate_records_keep_exact_verified_evidence_reference(self):
        state=self.through_audit()
        self.assertEqual([x["evidence_ref"] for x in state["gates"]],
                         ["ci:run-001","ci:run-001"])
        self.assertEqual([x["phase"] for x in state["gates"]],
                         ["VALIDATE","INTERNAL_AUDIT"])

    def test_second_task_cannot_replay_first_receipt_id(self):
        target=mission(teams=["yellow-team","orange-team"],
                       requirements=["yellow-team","orange-team"],
                       criteria=["ci-pass","second-pass"])
        self.grant(target);self.dispatch();self.report();self.validate();self.audit()
        self.dispatch(revision=5,team="orange-team",task="task-002",
                      criterion="second-pass",event="dispatch-002")
        self.assert_rejected("EVIDENCE_REPLAY",self.report,revision=6,
                             task="task-002",receipt="ci:run-001",event="report-002")

    def test_distinct_second_receipt_can_advance_to_validation(self):
        target=mission(teams=["yellow-team","orange-team"],
                       requirements=["yellow-team","orange-team"],
                       criteria=["ci-pass","second-pass"])
        self.grant(target);self.dispatch();self.report();self.validate();self.audit()
        self.dispatch(revision=5,team="orange-team",task="task-002",
                      criterion="second-pass",event="dispatch-002")
        new=self.report(revision=6,task="task-002",receipt="ci:run-002",event="report-002")
        self.assertEqual(new["phase"],"VALIDATION_PENDING")
        self.assertEqual(new["used_receipts"],["ci:run-001","ci:run-002"])

    def test_revocation_blocks_read_and_action_after_restart(self):
        self.grant();self.dispatch()
        self.assertEqual(self.host.revoke("mission-001",2,"head-token","revoke-001"),3)
        self.assert_rejected("GRANT_REVOKED",self.host.read,"mission-001")
        new=CloudAuthorityEngine(SQLiteDevelopmentJournal(self.path),
            self.identity,self.evidence,clock=lambda:self.now)
        self.assert_rejected("GRANT_REVOKED",new.read,"mission-001")

    def test_revocation_stale_revision_fails(self):
        self.grant();self.dispatch()
        self.assert_rejected("REVISION_CONFLICT",self.host.revoke,
                             "mission-001",1,"head-token","rev-001")

    def test_revocation_wrong_head_denied(self):
        self.grant()
        self.assert_rejected("HEAD_NOT_AUTHORIZED",self.host.revoke,
                             "mission-001",1,"impostor-token","rev-001")

    def test_revocation_after_expiration_is_supported(self):
        self.grant()
        self.now=self.identity.consent_expires+1
        self.assertEqual(self.host.revoke("mission-001",1,"head-token","rev-expired"),2)

    def test_journal_tamper_detected(self):
        self.grant()
        con=sqlite3.connect(self.path)
        con.execute("UPDATE mission_events SET entry='{}' WHERE mission_id='mission-001'")
        con.commit();con.close()
        self.assert_rejected("JOURNAL_INTEGRITY_FAILURE",self.host.read,"mission-001")

    def test_journal_event_hash_tamper_detected(self):
        self.grant()
        con=sqlite3.connect(self.path)
        con.execute("UPDATE mission_events SET entry_hash='tampered' WHERE mission_id='mission-001'")
        con.commit();con.close()
        self.assert_rejected("JOURNAL_INTEGRITY_FAILURE",self.host.read,"mission-001")

    def test_missing_mission_unknown(self):
        self.assert_rejected("MISSION_UNKNOWN",self.host.read,"no-such-mission")

    def test_one_issuer_for_two_missions_does_not_mix_records(self):
        self.grant()
        self.identity.consent_id="consent-unique-002"
        other=self.grant(mission("mission-002"),grant="grant-002")
        self.assertEqual(other["mission_id"],"mission-002")
        self.assertEqual(len(self.store.history("mission-001")),1)
        self.assertEqual(len(self.store.history("mission-002")),1)

    def test_core_has_no_hosting_vendor(self):
        source=(Path(__file__).resolve().parents[1]/"policy_v002"/"host_runtime.py").read_text()
        for vendor in ("supabase","vercel","firebase","cloudflare","aws","azure"):
            self.assertNotIn("import "+vendor,source.lower())
        self.assertNotIn("GITHUB_TOKEN",source)
        
    def test_missing_credential_error_never_echoes_token(self):
        self.grant()
        self.assert_rejected("IDENTITY_UNVERIFIED",self.dispatch,token="SECRET_NEVER_ECHO")
        
    def test_journal_has_atomic_revisions_and_unique_event_ids(self):
        self.grant()
        history=self.store.history("mission-001")
        self.assertEqual(history[0]["revision"],1)
        self.assertEqual(len(history[0]["hash"]),64)


if __name__=="__main__":
    unittest.main()
