# Color-Team-OPS — canonical cross-thread handoff for 2026-10-30 feature discussion

> **READ THIS FIRST in any new ChatGPT/agent thread.** It is designed to make the next conversation recover the decisions, constraints, open ideas and actual evidence **without reliance on previous chat memory**. **Do not treat this research record as permission to edit v0.0.2, merge or release.** Re-read current GitHub refs before action.

## 1. Project identity and actual repo state (snapshot, not a live guarantee)
- Private repo: `vixttha/Color-Team-OPS`.
- **Existing v0.0.1** source branch: `release/v0.0.1-cloud-only`, checked at `fc77a647554cd40fb94839b3eb99e5f0ce4210a9`.
- **Active v0.0.2 engineering branch**: `design/v0.0.2-team-contracts-single-lane`, checked at `963533265c21b0c0ae05d3d85846d65630593c08` (latest then "audit(v0.0.2 D5): lock host-neutrality regression checks and record real provenance limits"). It is **not** a completed/published v0.0.2 release.
- **This non-invasive research branch**: `research/nine-team-role-audit-2026-10-30`; exact HEAD must be freshly read. This document and linked records live in `research/` on this branch. Previous research includes 01–06.
- `main` snapshot: `a28c2908da47d16dbdf7e55eb29a0c1ce9b6c7d3`.
- **Possible other active worker:** user explicitly says another worker is doing v0.0.2 work. An observed branch SHA does NOT prove that process is running or stopped. **Do not stop it automatically or write to its branch.**

## 2. User intentions, ordered by commitment level
### Approved architecture direction
The owner expressly approved: **"evolve Color-Team-OPS from a system that follows suggested team sequences into one that determines which specialist is needed, why, when, and what evidence must exist before advancing."**

### Favorably endorsed ideas (research/design interest, not blanket code/deployment authority)
- A **searchable role-and-capability registry** (nine fixed teams with multiple specialized work competencies).
- **Explicit team-to-team handoff rules** (required evidence, reason, allowed/required/optional transitions).
- **Measured specialist performance testing** (real observed outcomes, not flattering titles).
- A **routing policy engine** that ties registry + handoffs + tests together. The user likes this concept and asked whether it duplicates an existing skill.
- **Feature synergy / capability composition:** user values features that integrate to make stronger products. Record both benefits and adverse interactions.
- **Document ALL features mentioned** and make them accessible to an independent new conversation/thread.
- Owner asked if they should stop the v0.0.2 worker before implementing. **Recommendation:** generally NO abrupt stop: let current bounded mission reach a safe checkpoint, collect exact SHA + actual test/audit result, then plan integration on a separate branch or next dedicated milestone. If worker is about to change the very same routing/team contracts, ask it to **pause before overlapping edits**, not abandon or rewrite active work. Coordinate via Head and explicit approval.

### Not approved / not inferred
- No automatic merge, production deployment, paid backend, plugin publication or special tool permissions.
- No replacement of Black Threat Intelligence by Black Infrastructure; no deleting Gray for Gold; no tenth team or 13th coordination skill.
- No claim that 99% routing or 99% mission correctness has been achieved.
- No instruction to change the running worker's branch, stop workers, or rebase its work automatically.

## 3. Canonical team taxonomy (the nine current specialists)
1. Yellow — functional software engineering (frontend/backend/API/db, testing).
2. Orange — secure application engineering (authn/authz, threat modeling, secure coding).
3. Green — cloud operations, DevSecOps, observability, deployment and recovery.
4. Red — authorized adversarial testing.
5. Blue — defense/detection/incident response.
6. Purple — adversarial-defensive correlation and retesting.
7. White — neutral cyber-exercise governance, rules of engagement and adjudication (not generic internal audit).
8. Black — real-world source-grounded threat intelligence (not infrastructure in THIS product).
9. Gray Cell — synthetic human/user misuse and mistakes (not replaced by proposed Gold).

The uploaded 634-line "Deep Audit: What Each Team Does in a Nine-Team Color-Team Company" gives an *alternative* White GRC / Black Infrastructure / Gold Leadership nine-team corporate model. It is useful organizational research but **not the approved existing Color-Team-OPS architecture**. It was faithfully preserved in `research/06-ALTERNATIVE-COMPANY-MODEL.md`. NIST and competitions vary color labels; do not describe one scheme as an industry universal.

## 4. Existing three coordinating skills — do NOT add a fourth
- **Mission Control**: initial scope, user grants, host/tool inventory, spending/attempt limits, authority and stop conditions.
- **OPS Director**: existing Head-router, already selects at most one permitted next specialist based on evidence/dependencies, or finishes/blocks. This is the natural home for a *better routing policy engine*. The added value is a versioned capability registry, conditional obligations, structured decision reasons and measured accuracy. Not a replacement for OPS Director.
- **Verification Gate**: independent evidence checking by exact source revision, and the logically distinct **Internal Auditor** phase. The Internal Auditor is a workflow role, **not White or Purple**.
- **Head** = Mission Control + OPS Director as owner of decisions; cycle: **Head → one Worker → Validate → Internal Auditor → Head** for each worker. Specialist can recommend but never self-dispatch.
- Existing **D2 trusted policy verifier** is the legal/authority/provenance gate and must be distinct from new best-specialist routing logic. Do not mistake the latter for cryptographic permissions.

## 5. What exists in v0.0.2 versus new gaps
Actual checked v0.0.2 work includes D1 contracts/state, D2 policy verifier, D3 GitHub source/CI evidence adapter, D4 reference protected host-authority mechanism, and D5 account-attributed GitHub pilot. Existing D5 explicitly labels real GitHub account event observations as **PROVIDER_EVIDENCE_OBSERVED_ROLE_AUTHORITY_UNVERIFIED**, not authenticated independent model actors/user consent. CI can pass without production host authority. The design already proposes **270 unique specialist cases** (30/team) and 810 repeated runs (3 repeats/case/configuration) but these are **NOT a demonstrated 99% skill or routing score**. Keep source-SHA discipline and honest `UNVERIFIED`/`CAPABILITY_BLOCKED`.

New value requested:
- R1: searchable versioned sub-capabilities (skill ownership, triggers, exclusions, data/tools, inputs, outputs, scorecards, optional lazy-loading).
- R2: typed required/optional/forbidden conditional handoff rules with decision reasons, evidence and no fixed universal team order.
- R3: deterministic eligibility/safety filter plus context-sensitive recommendation inside OPS Director; the legal/identity gate remains under existing verifier.
- R4: dedicated routing correctness, mandatory-specialist recall, unnecessary handoffs, abstention, transition quality, specialist performance and end-to-end mission benchmarks.
- R5: baseline vs component/combined ablation study and disciplined promotion with independent holdouts/uncertainty, not blanket 99% claims.
- R6: better cross-thread continuation and exact source/version breadcrumbs.

## 6. Scope/interaction/negative-effects quick reference
| Feature | Positive | Negative | Interacts with |
| --- | --- | --- | --- |
| Registry | correct specialization, minimal context loading | wrong/stale metadata causes misroutes, token/schema bloat | OPS Director, specialty packs, evals |
| Handoffs | evidence integrity, reproducibility, clearer responsibility | overstrict/verbose transitions, slow progress | Verify Gate, existing source-SHA checks |
| Router policy | fewer missed required teams and unnecessary hops | duplication, inconsistent rules, loops and false authority | Mission Control, OPS Director, D2, registry |
| Specialist/routing evals | measured improvement, safe promotion | benchmark overfitting, false assurance, evaluation cost | all prior modules; bounded budgets |
| Risk/task classifier | appropriate route for bug vs security incident | underestimated risk or false classification | Mission Control, registry, router |
| Provider-backed evidence + distinct audit | fewer unsupported completions | can block when tools/host authority absent | D2-D5, handoffs |
| Cloud exclusivity enforced mode | stronger cross-session write gate if provisioned | financial cost, platform complexity, direct-write bypass | binding provider-neutral cloud-only design; owner approval |

**Composability is a hypothesis to prove through paired ablation tests, NOT an excuse to add every feature unconditionally.**

## 7. Revised routing design — not a fixed team sequence
Head always establishes scope and final decision. Start specialist depends on mission:
- Ordinary feature → Yellow; Orange if sensitive, Gray if UX acceptance, Green for deployment.
- Authn/authz → Orange early threat review or Yellow if security requirements already known; then appropriate implementation/review; Red only with explicit exercise permission.
- Ordinary bug → Yellow; Gray/Orange conditional.
- Vulnerability report → Orange triage (Red if authorized reproduction is needed); Black optional threat context; appropriate repair/retest.
- Detection → Blue; Red/Purple/Green conditional.
- Cloud deploy/outage → Green; Yellow if code problem, Blue if actual compromise.
- Cyber incident → Blue; Green recovery, Orange/Yellow repair, Purple if correlation.
- Threat research → Black; no other specialist by default.
- User confusion → Gray; Yellow/Orange on proven issue.
- Exercise authority → White; Head owns final authorization, White cannot grant itself or impersonate external approver.
- External release gate or missing provider → Head blocks honestly; NO worker can invent authorization.

See `research/10-CONDITIONAL-MISSION-ROUTING-MATRIX.md` for a full table, decisions, exits and edge cases.

## 8. Measuring 99% correctly
Treat 99% as an **unproven target** for a precisely defined next-action routing benchmark, not a claim about entire mission success. Measure first-step accuracy, required-specialist recall, needless handoffs, correct abstention, complete-mission verification, specialist correctness, critical authority/evidence failures and efficiency separately. Use independently labeled accepted-next-action sets, hidden holdouts, real provider receipts, source/version binding, high-risk breakdowns, repeated variability trials and confidence intervals. Zero observed critical violations in a bounded suite is a release criterion, **not proof** of perfect safety. The existing 270 unique scenarios and three repeated runs are a pilot, not proof of 99%. See research/09.

## 9. Current documented feature ledger
- `research/01-VERIFIED-TAXONOMY-AUDIT.md` — actual vs uploaded colors.
- `research/02-ROLE-AND-SKILL-INVENTORY.md` — relevant job/competency mapping.
- `research/03-SOLO-DEV-MISSIONS.md` — practical missions.
- `research/04-DECISIONS-AND-GAPS.md` — original risk/decision research.
- `research/05-VERIFIED-SOURCES.md` — provenance and primary sources.
- `research/06-ALTERNATIVE-COMPANY-MODEL.md` — alternate Gold/Black model.
- `research/07-IDEA-APPROVAL-FEATURE-CATALOG.md` — 36 features, benefits/downsides/interactions, explicit approval status.
- `research/08-COORDINATOR-OVERLAP-AND-ROUTING-DESIGN.md` — exactly what three skills already do and where router fits.
- `research/09-ROUTING-ACCURACY-EVALUATION-PLAN.md` — statistical qualification, risk strata, 270/810 caution, paired ablation tests.
- `research/10-CONDITIONAL-MISSION-ROUTING-MATRIX.md` — detailed scenario-specific routing and truthfully blocked exits.
- `research/11-CROSS-THREAD-CANONICAL-HANDOFF.md` — this self-contained guide.

## 10. Next-thread startup instructions (READ-ONLY FIRST)
1. Open connected private GitHub `vixttha/Color-Team-OPS` and inspect current HEADs for `design/v0.0.2-team-contracts-single-lane`, `research/nine-team-role-audit-2026-10-30`, `release/v0.0.1-cloud-only` and `main`; do not rely on old SHAs.
2. Read this handoff and the feature catalog (07), coordinator overlap (08), routing plan (09,10), original constitution and latest D2–D5 records.
3. Ask whether any separate worker is still actively editing the v0.0.2 branch **only if it is materially necessary to avoid colliding writes**. Prefer read-only work on that branch until a safe handoff or explicit coordination.
4. Report which features are owner-approved as *direction* versus unapproved implementation details; explain positive and negative integration impacts.
5. Preserve all existing locked laws: cloud-only, provider-neutral, host-independent, no user local compute or runner prerequisite, one active worker, default read/advise, authenticated evidence and no auto merge/release/paid provisioning.
6. Propose versioned R1–R5 milestones integrated into existing v0.0.2 work; no new coordinator and no authority downgrade. **Do not silently implement or release.**
7. When owner explicitly authorizes future implementation, isolate branch and merge planning, perform real tests and source-bound audit. Never invent a completed test.

## 11. Should the user stop the current v0.0.2 worker?
**Recommendation: no abrupt cancellation based solely on these research ideas.** The ongoing worker appears to have been doing D5 provider-provenance/host-neutrality work, logically complementary to the new routing improvements. Let it finish the explicitly assigned bounded milestone and record exact SHA, CI results and open limitations. Then align R1–R3 with the verified base in a nonconflicting branch or next planned v0.0.2 stage. If the worker is **about to edit the same roles, routing contracts or schemas**, ask for a *checkpoint/pause before overlapping edits* so duplicated or incompatible work is avoided. A GitHub branch commit cannot verify a remote worker process is currently active, so do not assert it is running or stopped.

## 12. Sources
Project repository: https://github.com/vixttha/Color-Team-OPS ; v0.0.2: https://github.com/vixttha/Color-Team-OPS/tree/design/v0.0.2-team-contracts-single-lane ; research branch: https://github.com/vixttha/Color-Team-OPS/tree/research/nine-team-role-audit-2026-10-30/research ; NIST NICE: https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/about ; OpenAI eval guidance (methods only): https://developers.openai.com/api/docs/guides/evaluation-best-practices .
