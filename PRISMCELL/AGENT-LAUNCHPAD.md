# PrismCell nine-team launchpad — v0.0.1

One owner-invoked lane: **Head → one specialist Worker → Validate → logical Internal Auditor → Head**. Other specialists receive GitHub INCALL comments; they do not become independent auto-running agents just because their branches exist.

| Specialist | Role | GitHub home branch | INCALL issue |
|---|---|---|---|
| Yellow | Engineering, repairs and executable tests | `agent/YELLOW-TEAM-AGENT` | #9 |
| Orange | Application and agent security | `agent/ORANGE-TEAM-AGENT` | #10 |
| Green | Cloud/reproducibility/CI evidence | `agent/GREEN-TEAM-AGENT` | #11 |
| Red | Bounded offensive/security negative tests | `team/red-team-agent` | #12 |
| Blue | Detection, defensive review and incident readiness | `agents/blue-team-agent` | #13 |
| Purple | Cross-team evidence correlation within its own workcell | `agent/PURPLE-TEAM-AGENT` | #14 |
| White | Governance, scope and permission policy | `agent/WHITE-TEAM-AGENT` | #15 |
| Black | Threat intelligence and advisories | `agent/BLACK-TEAM-AGENT` | #16 |
| Gray Cell | Usability and human factors | `agent/GRAY-CELL-AGENT` | #17 |

## How to start

In this ChatGPT project say: **“Activate the [COLOR] TEAM AGENT from its PrismCell branch, inspect current queue and INCALL, and execute the highest-priority authorized bounded task in its own branch, with evidence and internal audit.”** Substitute the intended team. For a cross-team mission say: **“HEAD coordinate the specialist handoffs one at a time, preserving each team's branch and INCALL evidence.”**

### Dispatch control

The nine agents are independent **workspaces**, not nine separate authenticated processes and not a new Color-Team-OPS coordinator. Purple workcell is NOT Purple Review HQ. Development HQ retains product integration; Color-Team-OPS plugin remains separately governed. No Gold team or new coordinator.

## What “running” means today

The real GitHub branch and issue were checked, the current team has a recorded activation checkpoint, and it can be invoked to perform work immediately. No nine-way parallel execution, continuous listener or unattended code execution is installed. `PRISMCELL/STARTUP.md` is the entry contract. The team's `TEAM-WORKBENCH/OPERATIONS-CHECKPOINT.json` and `STATE.json` are its persistent current startup record.
