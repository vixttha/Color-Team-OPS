# Red Team workspace decisions

## RED-DEC-001 — 2026-11-02 — Separate home from product source
**Decision:** Use `team/red-team-agent` as the permanent Red Team documentation and investigation home. Base from the minimal `main`, not the active v0.0.2 integration branch.  
**Reason:** Avoid adding another integration writer or accidentally shipping team-HQ material in the plugin.  
**Boundary:** Red's home is not a new plugin skill, tenth color specialist or coordinator.

## RED-DEC-002 — 2026-11-02 — Durable GitHub record, not a continuously running agent
**Decision:** Persist state through versioned queue, findings, worklog and explicit rehydration on future invoked sessions.  
**Reason:** No unproven background execution, cross-chat state synchronization or global lock.

## RED-DEC-003 — 2026-11-02 — No privilege inheritance
**Decision:** Home-branch authorization does not allow active penetration tests, runner dispatch, other-branch writes, merges, plugin updates or releases.  
**Reason:** Constitution, one-thread Head control and owner approval boundaries remain binding.
