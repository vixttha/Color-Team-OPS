"""Development-only live check of GitHub Issue #7, no production role authority."""
import os
from policy_v002.github_provider import GitHubRESTReader
from policy_v002.pilot_provenance import PilotScope, inspect_read_only_pilot

SCOPE=PilotScope(
    repository="vixttha/Color-Team-OPS",
    repository_id=1439026865,
    issue_number=7,
    account_id=237333433,
    acting_app="chatgpt-codex-connector",
    branch="design/v0.0.2-team-contracts-single-lane",
    historical_source_sha="2d77eb25a185fad37bec55b97be60f26eb15b47c",
    run_id=41007120206,
    run_attempt=1,
    workflow_path=".github/workflows/v0.0.2-contract-prototype.yml",
    required_job_steps=(
        ("windows","Validate schemas and negative cases (Windows)"),
        ("linux","Validate schemas and negative cases (Linux)"),
        ("live-github-provider-read","Live GitHub REST read-only smoke"),
    ),
)

def main():
    if os.environ.get("GITHUB_REPOSITORY")!=SCOPE.repository:
        raise RuntimeError("Unexpected live provenance target")
    token=os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Ephemeral GitHub Actions token is required")
    reader=GitHubRESTReader(lambda:token,timeout=15)
    verdict=inspect_read_only_pilot(reader,SCOPE)
    print("D5_GITHUB_PROVIDER_RESULT",verdict.provider_status,verdict.code)
    print("D5_ROLE_AUTHORITY_RESULT",verdict.role_authority_status)
    if verdict.provider_status!="OBSERVED" or verdict.role_authority_status!="UNVERIFIED":
        raise RuntimeError("D5 must verify exact provider facts without promoting role authority")

if __name__=="__main__":
    main()
