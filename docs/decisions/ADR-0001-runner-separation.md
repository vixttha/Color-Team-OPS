# ADR-0001 — Cloud-only runtime and separated runner CI

**Status:** ACCEPTED — locked project decision  
**Date:** 2026-10-29  
**First version:** v0.0.1  
**Owner:** repository owner

## Context

Color Team OPS must be a browser-first, cloud-only plugin. The repository has optional owner-managed Windows and Linux GitHub runners, but their existence must never create a product dependency. GitHub documents risks of running untrusted code on persistent self-hosted runners.

## Decision

1. The mandatory repository CI baseline uses GitHub-hosted Ubuntu and Windows, not self-hosted runners.
2. Owner-runner development tests, independent audits, plugin validation and release tests are permitted only as optional supplements.
3. Supplemental runner execution requires manual approval and trusted main source. No pull-request-triggered self-hosted jobs.
4. Personal runners must never run the installed plugin, power autonomous cloud execution, act as the product database, or become a required/fallback check.
5. README, CHANGELOG and evidence must be updated with every version. Approval is tied to an exact commit SHA and independent review.
6. Missing optional runner evidence cannot invalidate a successful mandatory cloud CI baseline.

## Rejected alternatives

Mandatory personal runner tests, automatic self-hosted PR execution, local-worker fallback, and CI-free releases.

## Consequences

GitHub-hosted checks can consume allotted/billed private-repo minutes; optional personal runner availability is irrelevant to product operation. Manual workflow_dispatch cannot run until its definition is on the default branch. Record compatibility and actual test evidence rather than assuming operation.

## Links

[Runner policy](../design/RUNNER-POLICY.md) · [Release process](../RELEASE-PROCESS.md) · [Constitution](../CONSTITUTION.md)

Preserve this historical record. Supersede in a new ADR only with explicit owner authorization.
