# 10 — Decision CTO-002-A: single-lane ownership and safe cloud writes

**Status:** SELECTED DESIGN CANDIDATE for future v0.0.2. Not built, deployed, tested or approved as release functionality.
**Protected user requirement:** exactly one ordinary user-facing conversation; one Head; one active specialist Worker at a time; no second auditor conversation; no user-owned runner or local service needed.

## Decide the meaning of "one lane"
1. **Logical lane (mandatory for every supported session):** one active Worker *within a mission*. Head alone makes team assignments and final decisions. Team self-repair does not create another Worker. The conversation's host may pause or require explicit approvals.
2. **Exclusive mutable resource lane (enforced only when trusted cloud gateway is available):** for a given repository and authorized branch/resource, only a holder of a valid, fenced cloud lease can submit a write through the controlled gateway. This prevents cooperating plugin sessions from writing concurrently **through that gateway**.
3. **Global cross-conversation exclusivity is not guaranteed by skills alone**, nor by a database row if other apps/users can write directly to GitHub. A claim of full exclusivity is permitted only where all relevant mutations are mediated or GitHub-side restrictions prevent bypass. No claim that ChatGPT forbids a user from opening a second chat.

## Options assessed
| Alternative | Benefit | Defect / decision |
| --- | --- | --- |
| Prompt instruction / in-chat state only | Cloud-free and portable | No cross-session enforcement; retain as honest skills-only guidance |
| Redis TTL lock alone | Simple coordination | Lease expiry, stale actor and fencing issues; do not use as sole correctness primitive |
| Managed SQL transaction + monotonic fencing + write gateway | Auditable atomic state transitions and conflict control | Needs separately authorized cloud service; **preferred optional enforced mode** |
| User runners / local daemon | Would be easy to run development tasks | **Prohibited as plugin/runtime dependency** |
| Multiple Head processes or mandatory auditor chat | Possible isolation | Violates single-thread simplicity goal; reject |

Primary implementation candidate: a **provider-managed PostgreSQL-compatible transactional store**, not a mandated provider or subscription. Use `SELECT ... FOR UPDATE` or a guarded conditional UPDATE and a **database-generated increasing fence**. Durable row authority survives chat restarts only when cloud state was actually provisioned. Do not equate row lock with complete GitHub write exclusion.

## Proposed state (not a v0.0.1 schema)
```text
missions: (mission_id PK, owner_subject, status, phase, active_team,
           required_teams, contract_version, immutable_scope, revision, etag)
resource_leases: (resource_key PK, mission_id, holder_session, lease_until,
                  fencing_epoch BIGINT, status)
actions: (action_id UNIQUE, mission_id, resource_key, fence, expected_sha,
          requested_operation_digest, auth_ref, status, result_ref, created_at)
audit_events: (event_id UNIQUE, mission_id, phase, actor, action_id,
               source_sha, evidence_ref, previous_hash, event_hash, time)
```
Store no user credentials or raw secrets in Git; the cloud service must use encrypted provider-managed secret storage, restricted audit access and retention limits.

## Transactional acquire and renewal
- Authenticated request `acquire(mission_id, owner_session, resource_key, expected_etag)`. Resolve mission, owner, authorization, allowed target and active phase *from trusted service state*, not user-supplied JSON.
- In one database transaction: lock the lease/resource row, reject unexpired leases owned by another live session, verify intended one active Worker, increment monotonic `fencing_epoch`, assign holder, expiry and mission etag; commit. If no row exists, create it under unique `resource_key` and handle unique-conflict retries.
- A lease alone does **not** make a write safe. On **every mutation** verify unexpired holder, latest fence, mission authorization, matching phase, action idempotency and expected SHA at the server-side write boundary. Reject old fences.
- Renew with compare-and-swap using holder, fence, etag and server time; never rely on model-generated heartbeat promises. If lease expires, stop the old holder. A new holder gets a higher fence. An expired holder must reacquire and reread state.
- Release on explicit terminal state; when the host disappears, a bounded lease expires. Claiming "released" requires an observed service result. A lost reply produces `UNKNOWN_OUTCOME` and read-only reconciliation, never an automatic duplicate write.
- Scope lock on `repository_id + branch_ref` (or other exact writable resource), not merely the conversational mission ID, to avoid different missions writing the same branch. A user may have multiple read-only missions; never silently stop unrelated conversations.

## GitHub mutation gap
GitHub APIs do not understand Color Team OPS fencing epochs. Therefore **all plugin-controlled writes requiring exclusivity must travel through the authorized gateway**; gateway serializes writes for the same resource and checks GitHub's actual branch/ref state before updating. Prefer GitHub compare-and-swap or an expected-source-SHA guard when the chosen API supports it, with non-force fast-forward ref moves; never rely solely on a prior DB read. Prevent direct bypass using repo permission restrictions if strict global exclusivity is a requirement. If unrestricted direct writes exist, report `SINGLE_LANE_ENFORCED=FALSE` despite a valid internal lease.

With an external tool that cannot accept fencing or compare-and-swap, either gate it behind a serialized gateway operation with trusted post-action reconciliation or **block the mutation** if safety cannot be established. Do not promise atomicity across the DB transaction and GitHub HTTP request.

## Skills-only behavior and failures
- Basic supported-host skills remain usable with **no backend**: Head directs one sequential team in the conversation, builds proposed patches, researches and reviews. Scope-limited tool writes can occur only under existing explicit permissions and must be reported `GLOBAL_EXCLUSIVITY_UNVERIFIED`; for tasks requiring guaranteed exclusivity, **CAPABILITY_BLOCKED**, not speculative success.
- No mandatory cloud service, pricing plan, persistence, server, lock API, automation, local PC or GitHub runner for the basic experience.
- When a lease/auth service is unavailable, revoked, timed out, partitioned or returning ambiguous results, reject further high-impact writes, report the exact blocker, and permit read-only analysis.
- A stolen, stale or replayed lease token cannot grant extra user authorization; ownership + current scope + provider action permission are all separately required.

## Acceptance tests (NOT RUN)
Simultaneous acquires on same branch (only one succeeds); parallel missions same resource; old fence after expiry; renewal race; lost response; duplicate action_id; crash between DB claim and GitHub write; GitHub 409/non-fast-forward; revoked scope mid-mission; direct GitHub writer bypass detection; host interruption; second conversation; cloud outage; failed cleanup; user runner offline. Invariant: **no successful gateway-mediated write by an unauthorized/stale-fence actor**. A broader "nothing else can ever write GitHub" invariant needs provider-side exclusivity proof.

## Authoritative grounding
- PostgreSQL transaction/row locks: https://www.postgresql.org/docs/current/sql-select.html and https://www.postgresql.org/docs/current/transaction-iso.html
- Redis on fencing and expiry caveats: https://redis.io/docs/latest/develop/use/patterns/distributed-locks/
- GitHub ref update fast-forward semantics: https://docs.github.com/en/rest/git/refs
- OWASP action-specific approval and independent tool validation: https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
