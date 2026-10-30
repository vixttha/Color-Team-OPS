# Issue #8 / M3 — Yellow typed-handoff candidate

**Single active specialist:** Yellow, on master integration branch. **One version:** v0.0.2. **No fourth coordinator.**

The existing `policy_v002/route_advice.py` remains explicitly **recommendation-only**. This task extends `HandoffDraft` with the mission objective, caller-declared tools, previous gate status, remaining consented handoffs, exact source/revision, explicit stop conditions and optionally referenced previous Validate/Audit IDs. The authorization status remains `UNVERIFIED_HOST_GRANT`, even if its advisory decision says `SUGGEST_ONLY`.

The existing `tests/test_v002_route_advice.py` now has **39 authored tests** including the advisory Yellow→Orange→Yellow sequence, absent previous audit, exhausted handoff budget, rejection of malformed gate references and typed handoff scope. A suggested team is never a real dispatched Worker, signed permission, or live authenticated actor.

**Limitations:** This code is not automatically executable inside the installed private ChatGPT plugin, and the current installed v0.0.1 coordinator has not been updated. No end-to-end installed v0.0.2 one-prompt mission has been run. The previous candidate's 34/34 sandbox result applies only to its previous source hash, not these five new tests. No native exact-current-SHA suite was run.

**Gate request:** Validate actual Python cases in an approved cloud test environment, then challenge forged previous-gate references and concurrent/stale Head decisions. Until then M3 remains `REFERENCE_UNVERIFIED`. No merge, release or deployment.
