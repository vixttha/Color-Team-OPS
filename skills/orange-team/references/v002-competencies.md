# orange-team — v0.0.2 competency reference

**Type:** candidate specialist instruction reference, lazily loaded for the selected existing skill. **No new specialist or coordination skill is created.**

## Team remit
application security engineering.

## Distinct engineering / operational roles
1. Identity and consent reviewer — issuer/audience/scope, expiry, replay and revocation.
2. AppSec code reviewer — injection, access control, data-flow and secret handling.
3. Secure API engineer — authorization at mutation boundaries, tenancy, input normalization.
4. Security test engineer — adversarial unit regressions with read-only/sandboxed fixtures.

## Activation guidance
Auth, consent, forged evidence, risk of privilege escalation, secret exposure.

## Exclusions and safe handoffs
Do not impersonate a real trusted host, launch external attacks or act as the universal release auditor.

## Required evidence
Threat-to-code map, negative test result, exact affected SHA, severity, verified remediation.

## One-lane execution
Head authorizes only one active Worker. The Worker follows its parent `skills/orange-team/SKILL.md`, performs only scoped cloud actions with available connected tools, supplies actual results to Validate and the logical Internal Auditor, and returns control to Head. A reference file never grants a tool, role, user permission, host token, CI run, or release authorization.

**Owner invariant:** cloud-only, provider-neutral, independent of any hosting platform, and never dependent on a personal PC or self-hosted runner. If a tool or authentic evidence source is absent, return `UNVERIFIED` or `CAPABILITY_BLOCKED` rather than fabricating completion.

## R-04 — advice-only with sufficient user material

Review supplied code for authorization, input-validation and tenant flaws; propose security repairs without claiming a live exploit. When a task is a bounded proposal or review and the user supplied enough context, **do not demand GitHub, repository writes, live cloud telemetry or any optional provider solely to reason about that material**. Report any missing actual observations as `NOT_RUN` / `UNVERIFIED`. Real external reads, writes, tests, containment, deployment and authenticated provider claims still require current connected tools and actual owner permission. This reference grants no execution authority or independent agent identity.
