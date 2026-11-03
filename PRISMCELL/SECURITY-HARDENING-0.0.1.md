# PrismCell v0.0.1 security hardening — INCALL trial

Owner-directed one-lane Purple→Blue→Orange→Yellow→White/Purple verification. No changes to installed Color-Team-OPS plugin, HQ or product integration. Canonical team issue mapping remains nine specialists; purple-workcell != Purple Review HQ.

## Recorded changes
- Sender messages may only claim `POSTED` (not recipient ACCEPTED), no untrusted permission grants; limit payload/URLs, verify canonical team/branch mapping structurally.
- Work items may transition to `ACCEPTED` only with exact SHA, source-linked evidence, complete authorized-work-order fields, Validate PASS, logical Internal Auditor PASS and Head ACCEPT decision reference. SOURCE_OBSERVED or RESEARCH_CITED acceptance is allowed for *source research*, not falsely represented as live-host verification.
- State schema bounds nine legal teams, home mapping, source SHA and release flag; optional template_revision can be pinned during future adoption.
- `tools/guard.mjs` pure optional *reference* checker takes a trusted metadata envelope from caller, checks issue mapping, replay/edit fields, and returns `roleAuthenticated:false, authorityGranted:false` always. **These parameters are not themselves attestation**. Caller must obtain real GitHub API data and enforce write privileges externally. Even a valid guard output authorizes *triage only*, never acceptance or execution.
- `tests/guard.test.mjs` uses Node built-ins for optional developer/CI tests; installed workcell/plugin does not depend on Node or a local runner.

## Compatibility and caveats
Original queue items in QUEUED state remain valid without added acceptance evidence fields. Never apply an automatically inferred ACCEPTED status to legacy historical items. Other team source documents are unchanged by this template patch; each team should pin the installed template revision separately. GitHub comments are editable/deletable; their issue metadata, authorship and edit checks must be fetched afresh; the guard cannot guarantee cross-session security or actor-to-color authentication. Repo rulesets are not changed here.

## Test statement
Authoring step executed the exact pure JavaScript guard function bodies in a cloud JS execution isolate against 16 positive/negative cases; see work mission report for result. This is **NOT** a native Node test run, GitHub Actions CI run or independently attested host execution. Node test file is committed but remains NOT_RUN until a separately actually executed Node environment runs it. No self-hosted runner action was triggered.
