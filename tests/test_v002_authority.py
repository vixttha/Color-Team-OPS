"""D4 trusted host snapshot integration tests: ALL signed issuer records are SYNTHETIC."""
import copy
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
import unittest

from policy_v002.host_authority import (
    AuthorityUnavailable, SealedSnapshot, SignedSnapshotAuthority, canonical_json)
from policy_v002.github_provider import GitHubBackedTrustAdapter
from policy_v002.verifier import evaluate_completion
from test_v002_github import HostFixture, ReaderFixture, RUN, RID, SHA
from test_v002_policy import fixture

KEY=b"SYNTHETIC_D4_TEST_KEY_DO_NOT_USE_IN_PRODUCTION_ABCDEFG"
NOW=datetime(2026,10,30,5,0,tzinfo=timezone.utc)
TS=int(NOW.timestamp())


def make_body():
    host=HostFixture()
    auth=host.auth
    b=host.binding
    return dict(
        version="cto-d4-snapshot-1",issuer="host-test",audience="cto-v002",
        key_id="test-key",mission_id="m1",authorization_ref="ref1",
        revision=1,issued_at=TS-30,expires_at=TS+300,revoked=False,
        scope=dict(mission_id="m1",authorization_ref="ref1",repository_id=RID,
            repository="owner/repo",branch="design/new",source_sha=SHA,
            principal_id="test-principal",teams=sorted(auth.teams),
            actions=sorted(auth.actions),head_decisions=["d1"],task_ids=["t1"]),
        dispatches=[dict(mission_id="m1",source_sha=SHA,task_id="t1",
                        team="yellow-team",actor="HEAD",approved=True)],
        transitions=[dict(mission_id="m1",source_sha=SHA,
            transition_id=x.transition_id,from_phase=x.from_phase,to_phase=x.to_phase,
            actor=x.actor,task_id=x.task_id,team=x.team,approved=True)
            for x in host.transitions.values()],
        gates=[dict(mission_id="m1",source_sha=SHA,record_id=x.record_id,
            phase=x.phase,verdict=x.verdict,criterion_ids=sorted(x.criterion_ids),
            evidence_refs=sorted(x.evidence_refs),role=x.role,
            verifier_ref=x.verifier_ref,approved=True) for x in host.gates.values()],
        snapshot=dict(mission_id="m1",source_sha=SHA,phase="HEAD_DECISION",
                      active_team=None,active_task_id=None),
        run_bindings=[dict(mission_id="m1",source_sha=SHA,
            provider_record_id="run:"+str(RUN),task_id="t1",criterion_id="criterion1",
            repository_id=RID,repository="owner/repo",branch="design/new",
            run_id=RUN,run_attempt=1,workflow_path=b.workflow_path,event="push",
            required_jobs=list(b.required_jobs),
            required_job_steps=[list(x) for x in b.required_job_steps])]
    )


def seal(p):
    return SealedSnapshot(copy.deepcopy(p),hmac.new(KEY,canonical_json(p),hashlib.sha256).hexdigest())


class AuthorityTests(unittest.TestCase):
    def setUp(self):
        self.body=make_body()
        self.latest=1
        self.now=NOW

    def authority(self, envelope=None, key=KEY, issuer="host-test", audience="cto-v002"):
        return SignedSnapshotAuthority(
            envelope if envelope is not None else seal(self.body),
            expected_issuer=issuer,expected_audience=audience,
            key_lookup=lambda kid: key if kid=="test-key" else None,
            trusted_latest_revision=lambda mid: self.latest if mid=="m1" else None,
            clock=lambda:self.now)

    def rejected(self,**kwargs):
        with self.assertRaises(AuthorityUnavailable):
            self.authority(**kwargs)

    def policy(self):
        data=fixture()
        data["evidence_claims"][0]["provider_record_id"]="run:"+str(RUN)
        return evaluate_completion(**data,trust=GitHubBackedTrustAdapter(
            ReaderFixture(),self.authority()))

    def test_signed_host_and_github_fixture_complete(self):
        v=self.policy()
        self.assertEqual((v.status,v.code),("PASS","INTERNAL_COMPLETION_VERIFIED"))
    def test_signature_tampering(self):
        x=seal(self.body)
        mod=copy.deepcopy(x.payload)
        mod["scope"]["actions"].append("write_authorized_branch")
        self.rejected(envelope=SealedSnapshot(mod,x.mac_hex))
    def test_signature_forgery(self):
        self.rejected(envelope=SealedSnapshot(self.body,"0"*64))
    def test_wrong_issuer(self):
        self.rejected(issuer="impostor")
    def test_wrong_audience(self):
        self.rejected(audience="wrong")
    def test_missing_key(self):
        self.rejected(key=None)
    def test_short_key(self):
        self.rejected(key=b"short")
    def test_stale_revision(self):
        self.latest=2
        self.rejected()
    def test_missing_revision_or_revocation_store(self):
        self.latest=None
        self.rejected()
    def test_revoked_grant(self):
        self.body["revoked"]=True
        self.rejected()
    def test_expired_grant(self):
        self.now=NOW+timedelta(hours=1)
        self.rejected()
    def test_future_issued_grant(self):
        self.now=NOW-timedelta(hours=1)
        self.rejected()
    def test_overlong_grant(self):
        self.body["expires_at"]=TS+3700
        self.rejected()
    def test_expiry_checked_on_every_access(self):
        host=self.authority()
        self.now=NOW+timedelta(hours=1)
        with self.assertRaises(AuthorityUnavailable):
            host.authorization("m1","ref1")
    def test_revision_checked_on_every_access(self):
        host=self.authority()
        self.latest=3
        with self.assertRaises(AuthorityUnavailable):
            host.expected_repository_id("owner/repo")
    def test_foreign_transition(self):
        self.body["transitions"][0]["mission_id"]="wrong"
        self.rejected()
    def test_stale_gate_sha(self):
        self.body["gates"][0]["source_sha"]="b"*40
        self.rejected()
    def test_duplicate_gate(self):
        self.body["gates"].append(copy.deepcopy(self.body["gates"][0]))
        self.rejected()
    def test_active_worker_cannot_complete(self):
        self.body["snapshot"]["active_team"]="yellow-team"
        self.rejected()
    def test_wrong_mission_phase(self):
        self.body["snapshot"]["phase"]="WORKER_ACTIVE"
        self.rejected()
    def test_wrong_repository_id_binding(self):
        self.body["run_bindings"][0]["repository_id"]=55
        self.rejected()
    def test_unapproved_task_binding(self):
        self.body["run_bindings"][0]["task_id"]="other"
        self.rejected()
    def test_unapproved_dispatch(self):
        self.body["dispatches"][0]["team"]="red-team"
        self.rejected()
    def test_wrong_head_authorization(self):
        self.body["scope"]["head_decisions"]=["not-d1"]
        self.assertEqual(self.policy().code,"NOT_AUTHORIZED")
    def test_unapproved_dispatch_policy_block(self):
        self.body["dispatches"]=[]
        self.assertEqual(self.policy().code,"DISPATCH_NOT_AUTHORIZED")
    def test_unattested_audit_policy_unverified(self):
        self.body["gates"]=[x for x in self.body["gates"] if x["phase"]!="INTERNAL_AUDIT"]
        self.assertEqual(self.policy().code,"GATE_UNAUTHENTICATED")
    def test_absent_binding_unverified(self):
        self.assertIsNone(self.authority().run_binding("run:999"))
    def test_no_global_write_lock_inferred(self):
        self.assertFalse(self.authority().exclusive_write_enforced("m1","owner/repo","design/new"))
    def test_claim_only_no_signature(self):
        self.rejected(envelope=SealedSnapshot(self.body,""))
    def test_no_user_consent_claimed_by_test(self):
        # A synthetic test signer is NOT an authenticated user approval.
        self.assertEqual(self.authority().authorization("m1","ref1").principal_id,"test-principal")

if __name__=="__main__":
    unittest.main()
