# blue-team — v0.0.2 competency reference

**Type:** candidate specialist instruction reference, lazily loaded for the selected existing skill. **No new specialist or coordination skill is created.**

## Team remit
defensive detection and incident response.

## Distinct engineering / operational roles
1. Detection engineer — useful alerts, false positives, source identifiers and event coverage.
2. SOC analyst — triage, severity, signal correlation and containment advice.
3. Incident responder — timeline preservation, scoped recovery and audit trails.
4. Defensive engineer — misconfiguration hardening, logging, recovery exercises.

## Activation guidance
Security event visibility, alert gap, incident, suspicious action or defensive hardening.

## Exclusions and safe handoffs
No invented live telemetry, forced containment, or claims of closed incidents without evidence.

## Required evidence
Dated provider log, alert rule and test, incident timeline, defensive result and confidence.

## One-lane execution
Head authorizes only one active Worker. The Worker follows its parent `skills/blue-team/SKILL.md`, performs only scoped cloud actions with available connected tools, supplies actual results to Validate and the logical Internal Auditor, and returns control to Head. A reference file never grants a tool, role, user permission, host token, CI run, or release authorization.

**Owner invariant:** cloud-only, provider-neutral, independent of any hosting platform, and never dependent on a personal PC or self-hosted runner. If a tool or authentic evidence source is absent, return `UNVERIFIED` or `CAPABILITY_BLOCKED` rather than fabricating completion.
