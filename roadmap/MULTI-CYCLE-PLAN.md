# RED TEAM AGENT — multi-cycle investigation roadmap

**A planning horizon, NOT a background schedule.** Each cycle resumes only when invoked with an available tool and authorization. New integration changes may reorder work.

## Cycle 1 — Inventory and attack surface
RED-W001 branch/tree/permissions risk map; RED-W002 runner CI trust; RED-W012 patch/drift watch. Deliver accurate inventory and severity with exploit prerequisites.

## Cycle 2 — Identity, evidence and agent controls
RED-W003 authority/gate boundaries, RED-W004 forged/stale receipts and retry replay, RED-W005 prompt injection and cross-team privilege assumptions. Deliver controlled negative-case specifications and source-bound results where actually run.

## Cycle 3 — Portability, supply chain and optional utilities
RED-W006 optional library file safety; RED-W007 deterministic package and installed-vs-repo provenance; RED-W008 cross-host portability. Keep product runtime cloud-only and any local/owner runner use optional development testing.

## Cycle 4 — Genuine host trials and release readiness
RED-W009 independent specialist case evaluations; RED-W010 real installed-v0.0.2 host attack/denial trials **only if a safe, authorized candidate exists**; RED-W011 final risk contradiction audit for Head. Never release or merge automatically.

## Ongoing rules across many weeks
Each session reviews and preserves failures, source drift, new fixes, residual risks and next task in `worklog/`, `audits/` and `state/`. Reopen previously closed findings if a new exact source revision regresses. The same threat can span multiple work sessions; distinguish attempts from distinct test cases and avoid false completeness.

## Completion criteria
- All findings are `REMEDIATED_AND_RETESTED`, `ACCEPTED_RISK_BY_OWNER` or explicitly `OPEN/BLOCKED` with evidence.
- No severe claim lacks an actual source or host observation.
- Release status remains separately owner-controlled, including when source and host work pass.
