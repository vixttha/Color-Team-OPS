# CTO-V002-SINGLE-THREAD — M1 Yellow multi-assignment bridge handoff

**Scope and source:** Issue #8. Gate 0 master integration baseline `e8694fdd6d68b4ea10fc396e5a2215a3402fab74`; Yellow newer reference at `72d09023f9edc29638f26d734262905346069bb3`.

## Yellow Worker

Selective import of exactly two changed source blobs from tested Yellow reentry work: `policy_v002/host_runtime.py`, `tests/test_v002_yellow_host.py`. No divergent-branch merge, no replacement of D1–D5 identity/evidence contracts. Separate Yellow source successfully completed run [41030643107](https://github.com/vixttha/Color-Team-OPS/actions/runs/41030643107) at `72d09023f9edc29638f26d734262905346069bb3`, but this **does not pass tests for this integrated candidate**.

`policy_v002/m1_bridge.py` upgraded to `cto-v002-m1-bridge-3`: sequential multi-task event/journal/gate/receipt correlation, one distinct provider claim+receipt per completed task, exact source/task/criterion/authorization scope, Head dispatch from HEAD_READY then HEAD_DECISION after each audit, and synthetic D2 PASS always remaining UNVERIFIED. First/second/third task stages cannot overlap. Audit summary allows Yellow reentry after Orange but never duplicates the identity. Aggregated D2 gate records must cover all the task-scoped claims.

`tests/test_v002_m1_multitask.py` adds 22 new *authored* cases, including three-task Yellow→Orange→Yellow fixture, forged/replayed receipts/tasks/events, missing second audit, exhausted handoffs, stale SHA, missing worker, revocation and forged gate link. The existing `test_v002_m1_bridge.py` is version-pinned to v3 and its malformed criterion expectation updated to a typed rejection.

**Critical repair boundary:** the current engine validates one successful Worker report per task. `local_repairs > 0` is **NOT** promoted to authenticated history without a separate signed/ordered repair-event schema. The bridge explicitly returns `UNVERIFIED / REPAIR_EVENT_TRACE_UNAVAILABLE` instead of assuming that a worker's self-reported repair count proves a repair. In-task repair acceptance therefore remains **OPEN** for M1, even though Head can reassign the same team under a fresh task and finite handoff limit.

## Validation and trust limits

- Reentry source two Git blobs were copied exactly, and the previously executed Yellow-run SHA was checked. New M1 bridge code and 22 tests have been **authored but have not been executed in an exact-source native Python CI run**.
- No automatic invocation of owner personal runners. For a private GitHub repository, GitHub-hosted Actions can consume billable minutes, so hosted CI was not silently triggered without an approved cost ceiling.
- No authentic ChatGPT-host user-grant issuer, immutable cloud revocation service, same-host role independence, global cross-session lock or production write gateway exists in this change.
- This is a **development reference only**, NOT Head-approved M1 release acceptance. The separate Validate and Internal Auditor must run the whole integrated source before any PASS claim. Source/host authorization is still unverified.

## Suggested next Head action

Keep Yellow on the currently scoped M1 defect until repaired and genuinely tested. Orange must audit new consent/role/receipt code if it becomes security-active. Do not move to M2 completion or owner release approval merely because a multi-task fixture was authored.
