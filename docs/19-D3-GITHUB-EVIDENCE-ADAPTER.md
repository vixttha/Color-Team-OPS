# D3 — GitHub authenticated-evidence adapter, reference integration

**Status: read-only provider integration source written; not production-installed, not a host-identity service.**

The new `policy_v002/github_provider.py` implements GitHub REST read-only calls and `GitHubBackedTrustAdapter` for the D2 verifier. It uses a **protected token supplier** in the actual host integration, TLS, a fixed `api.github.com` origin, no redirects, validated repository/branch identifiers and bounded pagination. No secrets, static tokens, personal runner runtime requirement or GitHub write routes are included.

## Important identity split
**GitHub authentication** establishes what GitHub reports about a repository, branch/ref, workflow run and jobs. It does **not** grant user approval for Color Team OPS to dispatch, change code or declare completion.

**HostAuthority** must independently authenticate (or fail closed on) the user/mission grant, exact repository numeric identity, allowed teams/actions, Head decisions, task dispatch, mission snapshot, ordered transitions and separate Validate/Internal Auditor attestations. A worker-provided JSON claim is never that HostAuthority. The adapter's `HostAuthority` protocol is a boundary *requiring a future protected implementation*; an arbitrary fake host in unit tests is **not** an authenticated mission-state store.

**RunBinding** is a trusted host-created immutable mapping from `run:ID` to mission ID, task ID, criterion ID, repository numeric ID/name, branch, exact source SHA, expected workflow file/event, required job names and **per-job** named executed test steps. The verifier resolves the provider record again from GitHub and rejects an unrelated run, wrong branch, wrong source, wrong repository (including forks), renamed workflow, skipped work, missing jobs/steps, invalid/partial pagination, unknown IDs and unverifiable results.

**Trust levels:** a successful workflow and named steps prove those GitHub-reported checks completed, **not** absence of software bugs. Only a pre-registered criterion with a suitable test suite and observed run supports a narrow PASS. Not all GitHub workflow jobs implement meaningful tests. Head still needs the existing D2 requirement for both distinct verified internal gates at final SHA.

## Observed connected GitHub evidence (manually retrieved, not Python live E2E)
The ChatGPT-connected GitHub tools directly retrieved the private repository `vixttha/Color-Team-OPS`, numeric repository ID `1439026865`, and workflow run `41004395615` at commit `99b30820620b22580dd5c16720fe70a7c132067f`. Run `completed/success`, event `push`, workflow path `.github/workflows/v0.0.2-contract-prototype.yml`, repository and head-repository IDs both `1439026865`, attempt 1. Run jobs named `linux` (ID `123895875663`) and `windows` (ID `123895876038`) both returned `completed/success` with their named contract-validation steps completed successfully.

This is **real authenticated connector read evidence for an earlier D2 commit**, not an executed D3 Python adapter-to-GitHub call, not a current-HEAD D3 test and not a Color Team OPS mission authorization or internal audit attestation. The run can be inspected at https://github.com/vixttha/Color-Team-OPS/actions/runs/41004395615 .

## Required host provisioning (NOT DONE)
A cloud host must provision and protect GitHub App user/installation credentials with least privilege, supply actual user-approved mission grants, trusted mission ledger for Head dispatch/transition/gate records, read-only token rotation and target repository numeric identities. User impersonation must not arise from a mere installation token; if actions are on behalf of a user, use a user-scoped grant as appropriate. No ChatGPT host authorization API is assumed to exist. This repository does not deploy a host or provider installation.

## Test plan
- Synthetic GitHub responses that structurally resemble real run and job payloads; strict mismatch/partial/failed cases.
- Mock HTTP transport verifies GET-only, bounded endpoints, no redirects, secret-free errors, protected token supplier and pagination.
- D2 integration with a host test fixture proves adapter-policy interop, but **NOT host authenticity**.
- The actual connected GitHub run above provides a separate manually checked live observation. Live Python integration remains **NOT EXECUTED** until a secure supported cloud execution environment with authorized token and protected mission ledger exists.

## Scope and non-goals
No 13th skill, no second required auditor conversation, no owner PC/runner/CLI necessary to *use* the plugin, no change to existing nine teams, no always-on runtime dependency. No global single-writer lock or cloud write gateway. No automatic release, merge or production authorization. Never equate "Python unit PASS", provider read success or `GitHubBackedTrustAdapter` instance existence with a production-authenticated end-to-end mission.

Source references:
- https://docs.github.com/en/rest/git/refs
- https://docs.github.com/en/rest/actions/workflow-runs
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app
- https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app
