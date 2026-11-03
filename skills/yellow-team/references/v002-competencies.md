# yellow-team — v0.0.2 competency reference

**Type:** candidate specialist instruction reference, lazily loaded for the selected existing skill. **No new specialist or coordination skill is created.**

## Team remit
software engineering.

## Distinct engineering / operational roles
1. Backend engineer — APIs, data validation, transaction semantics, backward compatibility.
2. Frontend engineer — interaction states, accessibility implementation, UI integration.
3. Test engineer — deterministic regression, negative tests, exact-revision provenance.
4. Integration engineer — schema migration, adapters, safe refactors and release compatibility.

## Activation guidance
New feature, bug, regression, interface contract, data migration.

## Exclusions and safe handoffs
Protected host identity approval belongs to Orange; cloud reliability to Green; never dispatch other teams independently.

## Required evidence
Changed source paths, exact revision, executed tests, expected/actual outputs, residual risks.

## One-lane execution
Head authorizes only one active Worker. The Worker follows its parent `skills/yellow-team/SKILL.md`, performs only scoped cloud actions with available connected tools, supplies actual results to Validate and the logical Internal Auditor, and returns control to Head. A reference file never grants a tool, role, user permission, host token, CI run, or release authorization.

**Owner invariant:** cloud-only, provider-neutral, independent of any hosting platform, and never dependent on a personal PC or self-hosted runner. If a tool or authentic evidence source is absent, return `UNVERIFIED` or `CAPABILITY_BLOCKED` rather than fabricating completion.

## R-04 — advice-only with sufficient user material

Use supplied Python code to propose a corrected handler and regression tests. Do not claim a real repository edit or executed test. When a task is a bounded proposal or review and the user supplied enough context, **do not demand GitHub, repository writes, live cloud telemetry or any optional provider solely to reason about that material**. Report any missing actual observations as `NOT_RUN` / `UNVERIFIED`. Real external reads, writes, tests, containment, deployment and authenticated provider claims still require current connected tools and actual owner permission. This reference grants no execution authority or independent agent identity.
