# 07 — Integration roadmap and proposed acceptance contract

**Do not integrate this design into v0.0.1 or alter its release workflow.** These are future v0.0.2 ideas, and no claim is made that they have shipped.

## Architecture implementation sequence
**Phase D0 — documentation:** isolated idea branch; user reviews contracts and resolves open choices. Do not modify any installed plugin or production source.

**Phase D1 — schemas:** version the universal team contract, scoped task request, completion event, validation record, internal audit record and routing transitions; preserve v0.0.1 compatibility through explicit migration and negative tests. Do not interpret a valid JSON schema as proof of authority.

**Phase D2 — specialist packages:** develop portable curated references, decision trees, checklists and skill-specific test oracles for all nine canonical roles. Maintain existing nine skill identities and three coordination skills.

**Phase D3 — head-controlled flow:** incorporate tested Issue #4 state-machine ideas only after architecture review, implement a single active Worker, bounded repair, explicit Validate then Internal Audit then Head, and exact-SHA final checks. Worker cannot dispatch, override scope or approve own release.

**Phase D4 — evaluations:** run the 270-case initial lab plan (or approved alternative), establish baseline and regression protection with real records. No invented benchmark PASS.

**Phase D5 — trust/host integration:** validate available cloud tools and host authorization, evidence resolution, provider-specific compatibility. Any optional cloud lock/state service must be provider-managed, cloud-only and not required for basic skills-first guidance; no false guarantee of persistent dispatch.

**Phase D6 — version acceptance:** user signs off specific v0.0.2 scope; reconcile source/package, real host skill trials, exact-SHA test evidence and release controls. Do not silently publish or merge.

## Proposed acceptance cases
- Single supported conversation completes a normal authorized task without a second auditor chat.
- Exactly one active Worker per mission phase; only Head can dispatch another team.
- All nine have differentiated playbooks, evidence outputs and tests; no role swapped (Yellow/Orange/Green/White especially).
- Three coordination skills remain; Internal Auditor is a phase, not new specialist or 13th skill.
- Worker reports both successful work and unverified/untested cases; self-check is not final acceptance.
- Validate rejects fake PASS, fabricated tool outputs, wrong SHA and unapproved write.
- Internal Audit can find issues despite a green functional test; cannot override negative Validate.
- Repairs have finite budgets, preserve authorization, rerun appropriate source-bound checks.
- Current-sha final gate requires validated acceptance from mission-required teams and a trustworthy current source read.
- Wrong specialist routing, unsupported tool/host, conflicting writer, stale data, invalid evidence and no-progress loops fail closed.
- Real external release governance is not waived but never requires an extra auditor chat for ordinary technical completion.
- Plugin runtime never calls/requires owner runners, local compute, localhost, local DB, desktop CLI or future unattended service.
- Package source and approved version correspond exactly; all release docs/test receipts reflect final SHA.
- Future contracts provide graceful skills-only mode on a supported browser host without cloud enforcement. Global cross-session locking is NOT VERIFIED in this mode.

## Three reference scenario families
1. **Clean:** Yellow executes → Validate PASS → Internal Audit PASS → Head COMPLETE.
2. **Repair:** Orange detects/repairs → Validate FAIL → Auditor notes issue → Head bounded same-team repair → new SHA → retest → PASS → Head COMPLETE.
3. **External release gate:** Green work passes internal gates → Head records internal_complete=true but external release permission remains BLOCKED_EXTERNAL_APPROVAL.

## Adoption gate
No automatic promotion to future v0.0.2. This documentation is a design candidate; owner approval, verified behavioral test evidence and release readiness are separately required. Never treat internal audit as an independent third-party audit.
