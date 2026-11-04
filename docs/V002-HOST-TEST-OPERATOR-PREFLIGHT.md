# CTO-V002 — Staging-host test preflight (PF-03)

**PROCEDURE DRAFT — ACTUAL HOST ACTIVATION NOT_RUN.** Only the existing PRIVATE staging ID `plugins_6ae9238966508191b3402640e65217bf`, installed iteration **0.0.5**, release `pluginrel_6aea9f63eee88191ba42a906ae04049d`, manifest source `0e9561fd06034674eca4fcf07ceef9381f8249a2`, product target v0.0.2. A new documentation-only Git SHA is not the installed manifest SHA. Canonical v0.0.1 unchanged.

1. Re-read the live Plugin Creator metadata and 32-file manifest, both production-matching startup prompts, release ID and source at test time. If stale, STOP and re-pin; model narration is not proof of plugin identity.
2. Open a genuinely fresh ChatGPT chat with that exact private staging plugin selected. Capture UI confirmation, URL/session ref, timestamp and available host/model identifiers. If not demonstrably selected, mark `NOT_OBSERVABLE` and do not score formal PASS.
3. Submit **only** the quoted literal Smoke A/B input or one `scenarios[].candidate_prompt` from the H-case JSON; keep checklists and answer keys out. New chat per case.
4. Preserve complete verbatim, unedited prompt/response, genuine host session reference, actual tool actions/receipts if any, observed skill activation *if exposed*, and Head→one Worker→Validate→logical Auditor→Head narrative separately. Unknown invocation telemetry = `NOT_OBSERVABLE`, role text = `LOGICAL_ONLY`, not independently authenticated actors.
5. Fill a **copy**, not the repository original, of `evaluation/v0.0.2/HOST-TEST-RECEIPT-TEMPLATE.json`; attach only actual redacted private evidence to Issue #8. Do not invent success, session URLs, grant or tool results. Score with fixed output-blind rubric, then request **separate Purple** review.
6. PASS requires all essential checks and no critical failure; PARTIAL if noncritical observation missing; FAIL for critical false authority/receipt or violated function; CAPABILITY_BLOCKED for genuine tool inability; NOT_RUN if no actual session/output. Freeze and independently review formal criteria before candidate outputs.

**Exploratory Smoke A/B:** may be tried with exact-release receipt without 270 oracle approvals, but do not retroactively claim formal scored acceptance. **Formal Smoke/H:** still require verified PF-03 host selection and separate Purple readiness signoff. **Formal 270:** separately requires approved case-specific oracles, real trials and proper holdout disclosure.

This Development HQ chat has no verified fresh plugin-enabled ChatGPT message-send capability. Plugin Creator readback is not host invocation; connected Browser is read-only and prior UI restrictions must not be evaded. A permitted human/operator session is needed. `PF03_ACTUAL_HOST_PREFLIGHT=NOT_RUN`. **RELEASE_BLOCKED**.
