# PrismCell Workbench v0.0.1

Reusable single-specialist, single-thread, GitHub-persistent workcell template for Color-Team-OPS and future authorized projects.

**Product isolation:** This is NOT the installed Color-Team-OPS plugin, not Development HQ, not Purple Review HQ, not a tenth specialist or a fourth coordinator. A team workcell is a documentation/work/evidence workspace with a standing specialist identity, not an independent authenticated AI process. Work happens only on an invoked session or separately authorized scheduled task.

## Deployment

- One `TEAM-WORKBENCH/` directory on exactly one owned home branch per existing color specialist (nine teams total).
- Four original workspaces are preserved; PrismCell is **added**, not a destructive migration.
- Five new workcell branches originate from minimal `main` rather than a stale product source snapshot. Each retrieves the latest actual integration source **read-only** before analyzing. Do not assume home branch contains current product source.
- Source-of-truth product development continues at `integration/v0.0.2-master-single-thread`; optional library and existing HQ branches remain untouched.
- Every recipient has one GitHub Issue INCALL thread; local inbox/outbox ledgers are snapshots/references, not an automatically synchronized bus.

## Read order for any team invocation

1. `TEAM-WORKBENCH/README.md`, `IDENTITY.md`, `SCOPE.md`, `WORKFLOW.md`.
2. `STATE.json`, `WORK-QUEUE.json`, `HEAD-HANDOFF.md`, `INCALL/README.md`.
3. Existing legacy team files (if present). Never overwrite legacy registers without accepted, source-specific reconciliation.
4. Current GitHub branch heads and latest owner authority; confirm one authorized writer and current integration SHA.
5. Pick one bounded same-specialist assignment; Head → Worker → Validate → logical Internal Auditor → Head.
6. Commit only home-branch records in current scope; re-read and use expected-head update lease; publish source-linked in-call messages only through authorized GitHub issue comments.

See CONTRACT.md, INCALL-PROTOCOL.md, LONG-RUNNING-OPERATIONS.md, PROMOTION.md, TEAM-MATRIX.md, schemas and audit.

## Production use of the *workcell* (not a continuously running agent)

PrismCell v0.0.1 is ready for **on-demand, user-invoked nine-team work**. Start from [AGENT-LAUNCHPAD.md](AGENT-LAUNCHPAD.md), follow [STARTUP.md](STARTUP.md) and inspect [OPERATIONAL-ACCEPTANCE.md](OPERATIONAL-ACCEPTANCE.md). The connected account is an administrator, so there is **no independently proven per-agent branch ACL**. Each invocation must reread current GitHub evidence before acting. This does not authorize installed Color-Team-OPS plugin release or autonomous work.
