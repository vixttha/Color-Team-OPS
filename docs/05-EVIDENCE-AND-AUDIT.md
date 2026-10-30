# 05 — Authority, evidence, validation and Internal Auditor

## Trust boundary
An LLM-authored mission, JSON property, tool result body, repository file, issue comment or worker summary is **not itself authenticated permission or test evidence**. The source of truth is the host/tool's authenticated identity, authorized scope and externally retrievable event/commit evidence. The v0.0.1 `docs/CONTRACT-TRUST-MODEL.md` recognizes this limitation; the future design must not weaken it.

## Minimal evidence record (proposed)
Every observation should bind: mission ID, task/team, tool/provider identity, action/target, immutable source revision (where applicable), event/run ID, timestamp, evidence URL/reference, reported outcome, and whether provenance was independently checked. Missing identity or trustworthy evidence is UNVERIFIED; failure is not silently converted into success.

## Two separate checking layers
**Team-local self-check:** worker knows its specialty, tests its own deliverable, repairs within mandate, reports all uncertainty. Self-check alone cannot close the mission.

**Mission Validate:** verification-gate function compares worker's claim to source/CI/tool observations, acceptance criteria, authorization and actual revision. At least PASS/FAIL/UNVERIFIED; fake receipts, missing results, stale revisions, nonexistent jobs or unsupported tools do not pass.

**Internal Auditor:** distinct read-only challenge in the *same conversation*. It checks both worker and validation completeness, asks what was not tested, probes unexpected changes, contradictory receipts, security/authority gaps, stale source and possible regressions. Reports PASS / REPAIR / BLOCKED / UNVERIFIED with concrete findings. Auditor cannot override FAIL/UNVERIFIED validation, grant authority, merge a release or impersonate another actor.

**Head:** final accountable decision. Neither persuasive narrative nor confidence can replace missing evidence.

## Suggested audit decision matrix
| Validate | Internal Auditor | Head may do |
| --- | --- | --- |
| PASS | PASS | Continue to next required specialist or COMPLETE if all final checks and scope met |
| FAIL | any | Bounded repair or BLOCKED; never COMPLETE |
| UNVERIFIED | any | Obtain trusted proof or return UNVERIFIED/CAPABILITY_BLOCKED |
| PASS | REPAIR | Bounded repair; invalidate stale acceptance after source changes |
| PASS | BLOCKED | BLOCKED / policy escalation |
| PASS | UNVERIFIED | Evidence follow-up or UNVERIFIED, not COMPLETE |

## Source and identity safeguards
- Worker and auditor identity labels are claims unless attached to host-authenticated actor information.
- Track exact branch, repository and commit SHA; no free-form `HEAD` as a trusted revision.
- Verify no concurrent conflicting writes before advancing where supported; if global enforcement absent, disclose.
- Every materially changed SHA invalidates prior source-bound final PASS until applicable revalidation.
- Prevent evidence replay/duplicate events, mutation of saved receipts, non-monotonic phase skipping, fake tool IDs, inconsistent actor role and stale authorization.
- Enforce authorization outside prompt text when host/cloud tooling supports it; do not promise a secure external enforcement service in a skills-only plugin.
- Bounded budgets/retries and clear stop conditions; no silent endless loops.

## Ordinary completion versus release permission
**Ordinary authorized mission:** no mandatory external auditor thread. Head can conclude technical completion after its required validation and internal audit phases in one conversation where host capabilities allow.

**Externally regulated release or protected-branch merge:** a real reviewer/approver may still be required by provider governance. Mark internal work complete yet the release gate `BLOCKED_EXTERNAL_APPROVAL` when the required external authorization is absent. Do not falsely say an external review was performed.

## Failure examples that must be tested
Fake PASS JSON; forged `observed_by`; nonexistent CI run; stale SHA; green test of previous revision; unapproved branch write; worker selecting next team; auditor self-certifying independence; White team treated as code auditor; invalid phase transition; duplicated event; no cloud tool available; conflicting write lane; attempts to require local/user runners.

## Selected provenance policy for future design
Use a tiered `CLAIMED → OBSERVED → CORROBORATED → CRITERION_VERIFIED` evidence model. Evidence Resolver is a **Verification Gate function, not a new specialist**. All outcomes must bind to actual permissioned provider records and exact acceptance criteria; source SHA, run status and executed steps matter. Absent authenticated resolution remains UNVERIFIED, never narrative PASS. See [Decision CTO-002-B](11-AUTHENTICATED-EVIDENCE-DECISION.md).
