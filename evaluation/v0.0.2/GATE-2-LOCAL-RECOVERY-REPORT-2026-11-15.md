# Gate 2 local recovery report and agent handoff

Recorded 2026-11-15 UTC (2026-11-14 America/New_York). Status: **BLOCKED**. Development evaluation only; **RELEASE_BLOCKED**.

This is an agent-authored report of direct local command observations, not an independent certification. Private evidence remains on owner-controlled local storage. This document includes safe receipt identifiers and hashes only; no private prompts, credentials, raw transcripts, or private checkpoint files are published.

## Authority and scope

The owner authorized Head -> Worker -> Validate -> logical Internal Auditor -> Head in one session, with no additional reviewers or infrastructure. Exactly one additional candidate invocation was authorized for blue-team:edge:05 / no_handoff / attempt 2, gpt-6.1-sol, medium effort, existing ChatGPT subscription, tools disabled, read-only permissions. The original frozen semantic grader could use its original maximum two attempts.

The owner required the genuine original checkpoint to pass the prepared preflight before regression tests or execution. A genuine integrity, authentication, security, or execution blocker requires stopping rather than bypassing protections. This recovery authorization was not exercised: zero candidate and zero grader invocations occurred.

The subsequent owner instruction authorized documenting this result in GitHub. That documentation-only authority does not authorize a code fix, model retry, workflow dispatch, merge, plugin change, deployment, or release.

## Repository and inspected revisions

- Repository: vixttha/Color-Team-OPS.
- Local original checkout: C:\Users\bukto\Desktop\Color-Team-OPS-Project\Color-Team-OPS-Agent\Color-Team-OPS.
- Original local branch: feature/v0.0.2-codex-independent-eval.
- Original local branch tip, preserved: ece8db6488cd78d36b41b0f6faf3d4c6d631bccb.
- Recovery PR: https://github.com/vixttha/Color-Team-OPS/pull/24.
- Inspected PR head: 2235162650544ce80a6bd4ba3b924593ab0c1db4.
- PR base: a09a3226e73b55b1542ad485824f559002dc5c01; verified ancestor of the inspected head.
- At completion of recovery inspection, the original checkout was clean and detached at the inspected PR head. No local branch was advanced.
- PR #24 remained open and unmerged. Its head was unchanged.

Read global AGENTS.md and repository docs/CONSTITUTION.md, docs/01-SCOPE-AND-DECISIONS.md, docs/05-EVIDENCE-AND-AUDIT.md, and devtools/SOLO_EVAL.md. No repository AGENTS.md or PROJECT-LAWS.md was found.

PR base-to-head comparison verified exactly six development-only paths:

1. devtools/solo_eval_candidate_recovery.py
2. devtools/solo_eval_candidate_recovery_pipeline.py
3. devtools/solo_eval_resume_batch.py
4. tests/test_solo_eval_candidate_recovery.py
5. tests/test_solo_eval_candidate_recovery_pipeline.py
6. tests/test_solo_eval_resume_batch.py

The older local branch tip predates additional baseline tooling and workflow files already present in the PR ancestry. Those inherited files are not additions made by the six-file PR. Selecting the exact reviewed revision locally did not edit workflow definitions or dispatch them.

## Original checkpoint: directly verified

Original checkpoint directory, relative to the checkout:

.cli-eval-private/solo-v1/116c8468e98bfed123c7014586c6791114f2d57b596cb8af918192c437d3186b/

Freeze: evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v2.json.

- Canonical evaluator digest: 116c8468e98bfed123c7014586c6791114f2d57b596cb8af918192c437d3186b.
- Freeze file byte SHA-256: 52fe6beda104f96dbcb56f28a5517d3eadd0b23f46f20d8ec3def99b20bacdc7.
- These are different hash representations, not an integrity mismatch.
- Actual frozen source SHA: f789912bee3b8e50d323244299f3bf4e61969055.
- 1,080 frozen case-arm pairs; all 44 protected source-file hashes valid.
- 209 unique completed candidate responses and 209 corresponding provisional grades.
- Pilot acceptance present and bound to verified evidence.
- No duplicate completed pairs; no supervisor lock.
- Candidate receipt outcomes: 209 COMPLETED, one QUOTA_BLOCKED.
- Grader receipt outcomes: 209 GRADED, one historical QUOTA_BLOCKED. No unresolved grader terminal obstruction.
- Recorded graded critical pairs: zero. Recorded graded contradiction pairs: zero. These are provisional-grade observations, not independent semantic certification.
- The sole candidate obstruction is blue-team:edge:05 / no_handoff / attempt 1 / QUOTA_BLOCKED.

The existing full read-only auditor completed successfully:

```powershell
python -B -m devtools.solo_eval_quality_audit --freeze evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v2.json
```

This verified existing candidate/grader raw receipts and bindings. It is not a post-recovery audit, because recovery did not execute.

## Required preflight: failed closed

At clean detached HEAD 2235162650544ce80a6bd4ba3b924593ab0c1db4:

```powershell
python -B -m devtools.solo_eval_candidate_recovery_pipeline check --freeze evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v2.json
```

Sanitized output:

```json
{"disposition":"GATE_2_EXECUTION_BLOCKED","error_class":"Invalid","release":"RELEASE_BLOCKED"}
```

A read-only diagnostic invocation of preflight identified the underlying code: FROZEN_CANDIDATE_CONTRACT_CHANGED.

At devtools/solo_eval_candidate_recovery.py:25, EXPECTED_SOURCE_SHA is:

f789912bee3b0e50d323244299f3bf4e61969055

The authentic original freeze and resume supervisor instead bind:

f789912bee3b8e50d323244299f3bf4e61969055

The difference is ...3b0e... versus ...3b8e.... The mismatch was reproduced with the exact PR revision and a clean worktree. No constant, frozen source, rubric, or checkpoint was changed to bypass it.

### Preparation detail

Initially the reviewed development files and baseline dependencies were loaded into the older clean checkout as ten untracked files. The first preflight therefore stopped at DIRTY_RUN_SOURCE before reaching the incorrect SHA constant. All ten files were verified against the PR blobs with Git CRLF conversion accounted for, then only those agent-introduced files were removed before switching to the exact PR revision. The final worktree was clean, and the source-binding failure above was then reproduced. No pre-existing user changes were overwritten.

## Regression tests and execution

Both required test commands are NOT_RUN because Phase 1 did not pass:

```powershell
python -B -m unittest discover -s tests -p 'test_solo_eval_candidate_recovery*.py' -q
python -B -m unittest discover -s tests -p 'test_solo_eval_resume_batch.py' -q
```

Do not reinterpret PR #24's earlier synthetic-test results as native test results from this mission. No dependencies were installed. Native test isolation and retry behavior remain unverified by these tests in this mission.

- execute-once: NOT_RUN, never invoked.
- New candidate calls: 0.
- Candidate attempt 2 directory: absent.
- New grader calls: 0.
- New candidate or grader receipt identifiers: none.
- Authentication and execution-environment checks: not reached; no current authentication/capability claim.
- Post-recovery receipt audit: NOT_RUN; existing-checkpoint audit passed separately.

## Counts before and after

| Evidence | Before | After |
| --- | ---: | ---: |
| Unique completed candidates | 209 | 209 |
| Corresponding provisional grades | 209 | 209 |
| Original quota-blocked candidate attempt 1 | 1 | 1 |
| New candidate attempt 2 | 0 | 0 |
| Frozen matrix total | 1080 | 1080 |

871 matrix pairs remain without completed candidates. Gate 2's bounded recovery target of 210 candidates and 210 grades was not reached; it would not itself complete the full matrix.

## Safe receipt references and preservation evidence

Original target receipt identifier relative to the checkpoint:
candidates/560092e56edf66da15608f18/1/receipt.json

Original attempt-1 file SHA-256 values:

| File | SHA-256 |
| --- | --- |
| input.json | 99ddb1b83c5e3b991a1d659f00b2a62bb45ab385e35d2f9762b9e99057934a59 |
| stdout.jsonl | 51d002440e52e9eeefb4a7e176d260766b728dcf6d6e34ad35290c7443fb9f2c |
| stderr.txt | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| receipt.json | a4dc9e9b15432e778a23c67db9e7b939471628a40b706ac2842fecad92638494 |

A before/after hash comparison verified all 2,311 original checkpoint files unchanged, with zero added or missing files. Both installed local plugin cache trees were also unchanged: color-team-ops, 28 files; color-team-ops-v002-staging, 33 files. Total: 2,372 files compared, zero changes, additions, or deletions.

Local-only preservation manifest:
C:\Users\bukto\AppData\Local\Temp\color-team-gate2-20261114-before.json

Manifest SHA-256:
4cf282e6d8ba10295f210dd21ecd8ab3c71187c67fe964856661302fdde22a71

The manifest remains local and is not uploaded. The report records local verification; agents without these private bytes cannot independently reproduce checkpoint validation from GitHub alone.

## Three logical audits and Head decision

- Audit A, evidence integrity: PASS for existing evidence preservation. Original 209 evaluations and quota-blocked attempt 1 unchanged; frozen hashes valid; no duplicate completed pairs. New attempt authenticity is not assessable because no attempt 2 exists.
- Audit B, evaluation correctness: BLOCKED. Existing receipt bindings verified, but the recovery code has an incorrect frozen-source binding. No new candidate or grade exists for semantic inspection.
- Audit C, operational safety: PASS for recovery actions performed. No workflow dispatch, runner operation, paid execution, push, merge, deployment, publication, or plugin-management write occurred during recovery. Local checkout selection and read-only checks occurred. The later documentation publication is separately owner-authorized and must not be confused with recovery execution.

Head verdict: **Gate 2 BLOCKED**. Preserve RELEASE_BLOCKED. This is one agent's logically separate audits, not an invented independent human/team review.

## Handoff for the next agent

1. Read current instructions and this report; verify current remote revision and original local evidence again. Do not assume this timestamped state is still current.
2. Resolve the recovery module's incorrect expected source SHA through a separately authorized, reviewed development change. This report applies no fix and grants no execution authority.
3. Preserve the original freeze and all 44 protected files. Do not create a replacement checkpoint, restart the matrix, clean ignored evidence, or move the checkpoint.
4. After an appropriate corrected revision is available cleanly in the original checkout, require the genuine prepared preflight to pass. Then run both native regression commands with actual dependencies and verify no real model calls or historical evidence writes.
5. Validate direct local host authorization, existing subscription authentication, frozen model/effort, tools-disabled/read-only isolation, and absence of a supervisor lock before any model execution. The acknowledgement string does not prove these properties.
6. The original authorization was for exactly one additional candidate attempt 2. Do not infer additional calls from this documentation request. Never rerun execute-once automatically after attempt 2 starts writing; retain any candidate/grader failure evidence.
7. Grade only a genuine candidate with the frozen rubric/model and original two-attempt grader ceiling; inspect semantic contradictions, uncertainty, critical findings, quotations, schema, and bindings. Valid JSON alone is not quality PASS.
8. Rerun the full read-only checkpoint auditor, preservation checks, and three logical audits. Gate 2 requires 210 unique candidates, 210 bound provisional grades, original evidence preserved, exactly one new candidate attempt 2, and no unresolved integrity or critical-security findings.
9. Do not merge PR #24, alter workflows, bypass runner trust stop, dispatch Actions, use paid services, modify either installed plugin, deploy, or publish a release.

## Documentation publication boundary

This report is placed on an isolated docs branch based on inspected PR head 2235162650544ce80a6bd4ba3b924593ab0c1db4, leaving PR #24 and the watched evaluation branch unchanged. Workflow triggers at that inspected revision were checked: push triggers target other explicit branch names; no pull_request trigger was present. A PR #24 conversation comment links this report for discovery. No private checkpoint bytes are included.
