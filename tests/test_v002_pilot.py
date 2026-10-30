"""D5 provider-provenance test suite; all records below are SYNTHETIC fixtures."""
import copy
import unittest
from dataclasses import replace

from policy_v002.pilot_provenance import PilotScope, inspect_read_only_pilot
from policy_v002.github_provider import GitHubRESTReader, ProviderReadError
from test_v002_github import FakeOpener

SHA="2d77eb25a185fad37bec55b97be60f26eb15b47c"
APP="chatgpt-codex-connector"
ID=237333433
RID=1439026865
RUN=41007120206
ISSUE=7
REPO="vixttha/Color-Team-OPS"
BRANCH="design/v0.0.2-team-contracts-single-lane"
WORKFLOW=".github/workflows/v0.0.2-contract-prototype.yml"
JOBS=(
    ("windows","Validate schemas and negative cases (Windows)"),
    ("linux","Validate schemas and negative cases (Linux)"),
    ("live-github-provider-read","Live GitHub REST read-only smoke"),
)


def scope():
    return PilotScope(REPO,RID,ISSUE,ID,APP,BRANCH,SHA,RUN,1,WORKFLOW,JOBS)


def record(phase,index):
    stamp="2026-10-30T05:"+str(20+index).zfill(2)+":01Z"
    return dict(id=6515000000+index,created_at=stamp,updated_at=stamp,
                user={"id":ID},performed_via_github_app={"slug":APP},
                body="Pilot phase "+phase+"; claimed logical role only.")


class PilotFixture:
    def __init__(self):
        self.repo=dict(id=RID,full_name=REPO,private=True)
        self.issue_record=dict(number=ISSUE,state="open",created_at="2026-10-30T05:20:00Z",
            user={"id":ID},performed_via_github_app={"slug":APP})
        self.comments=[record("D5-0"+str(i),i) for i in range(1,6)]
        self.run=dict(id=RUN,run_attempt=1,event="push",status="completed",conclusion="success",
            head_sha=SHA,head_branch=BRANCH,path=WORKFLOW,
            repository={"id":RID},head_repository={"id":RID})
        self.jobs=[
            dict(id=100+i,run_id=RUN,head_sha=SHA,name=name,
                 status="completed",conclusion="success",
                 steps=[dict(name=step,status="completed",conclusion="success")])
            for i,(name,step) in enumerate(JOBS)
        ]
    def repository(self,repo):
        return copy.deepcopy(self.repo)
    def issue(self,repo,n):
        return copy.deepcopy(self.issue_record)
    def issue_comments(self,repo,n):
        return copy.deepcopy(self.comments)
    def workflow_run(self,repo,run):
        return copy.deepcopy(self.run)
    def attempt_jobs(self,repo,run,attempt):
        return copy.deepcopy(self.jobs)


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.reader=PilotFixture()
        self.scope=scope()
    def value(self):
        return inspect_read_only_pilot(self.reader,self.scope)
    def expect(self,status,code):
        result=self.value()
        self.assertEqual((result.provider_status,result.code),(status,code),result)
        self.assertEqual(result.role_authority_status,"UNVERIFIED")
    def test_valid_records_are_observations_only(self):
        self.expect("OBSERVED","PROVIDER_EVIDENCE_OBSERVED_ROLE_AUTHORITY_UNVERIFIED")
    def test_no_authenticated_head_claim(self):
        self.assertNotEqual(self.value().role_authority_status,"PASS")
    def test_bad_repository_id(self):
        self.reader.repo["id"]+=1
        self.expect("BLOCKED","REPOSITORY_MISMATCH")
    def test_public_repository_when_private_expected(self):
        self.reader.repo["private"]=False
        self.expect("BLOCKED","REPOSITORY_MISMATCH")
    def test_issue_wrong_number(self):
        self.reader.issue_record["number"]=10
        self.expect("BLOCKED","ISSUE_MISMATCH")
    def test_issue_closed(self):
        self.reader.issue_record["state"]="closed"
        self.expect("BLOCKED","ISSUE_MISMATCH")
    def test_issue_author_mismatch(self):
        self.reader.issue_record["user"]["id"]=1
        self.expect("BLOCKED","ISSUER_ATTRIBUTION_MISMATCH")
    def test_issue_app_mismatch(self):
        self.reader.issue_record["performed_via_github_app"]["slug"]="another-app"
        self.expect("BLOCKED","ISSUER_ATTRIBUTION_MISMATCH")
    def test_missing_worker_record(self):
        self.reader.comments.pop(1)
        self.expect("UNVERIFIED","INCOMPLETE_OR_CHANGED_TRACE")
    def test_added_record_makes_trace_unverified(self):
        self.reader.comments.append(record("D5-06",6))
        self.expect("UNVERIFIED","INCOMPLETE_OR_CHANGED_TRACE")
    def test_edited_validator_record(self):
        self.reader.comments[2]["updated_at"]="2026-10-30T05:29:01Z"
        self.expect("UNVERIFIED","EVENT_EDITED")
    def test_comment_author_mismatch(self):
        self.reader.comments[3]["user"]["id"]=77
        self.expect("BLOCKED","EVENT_ATTRIBUTION_MISMATCH")
    def test_comment_app_mismatch(self):
        self.reader.comments[2]["performed_via_github_app"]["slug"]="unknown"
        self.expect("BLOCKED","EVENT_ATTRIBUTION_MISMATCH")
    def test_claimed_stage_out_of_order(self):
        self.reader.comments[1]["body"]="D5-04 untrusted"
        self.expect("BLOCKED","PHASE_CLAIM_MISMATCH")
    def test_reordered_event_ids(self):
        self.reader.comments[2]["id"]=2
        self.expect("BLOCKED","EVENT_ORDER_INVALID")
    def test_reordered_timestamps(self):
        self.reader.comments[2]["created_at"]="2026-10-30T05:19:01Z"
        self.reader.comments[2]["updated_at"]="2026-10-30T05:19:01Z"
        self.expect("BLOCKED","EVENT_ORDER_INVALID")
    def test_bad_timestamp_blocks_proof(self):
        self.reader.comments[1]["created_at"]="invalid"
        self.expect("UNVERIFIED","PROVIDER_READ_UNAVAILABLE")
    def test_wrong_run_id(self):
        self.reader.run["id"]=123
        self.expect("BLOCKED","WORKFLOW_SCOPE_MISMATCH")
    def test_wrong_run_attempt(self):
        self.reader.run["run_attempt"]=2
        self.expect("BLOCKED","WORKFLOW_SCOPE_MISMATCH")
    def test_wrong_source_sha(self):
        self.reader.run["head_sha"]="b"*40
        self.expect("BLOCKED","WORKFLOW_SCOPE_MISMATCH")
    def test_wrong_head_repo(self):
        self.reader.run["head_repository"]["id"]=0
        self.expect("BLOCKED","WORKFLOW_SCOPE_MISMATCH")
    def test_wrong_workflow_path(self):
        self.reader.run["path"]="other.yml"
        self.expect("BLOCKED","WORKFLOW_SCOPE_MISMATCH")
    def test_cancelled_ci_is_unverified(self):
        self.reader.run["conclusion"]="cancelled"
        self.expect("UNVERIFIED","WORKFLOW_NOT_SUCCESSFUL")
    def test_failed_ci_is_unverified(self):
        self.reader.run["conclusion"]="failure"
        self.expect("UNVERIFIED","WORKFLOW_NOT_SUCCESSFUL")
    def test_job_missing(self):
        self.reader.jobs.pop()
        self.expect("UNVERIFIED","REQUIRED_JOBS_MISSING")
    def test_job_wrong_sha(self):
        self.reader.jobs[0]["head_sha"]="b"*40
        self.expect("BLOCKED","JOB_EVIDENCE_MISMATCH")
    def test_job_run_id_mismatch(self):
        self.reader.jobs[0]["run_id"]=1
        self.expect("BLOCKED","JOB_EVIDENCE_MISMATCH")
    def test_job_failure(self):
        self.reader.jobs[0]["conclusion"]="failure"
        self.expect("BLOCKED","JOB_EVIDENCE_MISMATCH")
    def test_required_step_missing(self):
        self.reader.jobs[0]["steps"]=[]
        self.expect("UNVERIFIED","REQUIRED_TEST_STEP_NOT_VERIFIED")
    def test_required_step_skipped(self):
        self.reader.jobs[1]["steps"][0]["conclusion"]="skipped"
        self.expect("UNVERIFIED","REQUIRED_TEST_STEP_NOT_VERIFIED")
    def test_unreachable_provider(self):
        def fail(*args):
            raise ProviderReadError("provider not available")
        self.reader.issue_comments=fail
        self.expect("UNVERIFIED","PROVIDER_READ_UNAVAILABLE")
    def test_invalid_scope_fails_closed(self):
        self.scope=replace(self.scope,account_id=0)
        self.expect("BLOCKED","INVALID_PILOT_SCOPE")
    def test_later_development_commit_does_not_change_historical_ci(self):
        # The pilot scope deliberately binds a historical SHA, never current branch HEAD.
        self.assertEqual(self.value().provider_status,"OBSERVED")


class RESTIssueEndpointTests(unittest.TestCase):
    def setUp(self):
        self.reader=GitHubRESTReader(lambda:"SYNTHETIC_TOKEN")
    def test_issue_get_only(self):
        self.reader._opener=FakeOpener([{"number":ISSUE}])
        self.reader.issue(REPO,ISSUE)
        req=self.reader._opener.requests[0]
        self.assertEqual(req.get_method(),"GET")
        self.assertEqual(req.full_url,"https://api.github.com/repos/"+REPO+"/issues/7")
    def test_issue_wrong_number_rejected(self):
        with self.assertRaises(ProviderReadError):
            self.reader.issue(REPO,0)
    def test_comment_list_one_page(self):
        self.reader._opener=FakeOpener([[{"id":1}]])
        records=self.reader.issue_comments(REPO,ISSUE)
        self.assertEqual(len(records),1)
        self.assertIn("/issues/7/comments?per_page=100&page=1",
                      self.reader._opener.requests[0].full_url)
    def test_comment_pagination(self):
        first=[{"id":i} for i in range(1,101)]
        second=[{"id":101}]
        self.reader._opener=FakeOpener([first,second])
        self.assertEqual(len(self.reader.issue_comments(REPO,ISSUE)),101)
    def test_duplicate_comment_ids_rejected(self):
        self.reader._opener=FakeOpener([[{"id":1},{"id":1}]])
        with self.assertRaises(ProviderReadError):
            self.reader.issue_comments(REPO,ISSUE)
    def test_non_array_comment_response_rejected(self):
        self.reader._opener=FakeOpener([{"id":1}])
        with self.assertRaises(ProviderReadError):
            self.reader.issue_comments(REPO,ISSUE)
    def test_bad_repository_locator_rejected(self):
        with self.assertRaises(ProviderReadError):
            self.reader.issue_comments("../repo",ISSUE)

if __name__=="__main__":
    unittest.main()
