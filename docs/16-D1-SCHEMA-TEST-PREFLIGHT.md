# D1 — Prototype gate review (pre-execution)

**Status:** The reference schemas and source tests exist in this *isolated design branch*. The attached suite validates structural JSON Schema invariants **only when actually run with Python and jsonschema**. Tests written ≠ tests passed; do not treat them as authenticated user actions, live host trials or functional backend assurance.

## Before native test execution
- Seven Draft 2020-12 schema files under `contracts/v0.0.2/`.
- Tests for allowed/disallowed roles, exact SHA shape, no-runner law, worker can't self-approve, valid gate verdict classes, COMPLETE needing gate references, head-only-shaped dispatch, forbidden phase skips.
- Explicitly not covered: actual authenticated actor, source run/event verification, real cloud exclusivity lock, cross-record ref lookup, and all nine specialist benchmark cases.

## Important cross-record gaps
- A structurally valid Head COMPLETE can still refer to forged `v1` and `a1`: this is by design; schema cannot authenticate references.
- An attacker can type `issued_by=HEAD`: host must authenticate.
- Mission `required_teams` subset of `allowed_teams` cannot be guaranteed by JSON Schema alone and must be validated by deterministic policy.
- `source_sha` is format-only. A real provider must verify the branch and commit.
- `ENFORCED_CLOUD` string is not proof that a lease gateway exists; runtime capability attestation is required.

## Review conclusion
The contract structure **does not knowingly contradict** the approved five-stage one-lane design, the 12-skill structure, internal auditor independence limitations, or personal runner independence. No production v0.0.2 behavior is declared complete. Executable native tests and a trusted policy verifier remain distinct milestones.

## Audit follow-up: fail-closed halt and false assurance coverage
A review found that the initial strict phase-transition list did not represent a **Head-authorized emergency block from an active phase**, despite the design requiring immediate safe stops. The next candidate adds terminal BLOCKED/CAPABILITY_BLOCKED/UNVERIFIED paths **only** for Head, while still forbidding an early COMPLETE and preserving the ordinary five-phase audit route. Added targeted tests for this distinction, for non-dispatch next_team rejection, and for fake gate references that are structurally valid but unauthenticated. The original 19/19 Linux+Windows result applies only to commit `f091c68661f35799ab4d6483546d199ec09269d5`; changes require exact-SHA retesting.
