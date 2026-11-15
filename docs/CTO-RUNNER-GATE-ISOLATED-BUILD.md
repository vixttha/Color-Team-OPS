# CTO-V002 — isolated owner-runner trust-gate development build

**Status:** DEVELOPMENT CANDIDATE ONLY / BOTH HOSTS NOT VERIFIED / RUNNER TRUST STOP ACTIVE / RELEASE_BLOCKED.

**Base branch:** `integration/v0.0.2-master-single-thread` at commit `228c199070ed670b459662ffb22a1c9e88c1e9b9` (read back November 14, 2026). **Destination:** isolated, non-runner-triggering feature branch; preserve integration/master, main, installed private 0.0.7 staging, canonical v0.0.1, frozen evaluation and earlier runner-gate history.

## Why this build exists

The owner requested a real isolated branch with working development-only code, rather than a handoff ZIP. Existing v0.2 historical ZIP is identified in the original audit by SHA-256 `3933de4ac648938ab28b4a270361209a9582b2d0a593418464049d31e4c16c6d` but its raw bytes **could not be retrieved in this session**. This is a **new candidate implementation of the documented v0.2 security contract**, not a verified patch of or replacement for the original v0.2 archive. Before promotion the next agent must compare them line by line and preserve useful original protections; no original source bytes are claimed to have been reused.

## Included in development-only branch

- `devtools/runner_trust_gate/admission.py`: pure strict identity/expiry verification + protected host approval-file lookup; no token fetching or GitHub mutations. Requires exact repository, executable SHA, workflow file ref and workflow SHA, YAML job key, GitHub run ID, run attempt, runner name and runner OS. The exact numeric GitHub *job ID* is not guaranteed in pre-job default variables and is **NOT** included in this prototype; host evidence should bind it post-execution. Any required pre-job identity that is unavailable results in DENY.
- `devtools/runner_trust_gate/pre_job_linux.sh`: admin-install template, GNU `timeout` 15s + 2s forced kill; exit nonzero stops the job.
- `devtools/runner_trust_gate/pre_job_windows.ps1`: admin-install template, PowerShell ACL/owner/ancestor checks plus 15s process deadline and `taskkill /T /F` on timeouts. **Native PowerShell syntax, group/ACL behavior and interpreter paths not verified here.**
- `tests/test_runner_trust_gate.py`: pure offline tests; no CI workflow enabled and no jobs started.
- This note. No `skills/` or plugin manifest edits and no `.github/workflows/` edits.

## Security boundaries

1. Approval records are *made by the owner or admin-controlled process*, not by ChatGPT, repo contents, workflow env, issue comments or CI jobs. Store only in a **host administrator-controlled location** (`/etc/color-team-ops/runner-gate/approvals` or `C:\CTOPSRunnerGate\approvals`). Do not copy approval records into the repository.
2. The hook *and Python interpreter, guard code, approval file and every ancestor* must be protected against runner-service-account changes; runner service must be unprivileged. On Linux the code checks root ownership and group/world mutability of approval path/ancestors. On Windows the protected PowerShell hook performs ACL inspection, which requires native acceptance before relying on it.
3. The hook must be configured outside the runner application/work folder, by an administrator. The owner must review the runner's `.env` or service-environment ACL; a malicious job must never disable the pre-job hook for the next job.
4. A GitHub commit, issue, PR comment, label or environment value is **never** permission by itself. Each owner approval must be exact identity and valid for no longer than 15 minutes.
5. **Replay gap:** the candidate binds run ID, attempt, YAML job key and runner name, so reuse against a different attempt/job is denied. It **does not provide an administrator-protected atomic one-use receipt store** to reject a duplicate of the identical run/attempt/job. To satisfy the original v0.2 acceptance plan, the implementing agent must add and native-test replay control or obtain explicit owner approval of the bounded residual risk. Do not claim one-use enforcement now.
6. **Host pre-job identity gap:** determine experimentally which `GITHUB_*` variables and workflow SHA actually exist before job steps. Required field missing => DENY; do not replace with self-reported workflow data.
7. **Windows ACL gap:** verify SID checks with actual runner service identity and Windows file system semantics; inspect protected `.env`, installed wrapper and Python executable. The installed hook must be the reviewed protected copy; the repo source cannot itself enforce host installation.
8. `GITHUB_SHA` may differ from what `actions/checkout` checks out in PR workflows; native approval must bind the exact executable SHA and checkout SHA and should not trust push/PR metadata alone.
9. No runner dispatch, reruns, model calls, protected-file writes, merges, release actions, plugin packaging changes, added paid compute or remote host installation are part of this branch.

## Exact-format owner-admin approval example (FICTIONAL, DO NOT INSTALL)

The filename must be `<run_id>-<attempt>-<job_key>-<runner>.json`. Only the administrator writes it to the protected approvals directory after checking the actual pending GitHub job and executable workflow source. Strings are matched **byte-for-byte**; nonmatching or expired records are denied.

```json
{
  "schema": 1,
  "repository": "vixttha/Color-Team-OPS",
  "sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "workflow_ref": "vixttha/Color-Team-OPS/.github/workflows/v0.0.2-integration-native.yml@refs/heads/integration/v0.0.2-master-single-thread",
  "workflow_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "job_key": "linux",
  "runner": "color-team-ops-linux-01",
  "runner_os": "Linux",
  "run_id": "42100000000",
  "attempt": "1",
  "issued_at": "2026-11-14T18:59:00Z",
  "expires_at": "2026-11-14T19:04:00Z"
}
```

## Acceptance gates before enabling any real job

- [ ] Exact original v0.2 ZIP re-obtained; hash checked and implementation diff reviewed, no historical evidence overwritten.
- [ ] Windows: admin verifies interpreter/wrapper, all ACLs and runner configuration; native PowerShell parser, timeout/child tree termination tested.
- [ ] Linux: admin verifies protected path and service-account non-root, hook environment and timeout/forced kill tested.
- [ ] Both: GitHub pre-job default variables captured safely and compared with GitHub job metadata without leaking secrets.
- [ ] Both: missing approval, wrong SHA, workflow ref/workflow SHA, repo, job key, run/attempt, runner name/OS, stale permit, forged/malformed JSON, symlink/parent replacement, replay and timeout are all denied **before any workflow step starts**.
- [ ] Both: one genuinely admin-approved exact-job positive execution, logs and checkout SHA captured with job/run/attempt and runner identity.
- [ ] Replay-control design and actual one-use enforcement are accepted (currently NOT implemented).
- [ ] Head and owner explicitly reassess runner trust stop; no automatic relaxation.

**Current disposition: isolated source candidate and synthetic tests only.** Never call this runner-gate installation complete, host verified or release ready.