"""CI-only HTTPS GitHub provider smoke. NO mission authorization is implied."""
import os
from policy_v002.github_provider import GitHubRESTReader

REPO="vixttha/Color-Team-OPS"
RID=1439026865
RUN=41005643330
SHA="64e23731bc889909614494bb88cbb6da2abbf37f"
BRANCH="design/v0.0.2-team-contracts-single-lane"
STEPS={"linux":"Validate schemas and negative cases (Linux)",
       "windows":"Validate schemas and negative cases (Windows)"}

def main():
    if os.environ.get("GITHUB_REPOSITORY")!=REPO:
        raise RuntimeError("Invalid live-provider testing scope")
    token=os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing ephemeral GitHub token")
    reader=GitHubRESTReader(lambda:token,timeout=15)
    repo=reader.repository(REPO)
    assert repo["id"]==RID and repo["full_name"]==REPO
    run=reader.workflow_run(REPO,RUN)
    assert run["id"]==RUN and run["head_sha"]==SHA and run["head_branch"]==BRANCH
    assert run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success"
    assert run["repository"]["id"]==RID and run["head_repository"]["id"]==RID
    assert run["path"]==".github/workflows/v0.0.2-contract-prototype.yml"
    jobs=reader.attempt_jobs(REPO,RUN,1)
    assert {j["name"] for j in jobs}==set(STEPS)
    for job in jobs:
        assert job["head_sha"]==SHA and job["run_id"]==RUN
        assert job["status"]=="completed" and job["conclusion"]=="success"
        steps=[s for s in job["steps"] if s.get("name")==STEPS[job["name"]]]
        assert len(steps)==1 and steps[0]["status"]=="completed" and steps[0]["conclusion"]=="success"
    print("D4_LIVE_GITHUB_READER_VERIFIED",RUN,SHA,"required_jobs",len(jobs))
    print("D4_HOST_USER_AUTHORIZATION_NOT_ATTESTED")

if __name__=="__main__":
    main()
