# BLUE TEAM AGENT — long-horizon work program

**Time model:** multi-week planning **when actively invoked**; no continuous autonomous execution, background scans or promised future deliveries. Duration is flexible. Each week can be a separate session or several bounded tasks. Only actual session records count as completed work.

| Work cycle | Defensive focus | Concrete exit criteria |
| --- | --- | --- |
| Week 1 | Establish Blue identity, immutable evidence rules, risk queue | GitHub home and source-bound baseline read back; release boundary explicit |
| Week 2 | Source authenticity and web skill package integrity | BT-001 patch candidate on Blue branch; negative tests tied to exact revision; Head review |
| Week 3 | Evaluation ingestion hardening | BT-002/BT-003 malformed-data and cross-case replay negative tests; no fake host scores |
| Week 4 | Runner / branch exposure and least privilege | BT-004 current branch protection and actor scope verified via authoritative API; recommendations without unauthorized changes |
| Week 5 | Detection signal taxonomy | Versioned event IDs, deny/allow decisions, revocation failures, unexpected Head/worker activity, CI anomalies with source and confidence |
| Week 6 | Blue specialist evaluation fixture quality | BT-007 realistic synthetic timelines and expected missing-evidence behavior, independent label readiness |
| Week 7 | Cloud incident triage and response playbooks | Safe containment approval ladder, preservation, alert fatigue tests, no invented successful mitigation |
| Week 8 | Source drift, replay and trust-boundary review | Explicit cross-team handoff with Orange/Purple/Green; separate review of source vs installed plugin |
| Week 9 | Browser-host defensive negative acceptance | BT-005 only if an authorized v0.0.2 test host/preview actually exists; otherwise stay BLOCKED |
| Week 10 | Independent specialist trial and false-positive review | BT-006 only when independent oracles and real model evidence exist |
| Week 11 | Whole-branch evidence inventory refresh | All branches re-enumerated; exact-head regression evidence contrasted with historical results |
| Week 12 | Blue Team long-term posture review | Open finding counts, fixed-at-SHA outcomes, exceptions, owner approval gates and next cycle backlog |

## Checkpoint discipline

At each actual cycle end, commit a new `logs/` entry and update `HANDOFF.md`, `STATE.json`, `BACKLOG.md` and `FINDINGS.json` as warranted. Every recorded completion must pass **Head → Blue → Validate → logical Internal Auditor → Head**. Missing host grants or reviewers remain a blocker rather than a reason to invent substitute evidence. The owner can interrupt, reprioritize, or terminate this program at any time.

A weekly schedule table is **planning**, not an automation. For an unattended weekly task, obtain separate owner authorization and register the specific automation ID, cadence and allowed read-only scope in `STATE.json`; never assume one exists.
