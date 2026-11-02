# CTO-V002 P2/P5 — Supported-host pre-release audit (2026-11-02)

**Disposition:** P2 `REQUIRES_OWNER_DECISION`; P5 `BLOCKED` for real host acceptance. No v0.0.2 host trial was run. The canonical private plugin remains v0.0.1 (Plugin Creator get-plugin-metadata and list-plugin-releases live readback on 2026-11-02).

## Host capability inquiry
The connected Plugin Creator exposes plugin metadata, file/release readback, **create** and **update**. It exposes no verified ephemeral preview execution of an uninstalled candidate. `update_plugin` would alter the canonical installed private release, and `create_plugin` would introduce another identity, neither authorized by the owner. A GitHub source ZIP is not an installed plugin. Official testing guidance requires testing the **complete installed plugin** and recording real tool selections and results: https://developers.openai.com/plugins/deploy/connect-chatgpt . The Help Center documents testing by mentioning an installed plugin: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt . Neither source proves an approved unpublished preview is available to this account. Do not invent one.

**Safe owner options for a later instruction:** (A) explicitly authorize a distinct, private, disposable staging identity after verifying account eligibility, test, then dispose under separate approval; (B) explicitly authorize guarded update of the canonical identity to candidate after all other gates and an approved rollback protocol; (C) supply an already-authorized supported pre-release preview capability with exact version binding. None executed. The existence of a possible option is not a grant.

## Host trial matrix
See `V002-P2-P5-HOST-TRIALS.json`, 11 source-prepared scenarios all `NOT_RUN`. Each needs a real host session ID, exact installed version/source, observed output, tool receipts if any and independent validation. No passing score can be inferred from static tests. A single chat switching logical roles is not a separately authenticated specialist.

## Sequential review scope and static findings
- **Orange / HIGH**: no live protected host issuer for user consent, revision-bound D2 repair attestations, tenant revocation or globally fenced writing; these capabilities must remain blocked if claimed.
- **Orange / HIGH**: no installed-v0.0.2 authenticated denial tests (stale/forged receipt, permission escalation, revocation). Source-level negative regression is real, host conclusions are unverified.
- **Purple / HIGH**: no real host trace proves specialist re-entry or model routing quality. A recommendation-only Python result is not a dispatched Worker.
- **Gray Cell / MEDIUM**: ambiguity handling, no-tool recovery, progress clarity and no-routine-confirmation experience untested on candidate host.
- **Purple / MEDIUM**: the 54 proposed holdout IDs are visible in GitHub source and are **not blinded**.
- **Cross-check / LOW**: README/changelog and historical audit pages had obsolete `NOT_RUN` native-test statements; reconciliation in this source change is intended, subject to fresh exact-SHA native tests.

**Validate:** Plugin Creator live metadata and official testing documentation were independently checked. **Logical Internal Auditor:** refuses to promote static/fixture tests to a P2/P5 host PASS. **Head:** proceed with independent code/tests/release documentation; stop only host-dependent acceptance and restricted identity actions. Release remains BLOCKED.
