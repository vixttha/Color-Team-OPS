# CTO-V002-SINGLE-THREAD — M3 conditional OPS Director advisory router

**Implementation scope:** a function, not a new team or 13th skill. **Mission:** one v0.0.2 release. **Worker:** Yellow under Head.

`policy_v002/route_advice.py` uses M2's canonical nine-team directory and typed `RouteIntent`/ `RouteAdvice` / `HandoffDraft` contracts. It returns only `SUGGEST_ONLY`, `ABSTAIN`, `BLOCKED`, `UNVERIFIED` or `CAPABILITY_BLOCKED`. It **does not dispatch**, authenticate user authority, create a gate, lock another session, provide a tool credential or update mission state.

**Deterministic preconditions:** exact mission ID / SHA / observed SHA / revision; single active Worker (or no new suggestion), handoff count bounded by Head's mission grant, previous Validate+Internal Auditor stages recorded before another suggestion, declared allowed teams, required and forbidden capability IDs, declared tool availability. One recommended Worker must cover the whole required capability set; cross-team obligations yield an abstain for **Head-controlled sequential decomposition**, never a parallel dispatch.

**Typed handoff:** `handoff_draft` makes only `DRAFT_ONLY` records with mission/revision/SHA, one selected team/capability, explicit criteria and evidence refs. The authorization field is always `UNVERIFIED_HOST_GRANT`. An authenticated mission grant and true provider evidence must be verified by existing Mission Control/Verification Gate and a protected host separately.

**Identity preservation:** Exactly 9 workers, 3 existing coordinating skills. OPS Director owns route selection, no fourth orchestration skill. White is not a generic Internal Auditor. Red adversarial work is not authorized by a declared `authorized-target` string; that string is a metadata prerequisite only.

**Testing:** `tests/test_v002_route_advice.py` contains 34 targeted cases for stale source, revision conflict, no active Worker, prior gates, budget, wrong/forbidden capabilities, missing tools, multiple-team decomposition, malformed input, and draft-only handoffs. Actual execution evidence must cite the exact candidate commit. Earlier M1 and M2 tests remain separately source-scoped.

**Remaining:** M3 is a recommendation prototype, not a trusted cloud dispatcher. It has no protected identity provider, independent role attestations, global cloud lock or executed ChatGPT plugin trial. M4 must measure actual routing decisions against independently reviewed case oracles rather than mistake passing fixture tests for specialist intelligence. No paid cloud platform or owner runner is mandatory.
