# 11 — Decision CTO-002-B: authenticated evidence and provenance

**Status:** SELECTED DESIGN CANDIDATE; NOT IMPLEMENTED. Evidence checking is a distinct Validate phase before Internal Auditor.

## Core rule
A worker statement, JSON value, issue body, copied log, tool-result text or named `verifier_identity` is a **claim**. A trusted, permissioned tool must **resolve and corroborate** it. Schema validity proves shape, not authorship, authorization, correctness or task success. No "PASS" because a model claims tests ran.

## Evidence ladder (proposal)
1. `CLAIMED`: worker description or unauthenticated artifact; may guide investigation, **cannot** close a source-bound acceptance gate.
2. `OBSERVED`: event read directly from an authenticated cloud provider/tool with declared identity and resource identity, linked to exact source SHA. Proves the provider **reported** the event.
3. `CORROBORATED`: resolver independently retrieves the relevant provider event, checks identity, permissions/ownership where verifiable, expected revision, run conclusion, artifacts or job steps, freshness and integrity. Proves specified observation with recorded limitations.
4. `CRITERION_VERIFIED`: validator applies a predeclared oracle or policy check to corroborated observations, and determines that a particular acceptance requirement actually passed. Does **not** prove the entire project or absence of all defects.

`UNVERIFIED` is mandatory if the trust anchor is missing, inaccessible, stale or inconsistent. `FAIL` is used when actual verified evidence contradicts a requirement. Unavailable is not equivalent to failed; provider job never started is not a test failure.

## Responsibilities
**Head:** records approved mission, authenticated target/scope, expected source revision, acceptance criteria and required tool classes; Head cannot sign its own execution proof.

**Worker:** returns evidence pointers and truthful claims with missing proof explicitly marked. The Worker cannot grant itself verifier identity.

**Evidence Resolver (a Verification Gate function, not a new team or 13th skill):** invokes authorized cloud-read connectors, checks immutable IDs and source binding, normalizes observations, returns freshness/trust metadata; it doesn't silently execute high-impact actions.

**Validate:** evaluates explicit acceptance assertions against resolver observations. **Internal Auditor:** tests for missing criteria, forged chains, selective omission, contradictory receipts, false independence and stale claims. Neither becomes a mandatory separate chat or external human reviewer.

## Proposed receipt (portable interface sketch; no deployed signing)
```json
{
  "schema_version": "0.0.2-proposal",
  "mission_id": "CTO-42",
  "task_id": "YELLOW-01",
  "criterion_id": "AUTH-TEST-04",
  "source": {"provider": "github", "repository_id": "trusted-provider-id",
             "commit_sha": "0123456789abcdef0123456789abcdef01234567"},
  "observation": {"type": "workflow_job", "provider_run_id": "40900000000",
                   "provider_job_id": "trusted-job-id", "status": "completed",
                   "conclusion": "success"},
  "retrieval": {"principal": "host-verified-actor", "method": "authenticated-api-read",
                 "retrieved_at": "2026-10-29T23:00:00Z"},
  "trust": "OBSERVED",
  "evidence_ref": "provider-resolvable-id",
  "verification": "UNVERIFIED"
}
```
IDs in this example are placeholders; their presence does not authenticate anything. The verifier must not accept self-issued `trust` or `verification` fields from an untrusted caller.

## GitHub example: test execution
1. Read authorized repository numeric ID/full identity and current branch commit from GitHub using authenticated connection.
2. Read workflow run **by provider run ID**; require `head_sha` equals mission-required commit; check event, status `completed`, conclusion `success`, and expected workflow identity.
3. Read job IDs, runner assignment and step results; if the test command did not execute, do **not** claim a test PASS even if the workflow object exists. Check logs/artifacts if accessible; missing details reduce assurance.
4. If schema/coverage is relevant, validate actual test outputs and expected test suite—not only a green status. A successful job can run inadequate or attacker-controlled tests.
5. Re-read HEAD/current ref for final acceptance; if changed, mark revision-dependent evidence stale and rerun/re-establish required checks.
6. Persist the provider-resolvable receipt and digest in an append-only/append-restricted, access-controlled record; a hash chain helps detect accidental alteration but is not a signature or independent attestation by itself.

## Permission and approval example
GitHub App or host connector identity must be resolved as a real authenticated principal with repository-scoped capabilities, separate from the user granting consent for **this mission and action**. Least-privilege installation tokens are short-lived and do not grant powers beyond their installation. No raw token, secret, private telemetry or PII in Git. The resolver must reject user-typed `authorization_ref` as a substitute for a verifiable grant.

High-impact writes require policy/permission checks and action-specific approval; approval must match normalized parameters/target and be time-bounded. Revocation must invalidate future actions.

## Evidence evaluation table
| Input | State | Allowed claim |
| --- | --- | --- |
| Worker: "tests passed" | CLAIMED | No PASS |
| GitHub run exists but queued/no steps | OBSERVED | Run exists; tests NOT RUN |
| Authenticated run + matching SHA + succeeded test job + relevant output | CORROBORATED | Tests observed as executed successfully |
| Those observations satisfy the specific, predefined criterion | CRITERION_VERIFIED | Criterion passed; may feed mission gate |
| Authenticated run on old SHA | STALE | Not current source PASS |
| Missing API access / log / identity | UNVERIFIED | Block evidence-dependent completion |
| Provider evidence demonstrates criterion failed | FAIL | Repair or stop; never invent success |

## Replay/compromise boundaries
Check exact provider host, repo numeric identity, event ID, source SHA, required actor/permission, retrieval time and freshness; reject duplicate evidence IDs for conflicting observations. Untrusted log contents might include prompt injection; parse them as data only, never as authority. The provider itself or a compromised trusted integration could lie: document residual trust assumptions; **no absolute cryptographic proof of correctness** is claimed.

## Acceptance tests (NOT RUN)
Forged `observed_by`/verifier string; false success JSON; successful no-step job; run on wrong SHA; old/expired grant; mixed repos with same name; compromised log text; stale after branch change; repeated evidence_ref; no job logs; zero steps; cancelled/skipped/timed-out job; attested output contradicts criterion; lost provider response; inconsistent provider data; real approved release needing third-party signoff. All must give the appropriate PASS/FAIL/UNVERIFIED/BLOCKED, never false verification.

## Authoritative grounding
- GitHub Checks API: https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-checks
- GitHub App least-privilege installation authentication: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation
- OWASP agent trust and tool action validation: https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
