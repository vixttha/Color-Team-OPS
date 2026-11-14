# ADR-0002 — Owner-authorized self-hosted CI for v0.0.1

**Status:** ACCEPTED by user direction — 2026-10-29
**Supersedes:** ADR-0001 sections selecting mandatory GitHub-hosted CI and requiring external independent review. ADR-0001's cloud-only product law and no-untrusted-PR execution rule remain intact.

## Binding product law

> Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate.

## Decision

1. The user explicitly selected the registered Windows and Linux GitHub self-hosted runners for **developing and verifying v0.0.1**. They are not infrastructure used by the installed plugin.
2. A dedicated workflow on `release/v0.0.1-cloud-only` is permitted to run package, policy, security and regression tests on those runners. Do not run untrusted PR/fork code. Use an exact checkout SHA, no embedded credentials, no secrets, read-only permissions and a bounded job timeout.
3. GitHub-hosted CI is **not** a mandatory requirement for v0.0.1; the previously failed provider-runner startup is a historical issue, not an unsatisfied selected release gate.
4. The assistant will conduct and report the requested review. It must disclose that this is a self-audit, not an externally independent opinion. External review is not a condition for this release.
5. v0.0.1 remains v0.0.1 until approved and installed. Do not promote a 0.0.2 version just to bypass packaging restrictions.
6. README and CHANGELOG remain updated for every version. Evidence must be tied to the exact tested source SHA and actual job output.

## Boundaries and consequences

Runner unavailability can temporarily block **developer test evidence** when those runners are chosen, but can never break the installed plugin, cloud host integrations or future autonomous cloud operations. The user may change test infrastructure in later decisions without weakening this invariant.

Reference: [Locked runner law](../design/RUNNER-POLICY.md), [Constitution](../CONSTITUTION.md), [Release process](../RELEASE-PROCESS.md).
