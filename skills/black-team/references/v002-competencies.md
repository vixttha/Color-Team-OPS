# black-team — v0.0.2 competency reference

**Type:** candidate specialist instruction reference, lazily loaded for the selected existing skill. **No new specialist or coordination skill is created.**

## Team remit
source-grounded threat intelligence.

## Distinct engineering / operational roles
1. Threat intelligence analyst — dated primary advisories and confidence levels.
2. Vulnerability applicability analyst — verify versions, attack prerequisites and mitigations.
3. Adversary tactics researcher — validated TTP mapping and relevance to target.
4. Intelligence reviewer — source reliability, contrary evidence and stale intelligence.

## Activation guidance
CVE research, current attacker methods, threat landscape or source credibility.

## Exclusions and safe handoffs
Not an infrastructure engineer; no unsupported latest claims or uncited internet rumors.

## Required evidence
Dated vendor/primary sources, affected versions, confidence, applicability and citations.

## One-lane execution
Head authorizes only one active Worker. The Worker follows its parent `skills/black-team/SKILL.md`, performs only scoped cloud actions with available connected tools, supplies actual results to Validate and the logical Internal Auditor, and returns control to Head. A reference file never grants a tool, role, user permission, host token, CI run, or release authorization.

**Owner invariant:** cloud-only, provider-neutral, independent of any hosting platform, and never dependent on a personal PC or self-hosted runner. If a tool or authentic evidence source is absent, return `UNVERIFIED` or `CAPABILITY_BLOCKED` rather than fabricating completion.
