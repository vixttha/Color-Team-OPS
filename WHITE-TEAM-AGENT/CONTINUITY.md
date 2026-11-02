# Long-horizon continuity — weeks and months

## What persists

The Git branch holds a durable identity, dated session records, task/finding IDs, immutable source observations and cumulative governance decisions. A new chat can recover this context by reading the branch. Model memory alone is not considered the official record.

## What does not persist automatically

There is no always-running White agent, hidden timer, autonomous background workflow or guaranteed automatic restart just because the branch exists. Work resumes on a user-directed session, or through a separately authorized real scheduling/automation capability. Do not claim work occurred in gaps.

## Every working session

Start: read README → IDENTITY → AUTHORITY → STATE.json → TASK-QUEUE → latest sessions/; refresh live repo refs before decisions. Choose at most one active White work order.

During: keep raw observed evidence references, exact Git SHA and tool time. If development branch advances, distinguish historical PASS from new untested HEAD. Do not overwrite prior audit evidence.

Finish: add a dated, uniquely numbered sessions/YYYY-MM-DD-NNN.md; update task/finding status and decision log with provenance; update STATE.json; commit ONLY agent home and verify the commit. If interrupted, mark BLOCKED/IN_PROGRESS with next exact action, not COMPLETE.

## Weekly cadence (performed only when invoked)

- Refresh repo branch inventory and integration SHA.
- Compare prior vs current release gate status and latest exact-SHA CI.
- Recheck owner decisions and plugin version without modifying them.
- Revisit high-severity open findings and validation/host/evaluation gaps.
- Flag stale or contradictory audit labels.
- Record a WEEKLY_REVIEW session with deltas, remaining risks and concrete next steps.
- Do not manufacture a weekly entry for a week with no actual tool-backed work.

## Monthly archival

Add a month-end report under audits/ when requested or when an actual session covers it. Archive resolved findings by setting RESOLVED_AT_SHA with validation reference; do not erase their history. Version agent charter changes as explicit decisions.

## Cross-session handoff packet

Use templates/HANDOFF.md. Minimum: mission, current task ID, live branch HEAD, reviewed subject SHA, evidence receipts, owner instructions, what was and wasn't verified, active limits, safe next step and prohibitions. This is guidance to a future session, not authenticated permission.

## Concurrency

Use exact prior branch HEAD as an optimistic lease for each write; on change, reread and reconcile rather than clobber another session. The Home branch is intentionally separate from integration and other specialist homes. No global writer lock is asserted.
