# IDEA-000037 — One-action mission pipeline planner and adaptive team launcher

**Status:** CAPTURED IDEA ONLY · implementation NOT_PLANNED · testing UNTESTED · not included in any release.
**Recorded:** 2026-10-30. **Origin:** owner asked Purple Team to preserve and elaborate the experience of having an M1–M5 plan, tasks, specialist ownership and a worker handoff, then being able to ask the system to carry it out.
**Catalog record:** [IDEA-000037](../ideas/records/IDEA-000037.json).
**Scope protection:** This is **not** a new v0.0.2 acceptance gate or permission to interrupt its active M5 mission. The optional Purple Ideas & Features Library remains independent of Color-Team-OPS operational runtime. No new FEAT record or release membership is implied.

## 1. The product experience

A user describes their goal in ordinary language. Color-Team-OPS turns that request into a coherent, inspectable mission plan—before anyone writes to a repo or calls a privileged tool.

The user sees **one project pipeline** with milestones, ordered tasks, dependencies, suggested color teams, role-specific acceptance checks and uncertainties. They can edit scope, remove steps and adjust preferences. A prominent action, tentatively **“Work on this”**, starts the **already-authorized** plan within the supported ChatGPT host, without requiring a manually assembled meta prompt.

The system then works through each task by **Head → one selected Worker → Validate → Internal Auditor → Head**. Head chooses the next team based on *current findings*—the plan's initial staff assignments are recommendations, not a rigid queue or irrevocable permission. Normal, in-scope handoffs require no additional user prompt. Actions outside the user's existing grant need a new explicit authorization; missing capabilities cause an honest stop.

This is a proposed interaction pattern, **not** a claim that ChatGPT currently exposes such a button, supplies unattended persistent execution, can authenticate multiple separate role principals, or can run all Python reference modules through an installed skill.

## 2. Proposed journey

1. **Describe:** “Build a private tool with authentication, tests, accessibility and a production-ready release package.” Optional repository, budget, deadline, privacy and deliverable constraints can be recognized without a long questionnaire.
2. **Head scopes:** Mission Control + OPS Director identify objective, environment, permitted tools, limits, expected deliverables and unknowns. Head refuses to invent provider access, credentials, security permission or a deployment target.
3. **Plan:** Generate one versioned milestone/task graph. Every task has a concrete deliverable, dependencies, a proposed eligible specialist (and reason), required tools, evidence and gate criteria, plus honest unresolved questions and blockers.
4. **Preview/edit:** User sees the pipeline, team routing and risk/permission summary. User may revise tasks, choose which optional work to include, and authorize a bounded mission scope.
5. **Launch:** A supported host action called **“Work on this”** (name provisional) records the accepted plan revision, authorized scope, budgets and exact repo/source context, then hands control to Head. It must never be interpreted as global permission to publish, pay, provision, change privileges or conduct offensive tests.
6. **Execute:** Head dispatches one authorized Worker at a time. Yellow may implement, Orange review sensitive auth, Yellow repair a finding, Green verify CI, etc., only when task findings justify each dispatch.
7. **Verify:** For every task, actual evidence is checked in Validate, independently challenged in a distinct logical Internal Auditor stage, and adjudicated by Head. A passing unit test alone cannot certify hosted permission, security or production release.
8. **Adapt:** If an audit uncovers a new needed task, Head proposes/records a bounded replanning decision within existing consent. Changes that expand authorization require owner approval. Already validated work is invalidated when material source changes warrant rechecks.
9. **Report:** A single mission view shows completed, active, blocked and remaining work, evidence references, artifact links and reasons for new specialist assignments. Claim completion only for genuinely accepted requirements.

## 3. A proposed compact plan object (conceptual, not a committed API)

| Field | Meaning |
| --- | --- |
| `mission_id`, `plan_revision`, `source_sha` | Versioned mission identity and source-bound plan; no stale approvals |
| `goal`, `scope`, `non_goals` | What the user asked to build, what is allowed and what is excluded |
| `authorized_actions`, `available_tools`, `budget` | Actual grant/host limits; plan data cannot mint authorization |
| `milestones[]` | User-readable work stages, ordered by dependency |
| `tasks[]` | Stable task IDs; purpose, artifact, dependencies and acceptance criteria |
| `candidate_team`, `capability_id`, `routing_reason` | Suggested specialist and why; final dispatch remains Head-owned |
| `gate_results` | Actual Validate, logical Internal Auditor and Head decisions |
| `blockers[]`, `revisions[]`, `receipts[]` | Stop reasons, approved replans and independent tool/source evidence |
| `release_status` | Explicit external owner/release decision; never inferred from an idea or feature JSON |

The plan preview may be a read-only graph/table with one authorized launch control; production structure, editing affordances and host APIs need discovery and actual testing before selection.

## 4. Team responsibility model

**Coordinators:** Mission Control frames scope; OPS Director plans/chooses the next qualified color; Verification Gate manages Validate and distinct logical Internal Auditor checks. Exactly **three** coordination skills remain.

**Specialists:** Yellow codes; Orange handles AppSec; Green handles cloud/CI/operations; Red conducts scoped authorized adversarial tests; Blue handles detection/response; Purple correlates cross-team findings; White handles exercise governance; Black researches real threats; Gray Cell tests usability/human error.

All **nine** are eligible, not all mandatory. There is exactly **one active specialist** at a time. A team's recommendation is not self-dispatch. Returning to a team for a different task or bounded repair is allowed when grants and budgets permit. The same physical/model principal playing multiple logical roles is **not** independent cryptographic attestation.

## 5. Distinction from existing ideas

- **IDEA-000001 / 000009:** Which team should work next? This idea adds **user-facing automatic pipeline creation, editable staffed task planning and the “Work on this” start action**.
- **IDEA-000002 / 000006:** Directory and handoffs are dependencies, not replacements for a mission-wide planner.
- **IDEA-000017 / 000019:** One-worker gates and owner release decisions constrain launched execution.
- **IDEA-000034:** Playbooks are suggested starter patterns; they must never override context-dependent routing.
- **Purple Ideas & Features Library:** Could inform planning *when relevant and available*, but must not be required to launch or complete a normal mission.

No new 13th coordinator, no new color, no provider or hosting-platform lock, no requirement to run the owner's personal PC as a runtime, and no need to launch nine workers in parallel.

## 6. Example plan (illustrative only, not live execution)

| Order | Task | Head's initial candidate | Validation |
| --- | --- | --- | --- |
| 1 | Implement a permissioned API | Yellow | Functional tests and source diff |
| 2 | Review the authentication boundary | Orange | Authorization misuse tests |
| 3 | Repair issues found in review | Yellow **if needed** | Regression + security retest |
| 4 | Verify cloud CI and recovery | Green **if in scope** | Real runner/provider evidence |
| 5 | Exercise user error paths | Gray Cell **if relevant** | Usability evidence |
| 6 | Assess release readiness | Head + bounded specialists | Full gates + external approval |

Head can replan, omit optional specialists or block unsupported steps. The user need not provide a second long prompt for normal authorized handoffs.

## 7. Critical risks and mitigations

| Risk | Mitigation / acceptance condition |
| --- | --- |
| Fabricated task graph or unnecessary team activations | User-readable scope; evidence-based conditional routing; benchmark unnecessary and missed assignments |
| “One click” mistaken for unrestricted permission | Explicit authorized scope before launch; privileged/paid/external actions need separate grant |
| Tool availability and host-capability mismatch | Probe supported interfaces first; abstain/block truthfully; do not claim persistent background operation |
| Endless replan, repair and expense | Stable task IDs, bounded handoffs/retries/budgets, no-progress detection and human-visible stop |
| False PASS from Worker self-report | Actual tool/source reread; separate recorded Validate and Internal Auditor; Head decision |
| Stale source and concurrent writes | Revision pinning, invalidate dependent evidence after edits, host-level locking when promised; no claim of global lock from a prompt |
| UI overload | Progressive disclosure: goal, pipeline, active team, blockers, evidence; detailed graph only when needed |
| Optional library becoming an implicit dependency | Tests show normal missions work with library absent; historical IDEA/FEAT records never grant permissions |

## 8. Potential delivery phases (not v0.0.2 release commitments)

**Research/UX prototype:** Explore a one-request plan preview, user editing and draft “Work on this” affordance. Distinguish UI sketch from working action.

**Plan builder:** Versioned tasks/dependencies, capability-aware team proposals, acceptance/evidence map, explicit scope and approval envelope.

**Supported-host launcher:** Integrate real authorized action with existing Head; observe one-prompt sequential task execution, not merely a prompt that claims switches.

**Adaptive execution and observability:** Bounded replanning and actual status/evidence dashboard, safe stops, resume semantics only where supported.

**Independent evaluation:** Compare planner with manually authored plans: task coverage, correct/extra teams, avoided interruptions, execution correctness, rollback/safety and total cost.

No phase is implicitly approved for current v0.0.2 implementation. Separate feature proposal and release planning must follow an explicit decision.

## 9. Minimum independent acceptance scenarios for future implementation

1. One natural-language goal yields a coherent editable pipeline with clear deliverables and no fabricated authority.
2. One user-authorized start launches the accepted plan through a *verified* supported host action; an unsupported host reports no launch capability.
3. A clean task switches Yellow → Orange → Yellow only if a real finding requires return; every assignment gets Validate/Audit/Head.
4. Correctly skips irrelevant teams and demonstrates safe STOP/ABSTAIN when no task should run.
5. Rejects forged receipts, stale source, wrong permissions, simultaneous workers, unbounded loops and unauthorized Red/offensive work.
6. A new privileged deployment or publication stops for explicit user approval; earlier “Work on this” consent is not treated as blanket release authority.
7. The mission can function when `ideas/`, `features/` and `portable/` are absent.
8. Native and supported-host observations are correctly labeled, reproducible and independently challenged; measured gains versus manual planning are reported without fictional percentages.

## 10. Idea decision ledger

- **User enthusiasm/request:** Explicitly wants further elaboration and an idea recorded because the plan → team assignment → “work on this” flow feels compelling.
- **Recorded disposition:** `captured`. This protects the idea without pretending the owner approved a finalized feature implementation, architecture, schedule or release.
- **Implementation:** `not_planned`; **Testing:** `untested`; **Release inclusion:** none.
- **Next design decision, when requested:** Explore the desired plan preview and launch experience and compare platform-native ChatGPT capabilities with an optional external cloud host, preserving privacy, permission boundaries and platform independence.

**References:** [v0.0.2 full release plan](https://github.com/vixttha/Color-Team-OPS/blob/planning/v0.0.2-complete-release-pipeline-2026-10-30/docs/V002-FULL-RELEASE-PIPELINE-36-FEATURE-TRACEABILITY.md) and [master development issue #8](https://github.com/vixttha/Color-Team-OPS/issues/8). Those show the existing manual workflow; they do **not** establish that the proposed one-action launcher has been built.
