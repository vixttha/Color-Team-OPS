# Issue #4 — Head-Controlled Single-Lane Mission-State Contract (prototype)

**Status:** DESIGN PROTOTYPE, audit completed in bounded simulation; **not approved for v0.0.1, not integrated or released**.
**Branch:** `design/issue-4-single-lane-contract`, founded on `main` at `a28c2908da47d16dbdf7e55eb29a0c1ce9b6c7d3`.
**Related:** https://github.com/vixttha/Color-Team-OPS/issues/4

## Locked proposed cycle

**HEAD → WORKER (one active color team) → VALIDATE → INTERNAL AUDITOR → HEAD**

> The Head is accountable for completion, the teams are accountable for their work, and the validation evidence is accountable for the claims.

The Head logically composes the existing Mission Control and OPS Director skills. A worker is one of the existing nine specialist teams. Validation uses a trusted test/tool observation. The Internal Auditor is a distinct *within-conversation review phase*, not automatically an external reviewer or a new color team. Head alone routes or finishes. No new required chat threads or thirteenth skill.

## Proposed source contract

Configuration includes `mission_id`, 40-hex immutable reference `source_sha`, `allowed_teams`, **explicit `required_teams`**, `allowed_actions`, `required_validation`, `required_audit`, `max_repairs`, `max_dispatches`, external review requirement, author identity, and authorized repo/branch scope if writes are claimed. The required team set must be a subset of allowed teams. **No JSON field is authentication.**

A worker cannot choose the next team, advance phases or approve itself. A team self-repair must be authorized by Head and within the bounded repair budget. Every team required by the mission must be verified on the **final source SHA**; source change invalidates all prior revision passes. One in-memory mission permits one active worker; a global cross-chat/write-lane mutex requires separate cloud enforcement not supplied by this prototype.

## Phase transition contract

| From | Event / authorized owner | To | Gate |
| --- | --- | --- | --- |
| HEAD | Head dispatch | WORKER | Allowed team, available dispatch budget, previous cycle accepted |
| WORKER | Worker submits claimed work, exact SHA | VALIDATE | Allowed write scope for source changes; claim is untrusted |
| VALIDATE | Evidence checks via trusted resolver | AUDIT | PASS, FAIL, UNVERIFIED; always record result |
| AUDIT | Separate internal challenge checks | HEAD | Audit cannot override failed/unverified validation |
| HEAD | Head retries same team | WORKER | Failed/incomplete cycle and remaining repair budget |
| HEAD | Head dispatches next team | WORKER | Prior cycle PASS and routing authorized |
| HEAD | Head completes | TERMINAL | Both gates PASS, all required teams PASS at current SHA, fresh trusted HEAD SHA check |
| HEAD | Head stops | TERMINAL | Reasoned BLOCKED, CAPABILITY_BLOCKED, IDLE or UNVERIFIED |

**External approval rule:** If an approval from a truly separate actor is required but not authenticated, the correct terminal state is `BLOCKED_EXTERNAL_APPROVAL` with `internal_complete=true`. An internally successful audit does not grant GitHub reviewer approval. Even fully complete work never auto-merges/releases/deploys.

**Permanent runner independence law (verbatim):**

> Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate.

## Three executed simulated missions

1. Clean: Yellow team -> both source-bound gates PASS -> Head COMPLETE.
2. Repair: Orange team -> validation FAIL -> audit FAIL -> Head bounded same-team repair -> new SHA -> both gates PASS -> Head COMPLETE.
3. External gate: Green team -> validation PASS -> internal audit PASS -> Head `internal_complete=true`, `BLOCKED_EXTERNAL_APPROVAL` due to missing authenticated external approval.

The simulation uses *fake trusted adapter fixtures*. It is **not real GitHub CI, real external reviewer approval, or live ChatGPT plugin acceptance**.

## Internal adversarial test evidence

A standalone Python reference implementation, two Draft 2020-12 schemas, three simulations, developer-only tests, and audit report were tested in an ephemeral build environment: **33/33 unit tests passed**. They include phase skips, unauthorized team/write, bad/missing/reused or stale evidence, same-team retry/dispatch caps, internal-audit failure, all-required-team completion, source revision invalidation, current-source recheck, release self-review, schema positive/negative cases, and terminal-state behavior.

**Distribution:** The executable ZIP and its local SHA-256 are provided in the design conversation; this GitHub branch records the architecture contract and audit synopsis, **not yet the executable ZIP's full source**. Do not claim repository CI validated the Python prototype.

## Audit findings

| Severity | Finding | Outcome |
| --- | --- | --- |
| High | Head could complete before all required team passes | Repaired in executable prototype with required-team pass map |
| High | Arbitrary external approval object could be accepted | Replaced with trusted-resolver lookup; production authentication remains OPEN |
| Medium | Finalization lacked fresh remote SHA check | Added resolver-backed current-source check |
| Medium | Evidence refs could repeat / snapshot mutate internal history | Added duplicate check and event copying |
| Medium | Premade state injection via constructor | Prevented from public constructor |
| High / OPEN | Caller-provided resolver is not authentication | **Production integration BLOCKER**; verified adapter required |
| High / OPEN | No global cross-session write lock | **Production enforcement BLOCKER**; one lane per in-memory mission only |
| High / OPEN | Repository identity, authorization and actual reviewer privileges unverified | **Production integration BLOCKER** |
| Medium / OPEN | No durable signed audit trail or resumable execution | Deferred |

**Internal verdict:** Pass for the narrow *simulated state-machine logic*. **Blocked for production trust enforcement or live/plugin release.** An author-associated internal audit is not a genuinely independent reviewer.

## Sources

- OpenAI manager/orchestrator pattern: https://developers.openai.com/api/docs/guides/agents/orchestration
- NIST SSDF PW.7 review/analysis: https://pages.nist.gov/nccoe-devsecops/example-implementation-1-2/appendix-c.html
- GitHub author self-approval rule: https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews

**Isolation:** Do not cherry-pick or merge into `release/v0.0.1-cloud-only`. Do not waive hosted CI, plugin parity, live skill tests, or independent release review for v0.0.1. After v0.0.1 approval, review this separate prototype and import its verified source with exact-SHA evidence.