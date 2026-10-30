# Yellow Team — Host-authority execution foundation

**Implementation branch:** `feature/v0.0.2-yellow-host-authority`. **Source:** existing v0.0.2 development branch at `963533265c21b0c0ae05d3d85846d65630593c08`.

## Owner law

**Keep Color Team OPS cloud-only, provider-neutral, and independent of any specific hosting platform.** CTO-LOCK-001 in `docs/23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md` remains binding. Existing development runners, a storage driver, or a GitHub evidence adapter must never be required to use the plugin.

## What Yellow built

`policy_v002/host_runtime.py` implements a host-neutral, fail-closed mission state engine using explicit four contracts: `IdentityBoundary` (external authentication and exact-intent consent); `EvidenceBoundary` (independent source revision and criterion-specific receipt verification); `JournalPort` (atomic durable CAS and event history); and `CloudAuthorityEngine` (enforced mission state changes). It supports exact-scope consent, Head dispatch, scoped Worker receipt, Validate, separate Internal Auditor re-observation, Head completion, and revocation.

`SQLiteDevelopmentJournal` is a **development/testing driver only**: it persists events across process restart, uses `BEGIN IMMEDIATE` and expected-revision compare-and-swap, unique event IDs, a hash-linked journal and corruption detection. It is neither deployed nor a substitute for a protected multi-tenant cloud database, an immutable third-party audit anchor, or KMS. Provider-neutral production `JournalPort` would need hosted transactional storage and enforced tenant boundaries. No vendor or charge is selected by this reference.

The `IdentityBoundary` adapter must be implemented by the actual protected cloud host and securely bind **explicit user consent to a SHA-256 digest of the exact mission request**. Per-phase action tokens are independently verified by operation and mission; phase role names and records written by an agent never confer authorization themselves. External provider `EvidenceBoundary` must bind task, criterion and SHA and re-read during both Validate and Internal Audit. A green CI run alone is not a grant.

## Strict limitations

- No production authentication provider, hosting deployment, real issuer signing keys, confidential credential manager, cloud revision/revocation database or live real-user mission has been established here.
- The Python driver must never be deployed as-is; even the hash chain can be rewritten by anyone controlling its DB file. Production requires service-enforced append-only integrity and independent audit custody.
- All user/auth/worker/auditor identities in unit tests are **synthetic fixtures**. Role separation is only as authentic as the cloud IdentityBoundary; logical internal audit is not an independently authenticated external person.
- The engine verifies read-only `read/inspect/report` mission scopes only. It performs no provider write action or global exclusive-write enforcement, never claims cloud mutex guarantees and never grants release permission.
- An actual authenticated end-to-end mission through a real cloud host must be demonstrated at the accepted exact source SHA before calling this complete at production level.

## Yellow acceptance

Tests must cover live-like single-lane end-to-end fixture mission, restart persistence, CAS/fencing of stale revisions, duplicate replay, unauthorized Head, unauthorized phase principal, forged consent, stale source, failed evidence, omitted internal audit, post-expiry behavior, revoke, integrity corruption, cross-mission separation, allowed-team/action bounds, and no provider-specific imports in mission engine. All outcomes must distinguish simulated fixture results from live provider-authorized mission proof.
