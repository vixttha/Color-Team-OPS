# Architecture v0.0.1 — No local execution dependency

## Installed artifact

`plugin.json` plus twelve portable `skills/*/SKILL.md`; supporting references are portable text and JSON schemas. There is **no** `mcp.json`, localhost URL, stdio command, local daemon, timer, webhook, GitHub workflow dependency, or local runtime packaged into this plugin.

## Logical flow (only within host-supported run)

Mission Control (contract) -> OPS Director (policy proposal) -> one of nine specialists -> Verification Gate (evaluate trusted evidence, maybe UNVERIFIED) -> OPS Director -> next authorized task OR COMPLETE/IDLE/BLOCK/ESCALATE/CAPABILITY_BLOCKED.

A skill's completion cannot itself start a new background ChatGPT/Kimi/Z.ai/Grok conversation. Host-provided continuity is needed even for in-session automatic handoffs. The host may stop or enforce approvals.

## Optional future cloud backend (NOT PART OF v0.0.1)

A host-neutral remotely hosted HTTPS MCP/API, managed cloud database, authenticated event ingestion, idempotent state transitions, budgets, one active write lane, durable queue, exact-revision independent gate, and bounded reconcilers. It must have an always-available **cloud-only no-self-hosted-runner mode** and explicitly negotiated host adapters. No always-on service is implied by packaging instructions.

## Decision policy

1. Reject unauthorized, malformed, stale, or unsupported missions (BLOCK or CAPABILITY_BLOCKED).
2. Verify actual external evidence; absent independent checks => UNVERIFIED, not PASS.
3. Prioritize safety/authority, security, functional, operations, defense, offensive, detection, intelligence, user behavior based on mission-specific findings and allowed teams.
4. Route at most one specialist per decision. Track event ID, source revision, work fingerprint and bounded retries to avoid loops.
5. No outstanding authorized tasks => COMPLETE. Waiting for an outside event => IDLE.

Proposed priorities are policy defaults and never override explicit scope or least privilege.
