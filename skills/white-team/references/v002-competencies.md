# white-team — v0.0.2 competency reference

**Type:** candidate specialist instruction reference, lazily loaded for the selected existing skill. **No new specialist or coordination skill is created.**

## Team remit
exercise governance and adjudication.

## Distinct engineering / operational roles
1. Rules-of-engagement officer — scope, permissions and safe stop conditions.
2. Neutral exercise controller — valid scenario boundaries and time windows.
3. Adjudicator — evaluate disputed observations against frozen exercise rules.
4. Safety officer — external impact review and escalation controls.

## Activation guidance
Explicit exercise scope conflict, neutral adjudication, ambiguous authorization boundary.

## Exclusions and safe handoffs
Not automatically the Internal Auditor, release signer or authorization issuer.

## Required evidence
Approved rule reference, disputed event chronology, neutral decision rationale and escalation.

## One-lane execution
Head authorizes only one active Worker. The Worker follows its parent `skills/white-team/SKILL.md`, performs only scoped cloud actions with available connected tools, supplies actual results to Validate and the logical Internal Auditor, and returns control to Head. A reference file never grants a tool, role, user permission, host token, CI run, or release authorization.

**Owner invariant:** cloud-only, provider-neutral, independent of any hosting platform, and never dependent on a personal PC or self-hosted runner. If a tool or authentic evidence source is absent, return `UNVERIFIED` or `CAPABILITY_BLOCKED` rather than fabricating completion.

## R-04 — advice-only with sufficient user material

Draft rules of engagement or governance advice from supplied scope; do not invent a signer, owner consent, or independent adjudicator. When a task is a bounded proposal or review and the user supplied enough context, **do not demand GitHub, repository writes, live cloud telemetry or any optional provider solely to reason about that material**. Report any missing actual observations as `NOT_RUN` / `UNVERIFIED`. Real external reads, writes, tests, containment, deployment and authenticated provider claims still require current connected tools and actual owner permission. This reference grants no execution authority or independent agent identity.
