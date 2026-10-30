# Color-Team-OPS — Owner-directed feature ideas and exhaustive discussion inventory

**Recorded 2026-10-30. Status: DESIGN IDEAS ONLY.** This page captures the user's approval of the *direction*: "evolve Color-Team-OPS from a system that follows suggested team sequences into one that determines which specialist is needed, why, when, and what evidence must exist before advancing." The user expressed positive interest in (1) a searchable role/capability registry, (2) explicit team handoffs, (3) measured specialist tests and (4) a routing policy engine, and requested all discussed features documented with pros/cons/interactions. **This is not approval to implement, merge, provision services, replace team meanings, halt another worker, or release v0.0.2.** Preserve the existing v0.0.1 behavior and ongoing v0.0.2 branch.

## Principle: capability composition, modular architecture, feature synergy
The user prefers components that amplify each other's utility. Use stable interfaces, narrow responsibilities, common event/evidence contracts and small replaceable capability packs. Treat composability as a hypothesis to benchmark: adding layers can also create coupling, bugs, overhead, stale metadata and hidden failure chains. Prefer the smallest composition proven to improve measured outcomes over a monolithic orchestration prompt.

## Ownership: 3 coordinators, nine specialists; no new skill
- **Mission Control:** mission contracts, intent/classification, permissions, explicit grants, allowed tools, budgets, stop/risk boundaries.
- **OPS Director:** Head's **only** cross-team router; candidate search, eligibility, dependency checks, next-step selection, one worker, loop caps and terminal outcomes. Embed the *proposed routing-policy engine* here or behind a pure reusable policy library, **not** as a fourth coordinator.
- **Verification Gate:** actual evidence checks, exact revision and acceptance checks; separately performed logical Internal Auditor challenge phase; no automatic White/Purple substitution.
- **Nine specialist workers:** Yellow, Orange, Green, Red, Blue, Purple, White, Black Threat Intelligence, Gray Cell. Keep current roles. 'Gold management' is a Head competency suggestion, not a replacement team; 'Black infrastructure' from the uploaded alternate model is Green in the released product.
- **Existing v0.0.2 code:** D2 policy verifier, D3 evidence adapter, D4 host authority, D5 provenance are already underway. The new ideas extend quality of selection, metadata and specialist evaluation; do NOT replace these trust controls.

## Feature catalogue — everything raised in the routing and accuracy discussion
Each row states (a) how it adds value; (b) downside; (c) which existing feature it improves. "Proposed" means no implementation claim.

| ID | Feature/idea | Positive value | Negative / failure mode | Integration/synergy | Status |
| --- | --- | --- | --- | --- | --- |
| F01 | **Conditional, evidence-driven routing** rather than fixed nine-team sequences | Avoids misroutes and irrelevant team calls | Rule complexity, missed unknown cases, hard-to-explain choices | OPS Director + Registry + Gates | **Approved direction**, not implemented |
| F02 | **Searchable role-and-capability registry** | Head locates a qualified specialty within a team | Metadata staleness, taxonomy bloat, wrong tags | F01, F05, F10, F20 | Favorably selected idea |
| F03 | **Versioned capability IDs + ownership** | Deterministic team mapping, reproducible decisions | Migration/version burden, alias collisions | F02, F20, F28 | Proposed detail |
| F04 | **Sub-specialist competency packs** (backend, AppSec, SRE, etc.) | Better task-matched checklists without new agents | Prompt sprawl, token costs, false implied expertise | F02, F12, F25 | Proposed detail |
| F05 | **Concise metadata search / lazy loading** | Smaller model context and faster specialist matching | Retrieval misses, broken context/knowledge linkage | F02, F04, F27 | Proposed detail |
| F06 | **Explicit handoff contracts** | Required context and evidence cannot silently disappear | Schema overhead, rigid workflows | F01, F10, F13 | Favorably selected idea |
| F07 | **Suggested vs required vs optional vs forbidden handoffs** | Reduces needless dispatch and clarifies mandatory checks | Incorrect trigger conditions, complex dependency graph | F01, F06, F08 | Proposed detail |
| F08 | **Dependency/conditional transition graph** | Explains why the next team is justified | Cycles, edge explosion, wrong assumptions | F07, F09, F17 | Proposed detail |
| F09 | **Routing policy engine in OPS Director** | Separates constraints from model judgment; testable decisions | Duplicates existing policy if separate; added maintenance | F01/F02/F06/F10; build as extension, NOT 13th skill | Favorably selected idea |
| F10 | **Deterministic eligibility and safety rules** | Prevents wrong authorization, bypass and scope drift | Too-strict fail-closed decisions; unavailable authority blocks progress | Mission Control + existing D2/D4 + F09 | Existing base concept; refinement proposed |
| F11 | **Evidence-driven judgment among eligible specialists** | Adaptable to diverse tasks | Nondeterminism, inconsistent explanations | OPS Director, registry, benchmark | Proposed detail |
| F12 | **Risk classification and task classification** | Different routes for outage, login, incident, UX, research | Misclassification can hide mandatory checks | Mission Control + F01/F07 | Proposed detail |
| F13 | **Common structured completion envelope** | Traceable artifacts, exact SHA, limitations, suggested next team | Serialization burden, brittle migrations | Existing v0.0.2 universal team contract + F06 | Design exists; extend, do not duplicate |
| F14 | **Independent provider-evidence verification** | Prevents workers from self-certifying results | Missing cloud capability makes some tasks UNVERIFIED | Verification Gate + existing D2/D3/D4/D5 | Already in progress; not newly invented |
| F15 | **Distinct internal auditor phase** | Challenges omissions, false PASS and stale proof | Latency / repeated checking if not scoped | Existing Head→Worker→Validate→Internal Auditor→Head | Already in v0.0.2 design |
| F16 | **Exact-revision / source-SHA binding** | Stops stale tests being reused on changed code | Re-running tests costs time; selective invalidation hard | F13/F14/F15 and provider adapter | Existing rule; keep |
| F17 | **Single-lane / bounded repair / stop controls** | Prevents parallel writes, loops and runaway costs | Restricts throughput; deadlocks without recovery policy | Head, F08, F09; managed lock only in enforced option | Existing design; not a global mutex by prompt |
| F18 | **Tool availability / authorization / safe abstention** | Truthful CAPABILITY_BLOCKED/UNVERIFIED rather than invented progress | More blocked outcomes, less apparent completion | Mission Control, F10, F14 | Existing rule; keep |
| F19 | **External merge/release authorization gate** | No accidental 'deploy done' from code tests alone | More explicit owner approvals | Head + existing state/host authority | Existing design; keep |
| F20 | **Evaluation laboratory / role-specific benchmarks** | Evidence of actual specialist competence | Dataset construction, cost and grading errors | F02/F04/F09/F22 | Favorably selected idea, pilot proposal exists |
| F21 | **Routing-specific benchmark** (accepted next team OR stop) | Directly tests claimed 99% routing target | Multiple valid routes, label quality, class imbalance | F01/F07/F09/F20 | New test-suite emphasis |
| F22 | **Paired baseline/candidate + ablation tests** | Determines whether registry/handoffs/router truly add value | More runs/cost; confounding if configs differ | F02+F06+F09+F20 | Proposed detail |
| F23 | **Hidden, independently labeled, representative holdouts** | Limits overfitting to published examples | Requires expert curation, refresh and protection | F20/F21/F24 | Proposed detail |
| F24 | **Statistical confidence / per-risk reporting** | Honest meaning for 99%, uncertainty and rare severe errors | Large data requirements; hard to claim global reliability | F20/F21 | Proposed detail |
| F25 | **Nine differentiated specialist scorecards** | Reveals Yellow vs Orange vs Blue errors separately | Aggregation/metric gaming, missing production ground truth | F04/F20/F24 | Existing v0.0.2 pilot design |
| F26 | **Zero observed critical violations as independent promotion gate** | Stops severe regressions even with high average score | Cannot prove zero future violations; may delay promotion | F10/F14/F20 | Existing proposal; test before release |
| F27 | **Cost/token/latency/handoff budgets** | Avoids asking nine teams for a trivial typo | Over-optimization may miss security requirements | Mission Control, OPS Director, F05/F22 | Existing budgets; measure real tradeoffs |
| F28 | **Versioned scorecards and safe promotion/rollback** | Avoids untested updates or behavior drift | Version management effort, stale data | F03/F20/F25/F29 | Proposed integration with existing promotion plan |
| F29 | **Monitoring and feedback-driven regression corpus** | Real failures inform targeted improvements | Privacy, data minimization, sampling bias | F20/F23/F28 | Proposed; no background process implied |
| F30 | **Specific scenario routing matrix** | Beginner-friendly and testable starting policies | Rules may be mistaken for mandatory fixed sequences | F01/F07/F12 | Previous answer refined; see 10 |
| F31 | **Cloud-only, provider-neutral, hosting-independent core** | Portable; no owner hardware prerequisites | Some advanced guarantees unavailable without hosted trust service | All features via replaceable adapters | **Already owner-locked CTO-LOCK-001** |
| F32 | **Optional authenticated host authority / managed lease and fencing** | If provisioned, strengthens cross-session state and exclusive gateway writes | Cost, operations, cloud failure, not universal for direct writes | Existing D4 and future enforced mode | Design only; not approved to provision |
| F33 | **Read-only external evidence adapters** | GitHub-first concrete source observations without lock-in | Vendor-specific semantics, provenance != user permission | Existing D3/D5 + F14 | Prototype/pilot evidence exists; limits documented |
| F34 | **Solo developer mission playbooks** | Easy starting points for build, auth, outage, incident, UX, research | Over-simplified ordering; may omit context | F01/F12/F30 | Research guide exists |
| F35 | **DORA-style delivery health outcomes (secondary measures)** | Checks whether orchestration improves shipping and recovery | Metrics can be misleading for small samples/solo work | F20/F22/F27 | Proposed optional business/engineering measure |
| F36 | **Cross-thread canonical handoff / decision record** | Other threads can accurately continue from source-of-truth | Can become stale if not revision-stamped | All features + linked GitHub docs | Requested; see 11 |

## Feature-combination impact map
- **Registry + Routing Engine:** eligibility based on actual capabilities rather than a generic color name. **Bad interaction:** wrong registry entry becomes automated misrouting. **Mitigation:** vetted metadata versions + test cases.
- **Registry + Handoff:** per-specialty required input/output and evidence. **Bad interaction:** combinatorial schema variants. **Mitigation:** common envelope with optional scoped, typed extensions.
- **Routing Engine + Handoff + Existing D2/D4 authority:** no next worker on unsupported claim or unauthorized action. **Bad interaction:** too many blockers and slower missions. **Mitigation:** explain blocks and offer read-only fallback, never downgrade security.
- **Evaluations + Registry:** identify missing, redundant or weak capabilities; promote only when measured. **Bad interaction:** tests overfit to registry vocabulary. **Mitigation:** unseen natural-language requests and blinded labels.
- **Evaluations + Router:** tune conditional rules on labeled mistakes rather than intuition. **Bad interaction:** Goodhart/metric gaming and drift. **Mitigation:** multiple metrics, frozen holdouts, no blind online self-learning.
- **Evaluations + Handoffs:** detect lost evidence and wrong transfer schema. **Bad interaction:** longer tests and duplicate audits. **Mitigation:** scope-specific oracle and incremental validation.
- **Risk classifier + budgets:** use minimal specialist chain for simple tasks, expand on security risk. **Bad interaction:** underestimated risk suppresses required review. **Mitigation:** conservative triggers and independent risk tests.
- **Provider adapters + evidence:** source-backed completion gate. **Bad interaction:** availability/latency and provider lock-in. **Mitigation:** adapters and honest UNVERIFIED results.
- **Head + Gold-type management competence:** prioritize and budget without another authority layer. **Bad interaction:** mixing program planning with tactical routing. **Mitigation:** Head retains bounded mission control, not autonomous project creation.
- **Black threat intelligence + Green operations + Orange AppSec:** threat research informs protective changes without replacing Black. **Bad interaction:** research sprawl / speculative claims. **Mitigation:** verified dates and concrete stack relevance.
- **Gray + Yellow + Orange:** human misuse scenarios reveal bugs in UI, logic and access control. **Bad interaction:** synthetic personas may not represent real users. **Mitigation:** disclose simulation limits and verify with safe real-world UX feedback only when authorized.

## Rejected / guarded anti-features
Do not add a 13th routing skill; do not activate all nine teams on every mission; do not automatically convert Gold into a tenth worker, rename Black or delete Gray; do not claim 99% accuracy without statistics; do not use model text as trusted evidence; do not automatically train on private conversations/credentials; do not infer deployment or paid-host authorization; do not require user-owned machines; do not make D3 GitHub adapter the sole mandatory provider; do not create global write locks by prompt.

## Suggested order and readiness
1. **Research and decision only**: baseline team/coordination ownership, feature metadata, acceptance criteria, status labels.
2. **R1** versioned searchable registry sidecar with no permissions; no new skill.
3. **R2** routing conditions and typed handoffs in OPS Director using existing mission + evidence + policy contracts; acceptance against frozen cases.
4. **R3** build evaluated specialty packs only where benchmarks show value.
5. **R4** expand existing evaluation lab to routing-specific cases and paired component ablations.
6. **R5** promotion on exact revision with independent safety evidence and per-risk scorecards; optional cloud-enforced mode remains separately authorized.

No product code or v0.0.2 design branch is modified by this research.
