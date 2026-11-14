# Example bounded handoff (not a claim of live automation)

1. Mission Control receives: "Review my cloud-hosted API for access-control issues; only read GitHub; 5 handoffs maximum".
2. OPS Director examines authorized available tools; without a GitHub connector it returns CAPABILITY_BLOCKED for repository inspection, while still offering generic security advice.
3. With authorized read-only connector, Orange examines a real change and proposes findings with exact refs; no unsupported tests are claimed.
4. Verification Gate distinguishes observed connector evidence from unverified narrative.
5. If verified findings require code edits but mission is read-only, OPS Director returns ESCALATE instead of upgrading privileges.
6. Once queue is empty, OPS Director returns COMPLETE. No artificial infinite loops or mandatory local execution.
