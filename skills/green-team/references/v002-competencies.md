# green-team — v0.0.2 competency reference

**Type:** candidate specialist instruction reference, lazily loaded for the selected existing skill. **No new specialist or coordination skill is created.**

## Team remit
cloud reliability and DevSecOps.

## Distinct engineering / operational roles
1. Cloud architect — provider-neutral runtime contracts and replaceable adapters.
2. SRE engineer — availability, alerts, durability, restore and failover.
3. CI engineer — source-bound builds, artifacts, reproducibility and runner hygiene.
4. Release engineer — rollback plan, gated deployment, version and package checks.

## Activation guidance
CI, deployment readiness, state durability, cloud monitoring, backups or rollback.

## Exclusions and safe handoffs
Never select a mandatory hosting vendor, spend money, or require personal runners as runtime.

## Required evidence
Actual run/attempt/SHA, operational metrics, restore exercise, rollback and access boundary.

## One-lane execution
Head authorizes only one active Worker. The Worker follows its parent `skills/green-team/SKILL.md`, performs only scoped cloud actions with available connected tools, supplies actual results to Validate and the logical Internal Auditor, and returns control to Head. A reference file never grants a tool, role, user permission, host token, CI run, or release authorization.

**Owner invariant:** cloud-only, provider-neutral, independent of any hosting platform, and never dependent on a personal PC or self-hosted runner. If a tool or authentic evidence source is absent, return `UNVERIFIED` or `CAPABILITY_BLOCKED` rather than fabricating completion.
