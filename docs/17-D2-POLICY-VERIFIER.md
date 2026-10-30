# D2 — Read-only cross-record policy verifier (prototype)

**Status:** future-v0.0.2 reference, not production authorization, not a global lock, and not a shipped plugin. This implementation is **read-only**. It cannot dispatch teams, write to GitHub, merge, authenticate the host user itself, create a cloud lease, or grant execution permission.

## Inputs
Seven D1 Draft 2020-12 schemas are validated first: mission, work orders, worker events, evidence claims, gate records, and Head decision. A `TrustAdapter` instance supplies **separately obtained** authorization, dispatch proof, exact live SHA, criterion-specific provider observations, gate provenance and optional exclusivity checks.

**Hard trust boundary:** Python dataclasses and a `TrustAdapter` object are **not inherently authenticated**. Only a separately deployed, protected adapter that reads genuine provider/host authority can make observations trustworthy. Synthetic unit fixtures model that interface; do not represent them as authenticated GitHub evidence. Until real provider adapters are integrated, all results from synthetic fixtures are `SIMULATED`, including a PASS result.

## Verification gates
- Exact D1 schema shape plus cross-record identifiers, unique IDs, no unapproved teams and nonempty required team list.
- Authenticated mission authorization must bind grant reference, principal, repository, branch, source revision, permitted teams/actions, issued Head decision and every task ID; claimed `actor=HEAD` alone is insufficient.
- Every work order must be linked to an authenticated dispatch and authorized task, contain valid allowed actions and criteria, and stay within repair limits.
- Every team task requires exactly one current-SHA `DONE` worker event. Required teams must appear; an unrequired team is allowed only if authorized.
- Each worker claim must match a task and resolve to a provider observation for a specified accepted criterion, task, provider record and exact SHA. All criteria need affirmative evidence; unrelated or missing observations do not pass.
- Exactly one VALIDATE and one INTERNAL_AUDIT gate must attest PASS for all criteria at the final SHA. Head references must point to those exact IDs. A trusted adapter must authenticate **both** distinct gate phases, including role identity and evidence refs. No separate auditor conversation is required.
- The source revision is checked before and after verification. A post-check write still requires fresh authorization and gateway checks; this **does not** create an atomic GitHub transaction.
- If global exclusivity is required, an actual trusted gateway assertion is required; setting `mode=ENFORCED_CLOUD` in a JSON document does not suffice.
- An internal PASS is not external release approval. `BLOCKED_EXTERNAL_APPROVAL` is a separate outcome for a verified internal mission that still lacks release permission.

## Outcomes
`PASS`: conditional **internal completion verification** against trusted adapter inputs; not a permission token or externally independent audit. `BLOCKED`: observed scope, authorization, outcome, mismatch, or invalid record. `UNVERIFIED`: missing trust anchor, proof, stale/unreadable provider, or incomplete coverage. `CAPABILITY_BLOCKED`: required exclusive write enforcement unavailable. `BLOCKED_EXTERNAL_APPROVAL`: internal work verified but release approval outstanding.

The reference verifier performs no mutation and needs no PC, runner, local server, always-on process, real API token or paid backend for use in a supported host. Owner self-hosted CI may test this developer source but is never a plugin runtime dependency.

## Remaining integration requirements
Real trusted host identity/authorization adapter, actual cloud evidence resolver, durable event history, role/provenance proof, state machine implementation, continuous cross-session ownership/enforcement and user-authorized release gate. Evaluate this code against live provider traces before claiming production verification.

## Security limitations
An arbitrary caller can fabricate an entire fake `TrustAdapter`. The prototype cannot stop that. This is intended to be run **inside a trusted host boundary**, not given an untrusted caller's adapter. Connector responses and logs may contain prompt injection and must be parsed as data. A read-only PASS is not race-free against branch writes; a write gateway must revalidate scope/revision/fence atomically as far as the provider permits. Test cases exercise these assertions using a named synthetic fixture adapter only.

See `policy_v002/verifier.py`, `tests/test_v002_policy.py`, and [v0.0.2 contract semantics](15-V0.0.2-CONTRACT-PROTOTYPE.md).

## D2 sequential execution evidence
The verifier now also requires a **trusted mission snapshot at HEAD_DECISION with no active Worker** and exactly four **provider-attested** transitions per final task: Head dispatch → Worker → Validate → Internal Auditor → Head. Each transition must belong to the assigned task, team, mission and exact source SHA, and must be authenticated by the supplied adapter. This proves sequential task tracing **only to the strength of that adapter**; it cannot enforce or attest a globally exclusive writer across unmediated GitHub clients. Future iterations still need persistently stored, genuine provider/host transition receipts. Required team tasks must also have at least one real evidence claim, rather than passing from another team's claim alone.
