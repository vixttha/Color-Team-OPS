# CTO-V002-SINGLE-THREAD — M1 bounded in-task repair extension

**Worker:** Yellow. **Scope:** isolated master integration branch only.

## Development behavior

The existing `CloudAuthorityEngine` now accepts a *backward-compatible optional*, exact-consent-bound `max_local_repairs` key. Omission means **zero** repairs, and a signed request may allow **0, 1, or 2** attempts. Requests outside the bound are rejected. Each in-task repair requires a Head `head_repair` principal, exact current revision, valid mission/source and `VALIDATION_PENDING` phase, and is recorded as a `REPAIR_ORDERED` journal event. The task returns to `WORKER_ACTIVE` for the same authenticated-by-adapter Worker subject; a distinct principal is blocked. All consumed receipts remain in `used_receipts` to prevent replay, and a repair history preserves task ID, prior receipt, Head subject, event ID and repair number across development-store restart.

The original `Yellow → Orange → Yellow` assignment reentry repair from `feature/v0.0.2-yellow-live-host-readiness` was preserved by exact Git blob. The bridge `cto-v002-m1-bridge-4` checks multiple ordinary completed assignments, explicit unique event/receipt/criterion links, and per-task gates. Signed optional repair budgets are matched to the D2 mission budget, but **extra in-task retry events are NOT YET mapped into D2's versioned transition attestation contract**. The bridge deliberately returns `UNVERIFIED / REPAIR_EVENT_TRACE_UNAVAILABLE` for those cases. This is a remaining M1 release blocker, not a false PASS.

**New authored test counts:** 70 Yellow host tests (including repeat-team, two allowed retries, replay, impersonation, expiry, restart, and budget failures), 34 legacy M1 bridge tests and 25 M1 multi-task tests. These have **not** been natively executed together at this integrated SHA. Historic Yellow reference `72d09023f9edc29638f26d734262905346069bb3` passed its **263/263** dual-platform suite at separate SHA ([run 41030643107](https://github.com/vixttha/Color-Team-OPS/actions/runs/41030643107)); its observed pass cannot be attributed to this candidate.

**No live host impersonation:** the reference IdentityBoundary, EvidenceBoundary, SQLite journal and test fixtures are development-only. User-consent issuance, protected multi-tenant durable ledger, actual signed gate/repair event source, zero-cost hosted integration and cross-chat writer enforcement remain unsupported/unverified. No provider is mandated.

**Native validation command for a separately authorized cloud test environment:** `python -B -m unittest discover -s tests -p 'test_v002_*.py' -v`, plus `python -B -m unittest discover -s tests -p 'test_package.py' -v`. Run from repository checkout pinned to the exact source SHA with supported `jsonschema` dependency; verify source and test hashes. Do not invoke user-owned runners automatically. For private repos, GitHub-hosted test runners may consume billable minutes outside the included allowance.

**Head gate classification:** `WORKER_CODE_COMMITTED_PENDING_NATIVE_VALIDATE`; `PRODUCTION_AUTH_UNVERIFIED`; `M1_IN_TASK_REPAIR_TRACE_INCOMPLETE`. The mission remains one version, and all M2–M5 previously developed source stays on the same branch.
