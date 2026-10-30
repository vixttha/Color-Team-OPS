# 08 — Traceability, prior design and sources

## User-direction traceability
| User intent / explicit direction | Documented implementation concept | Status |
| --- | --- | --- |
| One conversation, one lane | 02 architecture and per-mission single Worker | User direction; global lock not implemented |
| HEAD → WORKER → VALIDATE → INTERNAL AUDITOR → HEAD | 02 transitions and 05 decision matrix | User direction; future proposed enforcement |
| No mandatory independent auditor to complete ordinary mission | 01 governance distinction; 05 internal vs external approval | User direction |
| Head accountable for completion, teams for work, evidence for claims | README, 02, 05 | User direction |
| Nine strong, smart and distinct teams, not generic stencils | 03 common interface + 04 individual playbooks + 06 lab | Proposed engineering design |
| One common contract with specialty differences | 03 + 04 | Proposed |
| Every team can self-check and repair locally | 02 + 03 + 04 | Proposed bounded implementation |
| Head exclusively routes across teams | 02 + 05 + 07 | Proposed enforcement |
| Preserve 12 skills (nine workers + three coordinators) | 01 + 04 | Existing v0.0.1 identities retained |
| Keep v0.0.1 release untouched | README + 07 | Repository isolation requirement |
| Runners optional and never a runtime dependency | README + 01 + 07 | Binding constitutional law |
| Future v0.0.2 ideas, not ready release | Every document header/status | Design-only |

## Relevant existing repository sources (read and preserved conceptually)
- v0.0.1 source: `release/v0.0.1-cloud-only`, Constitution L1–L10, `docs/CONTRACT-TRUST-MODEL.md`, `docs/ARCHITECTURE.md`, schemas for mission/completion/routing, and nine `skills/*/SKILL.md`. This branch does not copy those files as deployed artifacts.
- [Issue #4 — single-lane proposal](https://github.com/vixttha/Color-Team-OPS/issues/4) and [isolated prototype document](https://github.com/vixttha/Color-Team-OPS/blob/c70ecb22b8607ebd1cac83cb85c1dfc4f2b303a0/docs/design/ISSUE-0004-SINGLE-LANE-CONTRACT.md). Prototype reported 33 passing simulated tests but **not production trust integration**; do not claim full executable prototype source is committed there.
- [v0.0.1 PR #1](https://github.com/vixttha/Color-Team-OPS/pull/1): active separate release work; untouched by this design branch.

## External reference material for later detailed specification
These are **design reading links**, not independently run tests or proof of capability:
- OpenAI agent orchestration: https://developers.openai.com/api/docs/guides/agents/orchestration
- NIST SSDF and DevSecOps practices: https://csrc.nist.gov/Projects/ssdf
- OWASP Agent Security: https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- MITRE ATT&CK knowledge base: https://attack.mitre.org/
- GitHub protected branches / review requirements: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12

## Audit terminology
Three checks by one assistant are **three audit passes, not three independent external auditors**. Audit outcomes may check document consistency but cannot establish unimplemented behavior or security claims. `docs/09-THREE-PASS-AUDIT.md` records the concrete passes performed on this branch.

## Resolved-at-design versus still-unproven
The following **engineering proposals** address previously open design topics without rewriting user decisions: [CTO-002-A](10-SINGLE-LANE-LOCKING-DECISION.md) selects optional managed SQL/fencing/gateway enforcement; [CTO-002-B](11-AUTHENTICATED-EVIDENCE-DECISION.md) selects authenticated provider observations and criterion verification; [CTO-002-C](12-SPECIALIST-PERFORMANCE-DECISION.md) selects nine role-specific benchmark suites with proposed repeated pilots. [Combined record](13-V0.0.2-DECISION-RECORD-AND-ROADMAP.md) clearly separates these ideas from v0.0.2 shipped features. Source authorities: PostgreSQL, Redis, GitHub, OWASP, OpenAI and NIST links appear in the detailed decisions. No external-source claim implies live integration or a completed evaluation.
