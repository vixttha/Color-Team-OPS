# Existing coordinators versus requested routing improvement — duplicate-control audit

**Design proposal only / 2026-10-30.** Source basis: exact existing `skills/mission-control/SKILL.md`, `skills/ops-director/SKILL.md`, `skills/verification-gate/SKILL.md` at `release/v0.0.1-cloud-only`; `docs/02-SINGLE-LANE-ARCHITECTURE.md`, `docs/03-UNIVERSAL-TEAM-CONTRACT.md`, `docs/12-SPECIALIST-PERFORMANCE-DECISION.md`, `docs/17-D2-POLICY-VERIFIER.md`, `docs/21-D4-HOST-AUTHORITY.md`, `docs/24-D5-PROVIDER-PROVENANCE-PILOT.md`, and `docs/23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md` at `design/v0.0.2-team-contracts-single-lane`. These branches move independently; re-read before implementing.

## Direct answer: is the routing policy engine already implemented?
**Partially in scope, not to requested capability depth.** Existing OPS Director triggers after completion and is explicitly responsible to "select at most one allowed specialist by findings/dependencies", budgets, repeat caps and DISPATCH/COMPLETE/IDLE/BLOCK/ESCALATE/CAPABILITY_BLOCKED. So adding a separate 'routing agent/skill' duplicates the existing Head. The new value would be a **versioned, inspectable candidate selection and dependency *policy*** attached to OPS Director, searchable capability metadata and measurable precision/recall, not another new orchestration authority.

**Caution:** existing v0.0.2 `D2 policy verifier` is an **authorization, state and provenance verifier**, not a general intelligence classifier for 'which team is best'. Do NOT replace or repurpose this trust-boundary verifier. Route recommendation `R` and trusted legality check `P` are separate operations: a model can suggest R; only authenticated P permits the transition. A confident or highly rated route is never an authority grant.

## Responsibility boundaries
| Concern | Existing owner | Already present | Proposed extension | Must NOT do |
| --- | --- | --- | --- | --- |
| Intent, resources, permission, budget, risk/stop rules | Mission Control | Yes in skill/mission contract | Typed task/risk tags; resource and capability eligibility manifest | Invent user grants or authorize automatically |
| Candidate discovery and team handoff suggestions | OPS Director | At-most-one team by findings/dependencies | Capability lookup; deterministic eligibility gates; dependency graph; rank among allowed; explicit decision reasons; no-op/abstain | Self-create work, parallel writers, override policy verifier, new 13th skill |
| Gate correctness | Verification Gate + v0.0.2 D2 / provider adapters | Trusted evidence/SHA semantics drafted and D2 implementation exists | Validate next-step prerequisites against typed handoff; check exact source/mission/task version; reject contradictory data | Treat worker narrative as actual CI evidence |
| Independent challenge | Separate Internal Auditor phase under Head/Verification Gate architecture | Logical phase in v0.0.2 contracts | Probe missing required team, wrong source binding, false "all clear", replayed handoff | Become White team, self-approve release or claim independent outside human |
| Specialist task work | Nine workers | Released skills and v0.0.2 specializations | Lazy-loaded task-specific competence packs and evidence rules | Set their own permissions, route peers or certify completion |
| Quality evidence | Development eval lab / Head promotion decision | v0.0.2 270-case proposal + measured adapter tests (different objective) | Routing benchmark, ablations, holdouts, per-risk outcomes, performance lineage | Treat provider CI tests as proof of routing accuracy |

## Candidate routing-policy-engine interface (conceptual only)
**Inputs:** versioned mission contract; source revision; request/task class; requirements; risk and data sensitivity; provider capabilities + owner-granted authorization; approved team IDs; existing findings; prerequisite and stop-rule status; dispatch budget; registry version; prior route decisions.
**Stage 1: safety filter:** reject unsupported/disallowed teams or actions; enforce mission authorization, correct source revision, no active worker, no exhausted budget/loop, no missing mandatory evidence. State `CAPABILITY_BLOCKED`, `UNVERIFIED` or `ESCALATE` rather than invented progress.
**Stage 2: obligations:** derive minimal required capability set from independently reviewable policy conditions. E.g. sensitive-auth-code => authn/authz review required; deployment => cloud readiness/release grants; Red offensive tests => verified authorized target and ROE; no deployment inferred from code task.
**Stage 3: candidate search:** match required capabilities against stable IDs and versioned metadata; only load top relevant specialist playbook (not all nine).
**Stage 4: decision:** choose one permitted worker with a traceable reason and minimal necessary work; if uncertainty could affect safety or quality, request diagnostic information or give blocked/unverified read-only result. Handoff recommendation alone cannot dispatch.
**Stage 5: completion-cycle:** the worker returns structured outcome → Validate → distinct internal audit → Head accepts, repairs, reroutes or blocks. Each subsequent route uses current trusted state and evidence rather than old assumptions.

## Mandatory versus discretionary
- **Mandatory:** obligations tied to acceptance criteria, known critical risks, authorized safety or compliance policy; cannot be skipped for speed.
- **Conditional:** triggered by an observed finding (e.g. Gray user error calls Yellow repair; Blue detector fails calls Green instrumentation).
- **Optional:** useful only if it can improve a stated goal or materially reduce risk (e.g. Black threat context for a particular product stack).
- **Forbidden:** unauthorized scope, unavailable tool, undispatched team, outside ROE, production effects not approved.
- **Stop/no-op:** no evidence to continue, already accepted mission, unresolvable tool/authority gap, loop/budget exhausted, exact revision changed, external release gate outstanding.

## Minimal schema extension proposal
```json
{
  "routing_contract_version": "IDEA-NOT-IMPLEMENTED",
  "mission_id": "M-42",
  "mission_revision": 7,
  "source_sha": "0123456789abcdef0123456789abcdef01234567",
  "registry_version": "r1",
  "task_class": "auth_feature",
  "risk_tags": ["authorization", "personal_data"],
  "required_capability_ids": ["orange.auth-review"],
  "candidate_team": "orange-team",
  "candidate_capability_id": "orange.auth-review",
  "classification": "REQUIRED",
  "reason_code": "AUTHZ_BOUNDARY_REQUIRES_REVIEW",
  "prerequisite_evidence_refs": ["provider:record-with-source-binding"],
  "review_status": "HEAD_RECOMMENDATION_ONLY",
  "on_unavailable": "CAPABILITY_BLOCKED"
}
```
The example uses fake identifiers and never pretends that a source SHA or permission was observed. Actual schema changes must be versioned against existing released JSON, not silently inserted.

## Main negative interactions and mitigations
1. **Double-routing authority:** adding a fourth coordinator or letting a router dispatch directly creates conflicting decisions. *Mitigate:* OPS Director only; Head still decision authority.
2. **False trust elevation:** routing policy guesses permission from text, or D3 GitHub comments treated as authenticated Head roles. *Mitigate:* dedicated D2/D4 check separate from routing; fail closed on absent protected host.
3. **Stale metadata / retriever failure:** correct team excluded from candidate list. *Mitigate:* minimal versioned taxonomy, static coverage assertions, manual read-only fallback where safe, allow abstention and record unknown gap.
4. **Many rule interactions:** contradictory condition sets cause loops, impossible routes and high cost. *Mitigate:* deterministic conflict resolution + fixtures + maximum handoffs.
5. **Duplicate evidence checking:** route engine does gate's work, creating slow or inconsistent PASS. *Mitigate:* router only consumes verifier verdict; verifier alone evaluates evidence truth.
6. **Security over-routing:** nine-step missions on trivial tasks. *Mitigate:* risk-adjusted minimal candidate route; measure unnecessary dispatch rate.
7. **Security under-routing:** budget suppression of mandatory Red/Orange/Blue work. *Mitigate:* hard safety/acceptance requirements before efficiency optimization.

## Build sequencing
- Stage A: **read-only registry + typed routing recommendations** as new data and tests only; no live switching.
- Stage B: integrate with OPS Director while preserving existing D2 verification and Head decision.
- Stage C: add schema-validated handoff envelopes with test cases for missing evidence, unauthorized team and stale source SHA.
- Stage D: evaluate via same-task baseline/candidate/ablation suites; promote only after owner-approved threshold and no critical regressions.
- Stage E: optional later cloud-managed enforcement only with explicit hosting/cost approval; base plugin remains usable without it.

## Existing current-progress caveat
As of checked time 2026-10-30, the design branch has D4/D5 candidate work and provenance tests, but its GitHub-account-attributed five-step pilot **does not prove authenticated host mission authority or independent model-role identities**. A green runner and completed workflow is NOT equivalent to demonstrably excellent specialist performance. No "99%" is currently measured.
