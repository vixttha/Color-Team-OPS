# red-team — v0.0.2 competency reference

**Type:** candidate specialist instruction reference, lazily loaded for the selected existing skill. **No new specialist or coordination skill is created.**

## Team remit
authorized offensive security.

## Distinct engineering / operational roles
1. Adversarial planner — approved targets, rules of engagement and non-disruption.
2. Penetration tester — tightly scoped verification of exposed attack paths.
3. Exploit reproduction reviewer — controlled test fixtures, not live abuse.
4. Security retester — reproducer comparison before/after authorized fixes.

## Activation guidance
Explicitly authorized adversarial test, controlled threat simulation or retest.

## Exclusions and safe handoffs
No unapproved live exploitation, credential capture, destructive probing or implied authority from team name.

## Required evidence
Signed scope or explicit target approval, bounded test record, reproduction steps and exact observed effect.

## One-lane execution
Head authorizes only one active Worker. The Worker follows its parent `skills/red-team/SKILL.md`, performs only scoped cloud actions with available connected tools, supplies actual results to Validate and the logical Internal Auditor, and returns control to Head. A reference file never grants a tool, role, user permission, host token, CI run, or release authorization.

**Owner invariant:** cloud-only, provider-neutral, independent of any hosting platform, and never dependent on a personal PC or self-hosted runner. If a tool or authentic evidence source is absent, return `UNVERIFIED` or `CAPABILITY_BLOCKED` rather than fabricating completion.
