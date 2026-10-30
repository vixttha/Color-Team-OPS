# Verified taxonomy audit — 2026-10-30

Status: RESEARCH ONLY. No change to released v0.0.1 skills, v0.0.2 proposals, Head authority, or installed plugin.

## Scope and method
Compared the user's 634-line uploaded "Deep Audit: What Each Team Does in a Nine-Team Color-Team Company" against (1) live private GitHub release/v0.0.1-cloud-only skill sources and constitution, (2) v0.0.2 design/04-NINE-TEAM-SPECIALIZATIONS and single-lane architecture, and (3) external primary standards and competition documentation. Source audit identifies **verified source statements**, **plausible organizational mappings**, and **unapproved project changes**; it does not treat a possible job title as a standardized team assignment.

## Findings by certainty
**Verified (strong primary support):**
- April Wright, Black Hat USA 2017: Yellow = developers; Orange = Red + Yellow; Green = Blue + Yellow. Purple bridges Red + Blue. The six colors function as a conceptual collaboration model, not a staffing standard.
- NIST NICE: work roles describe sets of tasks, knowledge and skills and are NOT synonyms for a job or job title; one job may span multiple work roles.
- NIST White Team glossary: neutral scope, rules of engagement, safety and adjudication during Red/Blue exercises.
- NIST "Building a Competition": Black = technical/administrative support; Gold/White = neutral exercise organization; Orange/Green may mean *end users* in exercises. This is a critical counterexample to treating colors as universal.
- NCCDC 2026 rules: Black = competition operations, Gold = support/communications, White = judges/compliance, Orange = user simulation. Gold is explicitly **not** generally 'corporate executive leadership' in that source.
- OWASP DevSecOps and NIST SSDF: secure coding, testable pipelines, provenance and secure deployment/operations are useful engineering practices. They do not assign specific color-team job titles.
- MITRE ATT&CK: evidence-led documentation of real-world adversary behavior; suitable for a threat-intelligence specialty.
**Reasonable project adaptation, not industry fact:** 'Black' as production platform engineering and 'Gold' as executive direction; expanding 'White' from exercise neutrality to all GRC; mapping 20+ commercial job titles per color.
**Not established:** a universal nine-color company standard, a definitive/exhaustive list of jobs per color, or the proposition that nine AI specialists automatically outperform fewer.

## Critical contradictions with actual repository
| Dimension | Existing released v0.0.1 / draft v0.0.2 | Uploaded proposed company model | Assessment |
| --- | --- | --- | --- |
| Yellow | Functional software engineering | Build | Compatible |
| Red | Authorized adversarial testing | Attack | Compatible |
| Blue | Defense / detection / incident response | Defend | Compatible |
| Orange | Security-aware app engineering | Product/AppSec | Compatible with slight scope shifts |
| Green | Cloud ops, secure deployment, observability, reliability, DevSecOps | Defensive security engineering/DevSecOps | Substantial emphasis shift; keep existing deployment remit |
| Purple | Offensive-defensive correlation/retesting | Security validation | Compatible |
| White | Neutral exercise rules/authority adjudication; NOT generic code auditor | Broad governance/risk/compliance/assurance, including Internal Auditor | Scope expansion conflicts with separation-of-duties contract |
| Black | Dated, source-grounded threat intelligence | Platform/infrastructure operations | Direct reassignment of a released skill |
| Ninth | Gray Cell: synthetic user mistakes/behavior | Gold executive direction | Removes a released skill; risks duplicating Head |
| Coordinator | Head (Mission Control + OPS Director), verification gate, separate internal audit phase | Gold directs organization | Gold-as-worker risks duplicate mission authority |

Sources checked in repo: `skills/{black-team,gray-cell,green-team,white-team,ops-director}/SKILL.md` on release/v0.0.1-cloud-only; `docs/CONSTITUTION.md` same ref; `docs/02-SINGLE-LANE-ARCHITECTURE.md` and `docs/04-NINE-TEAM-SPECIALIZATIONS.md` on design/v0.0.2-team-contracts-single-lane.

## Disposition
Preserve existing nine specialists, including **Black threat intelligence** and **Gray Cell**. Treat Gold as executive/program competencies of **Head**, Black infrastructure role candidates as **Green cloud/platform operations** with scoped Yellow support, and broadened GRC as limited **White analysis** or Head-owned governance decisions rather than granting White new policy authority. These are **recommendations**, not approval to change contracts. A new dedicated team / renaming would need an explicit owner architectural decision, compatibility/migration analysis and tests.

## Project invariant audit
Do not change cloud-only execution, optional runner constraint, read/advise defaults, no self-granting permissions, no auto merge/deploy, evidence at exact commit, separation of internal auditor from White/Purple, and one active writer with Head-mediated dispatch. Draft v0.0.2 enforcement of cloud-exclusive writing is **not proven** merely by instructions; do not claim it.

## Confidence / limitations
High confidence: confirmed wording in Black Hat abstract, NIST, NCCDC, OWASP, MITRE, project skills. Medium confidence: practical role assignment suggestions; job titles vary by employer. Not tested: performance or token-cost superiority of either taxonomy, safety of future schema migrations, live execution of every team. User-provided uploaded research is a secondary *input* and cannot independently validate itself. The research assistant's 404 GitHub claim is superseded by authenticated direct reads.

See [role inventory](02-ROLE-AND-SKILL-INVENTORY.md), [solo-developer playbook](03-SOLO-DEV-MISSIONS.md), [gap assessment](04-DECISIONS-AND-GAPS.md), and [sources](05-VERIFIED-SOURCES.md).
