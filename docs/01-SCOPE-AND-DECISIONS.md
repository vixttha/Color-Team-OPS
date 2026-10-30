# 01 — Scope, user decisions and open design choices

## User-established direction to preserve
- The product uses **one ChatGPT conversation** for an ordinary mission and a **single Head-controlled execution lane**.
- The chosen logical cycle is **HEAD → WORKER → VALIDATE → INTERNAL AUDITOR → HEAD**.
- No separate auditor conversation or independent auditor is required merely to complete an **ordinary internal mission**.
- Team specialists are **not fixed to workflow stages**: any of nine teams can be Worker, while the Head alone chooses the next team.
- Each active team performs a bounded **execute → self-check → local repair → report** loop.
- The Head is accountable for completion; teams are accountable for work; observed validation evidence is accountable for claims.
- All nine must be distinct specialists, not nine rebranded generic prompt stencils.
- There are **12 skills total**: nine specialists (Yellow, Orange, Green, Blue, Red, Purple, White, Black, Gray Cell) and three coordinating skills (Mission Control, OPS Director, Verification Gate). The Internal Auditor is a phase, **not a tenth specialist or thirteenth skill**.
- Future v0.0.2 concepts must be isolated from ongoing v0.0.1 release development.
- **Binding law, verbatim:** "Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate."

## Existing baseline, not modified by this branch
The v0.0.1 Constitution L1–L10: cloud-only, optional user runners for development/testing but never plugin/runtime dependency; portability claims bounded by host support; finite autonomy; least privilege; evidence before routing; separation of responsibilities; fail-closed completion; portable accountability; evidence-based releases. A future v0.0.2 must be evaluated for consistency with these laws rather than silently superseding them.

The current nine responsibilities follow the source skill descriptions, **not historical shorthand that swaps team meanings**:
- Yellow: ordinary software features, bug fixes, refactors and functional tests.
- Orange: security-aware software design and remediation.
- Green: cloud operations, deployment, reliability, observability and DevSecOps.
- Blue: defense, threat detection, incident response and recovery.
- Red: authorized adversarial testing.
- Purple: offensive/defensive evidence correlation and retesting.
- White: rules of engagement, neutral oversight, authority and adjudication; **not automatic code-audit ownership**.
- Black: dated, grounded adversary threat intelligence and relevance.
- Gray Cell: synthetic user behavior, human-error and UX misuse exercises.

## Proposal status classification
**Preserved user design direction**: one conversation, Head/Worker/Validate/Internal Auditor/Head cycle, nine specializations, no default external auditor thread, no runtime dependency on personal runners.

**Proposed design details requiring future approval**: precise field names and state machine, per-specialist playbook depth, benchmark case counts and thresholds, escalation mapping, risk-tiered audit methods, future cloud enforcement architecture, backward-compatible schema migration.

**Not implemented / not verified**: continuous autonomous execution, global mission locks, verified host identity/authorization service, cloud evidence resolver, cross-host portability, real behavioral benchmark outcomes, independent reviewer certification or any v0.0.2 plugin release.

## Explicit non-goals
No rewriting/deleting the v0.0.1 branch, `main`, Issue #4, its prototype, installed plugin or current CI. No extra required worker process, auditor chat, new 13th skill, local runner, local daemon, local database, cloud backend mandated for basic skill guidance, automatic merges/releases, privilege escalation, infinite retry loops or false claims of independent approval.

## Governance distinction
An internally verified mission may conclude inside the same thread. If an externally governed release action needs a *real separate approver*, the **release authorization** remains blocked until that approval exists. An internal audit cannot impersonate that person or override branch rules. Do not convert every ordinary mission into an externally dependent process.

## Design constraints to resolve through testing
- Whether local self-repairs consume the same budget as Head-level redispatches.
- Which checks must rerun after a source change; safe optimization may reuse genuinely still-valid evidence, but never fake final-revision PASS.
- How a host distinguishes internal challenge phase from external actor identity.
- Which specialist reference material is authoritative, versioned and maintainable.
- Whether dedicated cloud state/lock enforcement becomes an optional enhanced mode without degrading cloud-only skills-first operation.
