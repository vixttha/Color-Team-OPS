# 02 — Head-controlled single-lane architecture

## Logical topology

```text
USER (one conversation)
    |
HEAD = mission-control (authority) + ops-director (routing)
    |  mission contract + authorization + acceptance + budget
    v
ACTIVE WORKER = exactly one of nine existing specialists
    |  bounded execute -> self-check -> local repair -> completion event
    v
VALIDATE = verification-gate evidence phase
    |  trusted observation + acceptance + exact source SHA
    v
INTERNAL AUDITOR = distinct read-only challenge phase
    |  attempt to falsify worker/validator claims
    v
HEAD = accept | repair same worker | dispatch next permitted worker
    |      |               |
    |      +---- bounded --+
    +--> complete | idle | blocked | capability_blocked | unverified
```

Neither validation nor audit is a permanently assigned color team. White governs exercise rules, Purple correlates attack/defense signals, and neither substitutes for the generic internal auditor.

## Roles, permissions and handoffs
- **Head** owns mission identity, initial scope, authorization, required/allowed teams, permitted tools/actions, budgets, stop rules, acceptance criteria, routing, final decision. No skill alone authorizes a cloud tool action.
- **Worker** executes one scoped task, chooses specialist *methods* within scope, performs bounded self-review, returns evidence, limitations, suggested next specialist. Worker **cannot** expand scope, dispatch other teams, silently bypass a gate or declare mission-level PASS.
- **Validate** checks external tool observations, test outcomes, exact source revision, action scope and acceptance. It never turns a string-shaped claim into trusted verification.
- **Internal Auditor** examines an evidence-focused view (mission contract, original criteria, diff, trusted receipts, finding coverage, residual risk) and searches for omissions/contradictions. It is logically distinct but need not be a separate process, model, thread or human.
- **Head** takes the gate results and alone decides retry, another team, complete or truthful blocked outcome. Head cannot override absent verification by declaring it observed.

## One lane, two meanings
**Single-thread UX:** user can conduct an ordinary mission in one supported host conversation. The host may require explicit user action/approval and may not maintain tool continuity.

**One active writer per mission:** at most one active worker performs scoped writes; read-only checks happen sequentially. This can be specified in a portable contract. It is *not a global mutex* without a separately authorized cloud lock. If multiple chats start the same mission, instruction-only prevention is UNVERIFIED.

No new conversation is required for the internal auditor; no automatic outside reviewer is a default dependency.

## Suggested future states (proposal, not existing v0.0.1 schema)
`HEAD_READY`, `WORKER_ACTIVE`, `VALIDATION_PENDING`, `INTERNAL_AUDIT_PENDING`, `HEAD_DECISION`, `COMPLETE`, `IDLE`, `BLOCKED`, `CAPABILITY_BLOCKED`, `UNVERIFIED`, `BLOCKED_EXTERNAL_APPROVAL`.

| From | To | Required gate |
| --- | --- | --- |
| HEAD_READY / HEAD_DECISION | WORKER_ACTIVE | Head dispatch; team allowed; tools and budget authorized; no other active worker |
| WORKER_ACTIVE | VALIDATION_PENDING | Worker completion event; revised SHA and evidence claims; bounded local repairs exhausted or complete |
| VALIDATION_PENDING | INTERNAL_AUDIT_PENDING | Record PASS / FAIL / UNVERIFIED validation; never skip audit by hiding failure |
| INTERNAL_AUDIT_PENDING | HEAD_DECISION | Record challenge verdict and uncovered/remaining issues; audit cannot upgrade failed validation |
| HEAD_DECISION | WORKER_ACTIVE | Head-authorized same-team repair or next permitted specialist; budget/progress checks |
| HEAD_DECISION | COMPLETE | Required acceptance, relevant team completion, validation AND audit PASS for current trusted revision; no outstanding mandatory internal work |
| HEAD_DECISION | BLOCKED_EXTERNAL_APPROVAL | Internal work meets acceptance; **separate release gate** needs authenticated outside actor |
| Any stage | truthful terminal/block state | Unsupported tool, stale/invalid proof, conflicting write, exhausted budget, no progress, revoked authority or unsafe impact |

## Source revision discipline
All source-bound worker/gate claims are labeled with the immutable commit SHA and mission/task ID. Material source edits render prior exact-revision acceptance stale. Required checks must run or be re-established by trusted evidence for the final source. The prototype's conservative approach is to invalidate all prior revision-bound passes; any selective reuse needs an independently verified dependency/impact rule, not model assertion.

## Bounded repair discipline
Local repairs: within existing assigned scope, action permission, and finite per-worker limit. If an issue changes permissions, changes target team, exhausts retries, or needs independent authorization, return to Head. No team can create new work merely to remain active.

Head-level dispatch: at most one team selected per decision; track work fingerprint, status, attempt number, source revision, previous findings, elapsed/cost budget, and progress. Fail closed on loops.

## External release gate
Completing a technical mission is not the same as merging or publishing. If external approval is required by repo policy, report internal completion separately from unfulfilled release authorization. No default independent auditor **conversation** is needed to complete ordinary internal work.

## Cloud-enforced exclusive writes (optional future mode)
The base one-chat protocol above does **not** create a global lock. The selected future design uses a provider-managed transactional mission/resource record and monotonically increasing fencing epoch, checked at a controlled write gateway; every write also rechecks GitHub target revision. Only gateway-mediated operations can be claimed exclusive, and direct provider writes require separate restrictions. In absence of enforcement, guaranteed-single-writer mutations are CAPABILITY_BLOCKED rather than claimed safe. See [Decision CTO-002-A](10-SINGLE-LANE-LOCKING-DECISION.md).
