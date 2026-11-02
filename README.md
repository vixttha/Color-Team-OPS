# RED TEAM AGENT

**Permanent GitHub home for the Red Team working thread in Color-Team-OPS.**

- **Display name:** RED TEAM AGENT
- **Home branch:** `team/red-team-agent`
- **Repository:** `vixttha/Color-Team-OPS` (private)
- **Scope:** long-lived, owner-directed *Red Team assessment workspace*, not another Color Team OPS product skill or coordinator.
- **Product mission:** `CTO-V002-SINGLE-THREAD` remains owned by the existing Head and integration branch.
- **This workspace mission:** `RED-HQ-001` (rolling security research, risk tracking and authorized retests).
- **Release control:** NO v0.0.2 release, merge, production write, plugin update or privilege change without fresh owner approval.

## How to resume the Red Team after any break

1. Read `identity/RED-TEAM-AGENT.md` and `policy/WORKING-CONTRACT.md`.
2. Read `state/CURRENT.json`, `state/HANDOFF.md`, `state/WORK-QUEUE.json` and `state/FINDINGS.json`.
3. Re-check live GitHub branch heads, Issue #8, applicable project constitution and actual tool access; do not trust stored SHAs as current.
4. Select **one** justified, bounded work item. Preserve the HEAD → Worker → Validate → logical Internal Auditor → HEAD review loop.
5. Save source-bound evidence and any findings to THIS home branch; update the work queue and handoff. Use optimistic ref/CAS checks to avoid overwriting another session.
6. If handoff to Development HQ is useful, communicate via Issue #8 within current authority; do not edit the live integration branch without separate explicit approval.

## Contents

| Path | Purpose |
| --- | --- |
| `identity/` | Agent identity, capabilities, boundaries and continuity |
| `policy/` | Authority, threat modeling, evidence and security-review standards |
| `state/` | Current mission pointer, queue, findings and decisions |
| `audits/` | Immutable date/source-specific review reports |
| `worklog/` | One bounded record per work session |
| `playbooks/` | Non-disruptive, permission-gated adversarial test plans |
| `templates/` | Finding and session report formats |
| `roadmap/` | Multi-cycle work plan; scheduled work is NOT implied |

This branch is a durable **repository record**, not a continuously running autonomous agent. Work happens when the user invokes an appropriate supported session or a separately configured authorized automation runs. GitHub files are never permission grants or proof of tests.
