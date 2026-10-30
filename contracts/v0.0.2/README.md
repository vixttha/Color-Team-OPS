# v0.0.2 — Versioned reference contract prototypes

**STATUS: FUTURE DESIGN REFERENCE — not a deployed plugin, not production evidence, and not owner-accepted release.**

These seven **Draft 2020-12** JSON schemas are separate from the v0.0.1 release-branch schemas. They shape mission contracts, Head's work orders, worker claims, evidence pointers, gate records, Head decisions and phase transitions. They are **not drop-in backward compatible** with v0.0.1; source formats must be migrated deliberately and verified. The schema version is `0.0.2-prototype`, not a claim of a released software version.

Most importantly: **a valid schema never authenticates an actor, permissions, provider result, evidence receipt or source SHA**. The connector/host and eventual optional managed gateway must verify these claims. No model-generated field grants authority. Cross-record checks (required_teams subset, active worker singleton, true final-SHA validation/audit PASS, stale evidence rejection, expired authorizations) require trusted runtime/validator policy beyond JSON Schema.

Schema inventory:
- `mission.schema.json`: cloud-only, runner-independent mandate, authorized scope, explicit capabilities/requirements.
- `work-order.schema.json`: Head-scoped specialist assignment and acceptance criteria.
- `worker-event.schema.json`: result is never a verification PASS.
- `evidence-claim.schema.json`: untrusted provider pointers, not "authenticated evidence".
- `gate-record.schema.json`: distinct VALIDATE and INTERNAL_AUDIT phases; PASS requires pointers, which remain untrusted until independently resolved.
- `head-decision.schema.json`: only Head-shaped DISPATCH, REPAIR or COMPLETE; schema-level COMPLETE requires references but runtime must resolve final revision and actual PASS.
- `transition-event.schema.json`: allowed adjacent state transitions and actor labels; no shortcuts around Validate or Internal Auditor.

Read [contract semantics](../../docs/15-V0.0.2-CONTRACT-PROTOTYPE.md). Execute proposed test suite via Python `jsonschema` Draft202012Validator in `tests/test_v002_contracts.py`, if installed. A green structural test does not establish quality of specialist work or authenticity of evidence.

The permanent rule remains: **"Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate."** Developer testing may occur on owner runners by permission, but neither that CI nor a local runtime is required for normal plugin use.
