# CTO-V002-SINGLE-THREAD — Orange M1 authority-boundary review and Head decision

**Security-review code revision:** `92c69b8b3fd97eb7b404d361e89909419a7ba39b`. **Scope:** M1 bridge only.

## Orange worker findings
Nine adversarial mutations were submitted against the original reference bridge: foreign work order and Worker mission IDs, stale work/Worker SHA, foreign Validate gate, foreign transition mission ID, stale transition SHA, foreign Head decision mission ID and altered authorization reference. All nine **initially reached the generic aligned/unverified status** instead of explicit contradiction rejection. This did not award authentication; the bridge never returns PASS, but concealed contradictory evidence that would have complicated a future host integration.

Orange added strict exact-mission/sha/authorization matching to work and Worker events, transitions, aggregate gates and Head decision, with nine regression cases in `tests/test_v002_m1_orange.py`. Core data adapters remain provider-neutral, read-only and fail closed.

## Validate
The corrected source was reproduced in an isolated cloud-side sandbox and its `git hash-object` matched the GitHub source blob `326ae2cd7c6e945095123a8968ef9fb1566c3840`. The committed Orange test file matched blob `09d6c6e58bd84082ebf7fb267f2128ff7ae29a85`.

**Observed:** `43/43` sandbox cases PASS (34 M1 tests + 9 Orange security regressions). The D2 policy and Yellow journal imports were sandbox test substitutes; **a complete repository-wide test at this commit was NOT performed**. A GitHub Actions run on this integration branch was not observed. The previous 260/260 Yellow baseline belongs to a different source SHA.

## Internal Auditor challenge
The new checks reject the nine cross-record inconsistencies with specific BLOCKED outcomes. A simulated fake D2 PASS remains `UNVERIFIED` in the bridge. Host-issued user consent, verifier identity, externally protected immutable mission ledger, cloud write gateway and cross-session global lock are still missing. No independent human or protected-host auditor identity was present; this is the distinct logical Internal Auditor phase in the same conversation.

**Audit verdict:** `M1_SECURITY_BOUNDARY_REFERENCE_PASS`, `REAL_HOST_AUTH_UNVERIFIED`, `RELEASE_BLOCKED`.

## Head decision
Head **accepts this scoped M1 source-and-security work for development continuation**, not as production-authenticated mission completion, M1 production readiness, or v0.0.2 release acceptance. No new hosted infrastructure, service vendor, runner runtime prerequisite, merge or publication is authorized.

**Next specialist (one active): Yellow, M2.** Reasons: the next task is canonical registry and searchable capability metadata engineering, not a new security operation. No fixed nine-team queue. Source branches Purple/Yellow remain historical inputs; only `integration/v0.0.2-master-single-thread` may receive writes.

### M2 Yellow work order
Build one versioned canonical nine-team directory with stable capability IDs, conditional triggers, exclusions, evidence expectations, provider/tool requirements **without assuming grants**, and lazy one-team playbook references; allow deterministic search and reject duplicate aliases, unknown teams, unapproved capabilities or an attempt to grant tool rights. Do not import the 36 idea records as shipped features; their Purple proposals remain separate and unapproved. Add negative tests and a bounded single-lane referral to Validate → Internal Auditor → Head. Preserve exactly nine teams and three coordination skills, the mission state authority and the locked cloud-only, provider-neutral requirements.

**Stop:** exact source divergence, unsupported GitHub permission, implied production authentication, paid vendor resource, release/merge requirement or auto-dispatch by the team directory.
