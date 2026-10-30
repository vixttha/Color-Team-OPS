"""D3 GitHub evidence adapter tests — all provider/host fixtures synthetic.

No actual credentials, GitHub network access or real ChatGPT host execution.
"""
from dataclasses import replace
import copy
import json
import unittest

from policy_v002.github_provider import (
    GitHubRESTReader, GitHubBackedTrustAdapter, RunBinding, ProviderReadError
)
from policy_v002.verifier import evaluate_completion
from test_v002_policy import FakeAdapter, fixture, SHA, OTHER_SHA

RID = 1439026865
RUN = 41004395615
PATH = ".github/workflows/v0.0.2-contract-prototype.yml"
BRANCH = "design/new"
LINUX_STEP = "Validate schemas and negative cases (Linux)"
WINDOWS_STEP = "Validate schemas and negative cases (Windows)"


class HostFixture(FakeAdapter):
    """Synthetic host records; is NOT an authenticated mission ledger."""
    def __init__(self):
        super().__init__()
        self.repo_id = RID
        self.binding = RunBinding("m1", "t1", "criterion1", RID,
            "owner/repo", BRANCH, SHA, RUN, PATH, "push",
            ("linux", "windows"),
            (("linux", LINUX_STEP), ("windows", WINDOWS_STEP)))
    def expected_repository_id(self, repository):
        return self.repo_id if repository == "owner/repo" else None
    def run_binding(self, provider_record_id):
        return self.binding if provider_record_id == f"run:{RUN}" else None


class ReaderFixture:
    """Mock read-only provider GET responses, never external API output."""
    def __init__(self):
        self.repo = {"id": RID, "full_name": "owner/repo", "private": True}
        self.ref = {"ref": "refs/heads/" + BRANCH,
                    "object": {"type": "commit", "sha": SHA}}
        self.run = {
            "id": RUN, "repository": {"id": RID}, "head_repository": {"id": RID},
            "head_sha": SHA, "head_branch": BRANCH, "path": PATH, "event": "push",
            "run_attempt": 1, "status": "completed", "conclusion": "success"
        }
        self.jobs = [
            {"id": 1, "run_id": RUN, "name": "linux", "status": "completed",
             "conclusion": "success",
             "steps": [{"name": LINUX_STEP, "status": "completed", "conclusion": "success"}]},
            {"id": 2, "run_id": RUN, "name": "windows", "status": "completed",
             "conclusion": "success",
             "steps": [{"name": WINDOWS_STEP, "status": "completed", "conclusion": "success"}]},
        ]
    def repository(self, repository):
        return copy.deepcopy(self.repo)
    def branch_ref(self, repository, branch):
        return copy.deepcopy(self.ref)
    def workflow_run(self, repository, run_id):
        return copy.deepcopy(self.run)
    def latest_jobs(self, repository, run_id):
        return copy.deepcopy(self.jobs)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.host=HostFixture()
        self.reader=ReaderFixture()
        self.adapter=GitHubBackedTrustAdapter(self.reader,self.host)
        self.data=fixture()
        self.data["evidence_claims"][0]["provider_record_id"]=f"run:{RUN}"

    def verify(self):
        return evaluate_completion(**self.data,trust=self.adapter)

    def assert_verdict(self,status,code):
        outcome=self.verify()
        self.assertEqual((outcome.status,outcome.code),(status,code),outcome)

    def test_run_criteria_to_d2_pass_synthetic(self):
        self.assert_verdict("PASS","INTERNAL_COMPLETION_VERIFIED")
    def test_live_current_branch_sha_must_match(self):
        self.reader.ref["object"]["sha"]=OTHER_SHA
        self.assert_verdict("BLOCKED","STALE_REVISION")
    def test_missing_host_authorization(self):
        self.host.auth=None
        self.assert_verdict("UNVERIFIED","AUTH_UNAVAILABLE")
    def test_host_ledger_missing_run_binding(self):
        self.host.binding=None
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_wrong_repo_numeric_id(self):
        self.reader.repo["id"]=123
        self.assert_verdict("UNVERIFIED","SOURCE_UNAVAILABLE")
    def test_forked_head_repository_not_evidence(self):
        self.reader.run["head_repository"]["id"]=45
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_wrong_run_repository_id_not_evidence(self):
        self.reader.run["repository"]["id"]=45
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_wrong_sha_in_workflow_run_not_evidence(self):
        self.reader.run["head_sha"]=OTHER_SHA
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_wrong_branch_in_run_not_evidence(self):
        self.reader.run["head_branch"]="main"
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_unapproved_workflow_not_evidence(self):
        self.reader.run["path"]=".github/workflows/other.yml"
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_unapproved_event_not_evidence(self):
        self.reader.run["event"]="pull_request"
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_run_queued_not_evidence(self):
        self.reader.run["status"]="queued"
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_run_cancelled_not_evidence(self):
        self.reader.run["conclusion"]="cancelled"
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_run_failure_blocked(self):
        self.reader.run["conclusion"]="failure"
        self.assert_verdict("BLOCKED","CRITERION_FAILED")
    def test_required_job_failure_blocked(self):
        self.reader.jobs[0]["conclusion"]="failure"
        self.assert_verdict("BLOCKED","CRITERION_FAILED")
    def test_required_test_step_failure_blocked(self):
        self.reader.jobs[0]["steps"][0]["conclusion"]="failure"
        self.assert_verdict("BLOCKED","CRITERION_FAILED")
    def test_required_test_step_missing_not_evidence(self):
        self.reader.jobs[0]["steps"]=[]
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_wrong_job_name_not_evidence(self):
        self.reader.jobs[0]["name"]="something-else"
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_one_job_missing_not_evidence(self):
        self.reader.jobs.pop()
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_duplicate_required_job_name_not_evidence(self):
        self.reader.jobs.append(copy.deepcopy(self.reader.jobs[0]))
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_run_id_wrong_not_evidence(self):
        self.reader.run["id"]=RUN+1
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_unbound_other_green_run_not_evidence(self):
        self.data["evidence_claims"][0]["provider_record_id"]="run:99999"
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_mismatched_host_run_binding_not_evidence(self):
        self.host.binding=replace(self.host.binding,run_id=RUN+1)
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_invalid_host_repo_id_not_evidence(self):
        self.host.repo_id=-1
        self.assert_verdict("UNVERIFIED","SOURCE_UNAVAILABLE")
    def test_case_sensitive_provider_reject(self):
        self.data["evidence_claims"][0]["provider"]="GitHub"
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_wrong_bound_criterion_not_evidence(self):
        self.host.binding=replace(self.host.binding,criterion_id="unrelated")
        self.assert_verdict("BLOCKED","EVIDENCE_SCOPE_MISMATCH")
    def test_only_host_attests_internal_audit(self):
        self.host.gates["a1"]=None
        self.assert_verdict("UNVERIFIED","GATE_UNAUTHENTICATED")
    def test_binding_with_only_checkout_is_not_accepted_as_test_criterion(self):
        self.host.binding=replace(self.host.binding,
           required_job_steps=(("linux","Unrelated"),("windows",WINDOWS_STEP)))
        self.assert_verdict("UNVERIFIED","EVIDENCE_UNAVAILABLE")
    def test_auth_cannot_be_inferred_from_ability_to_read_repository(self):
        self.host.auth=replace(self.host.auth,valid=False)
        self.assert_verdict("BLOCKED","AUTH_REVOKED")
    def test_no_global_write_lock_inferred_from_provider_read(self):
        self.data["mission"]["requires_global_exclusive_write"]=True
        self.data["mission"]["mode"]="ENFORCED_CLOUD"
        self.assert_verdict("CAPABILITY_BLOCKED","EXCLUSIVE_WRITE_NOT_ENFORCED")


class FakeHTTPResponse:
    def __init__(self,url,payload,status=200):
        self.status=status
        self.url=url
        self.raw=json.dumps(payload).encode("utf-8")
    def __enter__(self):
        return self
    def __exit__(self,*args):
        pass
    def geturl(self):
        return self.url
    def read(self,n):
        return self.raw[:n]


class FakeOpener:
    def __init__(self,responses):
        self.responses=list(responses)
        self.requests=[]
    def open(self,request,timeout):
        self.requests.append(request)
        return FakeHTTPResponse(request.full_url,self.responses.pop(0))


class RestReaderTests(unittest.TestCase):
    def setUp(self):
        self.reader=GitHubRESTReader(lambda:"TEST_ONLY_TOKEN")
    def test_exact_get_and_host(self):
        self.reader._opener=FakeOpener([{"id":RID,"full_name":"owner/repo","private":True}])
        self.reader.repository("owner/repo")
        req=self.reader._opener.requests[0]
        self.assertEqual(req.get_method(),"GET")
        self.assertEqual(req.full_url,"https://api.github.com/repos/owner/repo")
        self.assertEqual(req.get_header("Authorization"),"Bearer TEST_ONLY_TOKEN")
    def test_repo_locator_rejects_path_injection(self):
        with self.assertRaises(ProviderReadError):
            self.reader.repository("../owner/repo")
    def test_branch_rejects_traversal(self):
        with self.assertRaises(ProviderReadError):
            self.reader.branch_ref("owner/repo","feature/../main")
    def test_branch_encoded_path(self):
        self.reader._opener=FakeOpener([{"ref":"refs/heads/design/new"}])
        self.reader.branch_ref("owner/repo","design/new")
        self.assertIn("/git/ref/heads/design/new",self.reader._opener.requests[0].full_url)
    def test_missing_credentials_fail_closed(self):
        reader=GitHubRESTReader(lambda:"")
        reader._opener=FakeOpener([])
        with self.assertRaises(ProviderReadError):
            reader.repository("owner/repo")
    def test_jobs_complete_one_page(self):
        self.reader._opener=FakeOpener([{"total_count":1,"jobs":[{"id":1,"name":"linux"}]}])
        rows=self.reader.latest_jobs("owner/repo",123)
        self.assertEqual(len(rows),1)
    def test_jobs_paginate_without_truncation(self):
        page1=[{"id":i} for i in range(100)]
        page2=[{"id":100}]
        self.reader._opener=FakeOpener([
            {"total_count":101,"jobs":page1},{"total_count":101,"jobs":page2}
        ])
        rows=self.reader.latest_jobs("owner/repo",123)
        self.assertEqual(len(rows),101)
        self.assertEqual(len(self.reader._opener.requests),2)
    def test_jobs_duplicate_ids_rejected(self):
        self.reader._opener=FakeOpener([{"total_count":2,"jobs":[{"id":1},{"id":1}]}])
        with self.assertRaises(ProviderReadError):
            self.reader.latest_jobs("owner/repo",123)
    def test_jobs_incomplete_page_rejected(self):
        self.reader._opener=FakeOpener([{"total_count":2,"jobs":[]}])
        with self.assertRaises(ProviderReadError):
            self.reader.latest_jobs("owner/repo",123)
    def test_jobs_over_cap_rejected(self):
        self.reader._opener=FakeOpener([{"total_count":1001,"jobs":[]}])
        with self.assertRaises(ProviderReadError):
            self.reader.latest_jobs("owner/repo",123)
    def test_invalid_run_identifier_rejected(self):
        with self.assertRaises(ProviderReadError):
            self.reader.workflow_run("owner/repo",0)
    def test_uses_no_mutation_http_method(self):
        self.reader._opener=FakeOpener([{"id":RID}, {"ref":"refs/heads/design/new"}])
        self.reader.repository("owner/repo")
        self.reader.branch_ref("owner/repo","design/new")
        self.assertTrue(all(r.get_method()=="GET" for r in self.reader._opener.requests))

if __name__=="__main__":
    unittest.main()
