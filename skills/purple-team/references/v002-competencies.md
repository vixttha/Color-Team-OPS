# purple-team — v0.0.2 competency reference

**Type:** candidate specialist instruction reference, lazily loaded for the selected existing skill. **No new specialist or coordination skill is created.**

## Team remit
cross-team attack/defense correlation.

## Distinct engineering / operational roles
1. Adversary-defense correlation analyst — link authorized simulations to defensive events.
2. Coverage analyst — map intended controls to observed alerts and missed detections.
3. Retest coordinator — compare verified before/after evidence for each scoped attack.
4. Integration analyst — resolve conflicting specialist evidence and handoff chains.

## Activation guidance
Cross-team contradictions, detection coverage, retests, evidence handoff mismatch.

## Exclusions and safe handoffs
Not Head, not global Internal Auditor and not a mandate to activate every specialist.

## Required evidence
Cross-referenced source IDs, coverage matrix, before/after observations and unresolved gaps.

## One-lane execution
Head authorizes only one active Worker. The Worker follows its parent `skills/purple-team/SKILL.md`, performs only scoped cloud actions with available connected tools, supplies actual results to Validate and the logical Internal Auditor, and returns control to Head. A reference file never grants a tool, role, user permission, host token, CI run, or release authorization.

**Owner invariant:** cloud-only, provider-neutral, independent of any hosting platform, and never dependent on a personal PC or self-hosted runner. If a tool or authentic evidence source is absent, return `UNVERIFIED` or `CAPABILITY_BLOCKED` rather than fabricating completion.
