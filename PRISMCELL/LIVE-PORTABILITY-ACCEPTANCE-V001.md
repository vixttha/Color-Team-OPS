# PrismCell v0.0.1 — live second-repository portability acceptance

**Status: NOT RUN / HOLD GENERAL LIVE-PORTABILITY CLAIM.** This is a controlled acceptance plan, NOT evidence of a completed real installation. It introduces no cloud host, no Vercel service, no product runtime and no GitHub-hosted compute.

## Fixed accepted source

- Canonical source: `vixttha/Color-Team-OPS` branch `template/prismcell-workbench-v0.0.1` at `2cdc66f37537c077db68eeb9fa190e24d071039f`.
- Tested source: `45ecbdc2460c22a79fff54557012f62b33c38a10`; approved [owner-runner run #41715667469](https://github.com/vixttha/Color-Team-OPS/actions/runs/41715667469) on Windows and Linux: 110 Node + 25 Python/schema tests per OS and offline 52-file synthetic starter PASS. Promoted canonical tree compares with zero changed files, but merge SHA itself was not directly runner-tested.
- [PR #18](https://github.com/vixttha/Color-Team-OPS/pull/18) merged; nine existing Color-Team-OPS workcells already pinned to canonical. Existing activity must remain untouched.

## Prerequisite: independent, dedicated test repository

The owner should explicitly designate **a new private GitHub repository dedicated to this test**, not an active product, an existing specialist home or another team's production namespace. GitHub repository creation is outside the currently available connected GitHub actions. **Do not pick an unrelated existing repository merely because write access exists.**

Use a clearly marked test-only project identity, with three *different* logical specialist teams such as `ASTRONOMY`, `STORY`, and `REVIEW`. These are distinct from Color-Team-OPS' nine specialist workcells, and are not additional Color-Team-OPS agents. Confirm the repository really exists and that its linked GitHub principal permits creating issues and team home branches before any writes. Do not enable Actions workflows, share owner-runner credentials, copy history from existing workcells, or alter the Color-Team-OPS product.

## Live acceptance procedure — each receipt required

1. **Provider preflight.** Obtain and record actual new repository URL, default branch commit SHA, privacy/permissions, and the authorized owner. Identify safe rollback (delete only the trial's own files/branches/issues if owner separately authorizes; prefer archive/leave test records until acceptance).
2. **Live channels.** Create three actual GitHub Issues titled `PrismCell INCALL — ASTRONOMY`, `PrismCell INCALL — STORY` and `PrismCell INCALL — REVIEW` in the new repository; read each issue back to verify its real issue number, URL and open state. Issue text is transport, not instruction authority.
3. **Home branches.** Create three unique, dedicated branches from the clean test repository's default branch, e.g. `agent/astronomy`, `agent/story`, `agent/review`. Read branch existence and heads before writing. Do not push to the default branch.
4. **Real config.** Build `prismcell-project-config-0.0.1` config from [config/example.json](config/example.json) with real repository, URL, project ID, branch names and **provider-observed** issue numbers/URLs. `transport` must be `github-issues-manual`. Do not fabricate live issue references or any authority.
5. **Clean generation.** From fixed source use the deterministic offline `core/starter.mjs` or `node PRISMCELL/tools/initialize-project.mjs --config project.json --out new-empty-folder --source-sha 2cdc66f37537c077db68eeb9fa190e24d071039f`. Require a *new nonexistent output directory*, no copied histories. Then run `node PRISMCELL/tools/verify-manifest.mjs new-empty-folder 2cdc66f37537c077db68eeb9fa190e24d071039f 3` and retain the verification receipt (expected inventory: 51 team documents + manifest = 52 files). Store expected manifest hash separately if testing tamper resistance. No local runner is needed in production; offline generation can be performed through any approved ephemeral test environment.
6. **Install real workcells.** Copy only each generated team's own 17 `TEAM-WORKBENCH/` documents to its matching authorized branch using the provider's normal write API. Do not copy `Color-Team-OPS` histories/legacy audit ledgers, commit original project source, or merge home branches. Record exact installed file Git blob SHAs and new branch commit SHAs. Bootstrap state must remain `BOOTSTRAPPED_PENDING_LIVE_VERIFICATION`, not fabricated ready.
7. **Provider readback / activation.** Re-fetch all three branch heads, stored files, corresponding live open Issues, and actual permissions; verify there are no unexpected files, stale recipient refs or invented evidence. Only authorized Head activation may change each verified workcell to `READY_ON_INVOCATION`; preserve `release_authorized:false`, `background_agent_running:false`, `active_work_item:null`.
8. **Bounded real INCALL test.** Post one harmless, explicitly synthetic-but-live GitHub Issue REQUEST through a real issue comment, confirm the recipient reads it and records a correct acknowledgment and source-linked outbox receipt. Ensure the acknowledgment conveys **received for review**, not an accepted instruction, security permission, autonomous worker or completed task. Re-read actual comment IDs and files; retain originals.
9. **Adversarial rejection.** Try a harmless schema-invalid message and a forged permission/Head-approval claim as test inputs, with bounded local treatment only; confirm they cannot grant authority, route to another team, modify another branch or cause automatic agent execution.
10. **Independent acceptance.** Record exact repository/branch/issue identifiers, source SHA, log excerpts, statuses, clean-install and negative-test evidence and gaps. Request Purple logical review after Yellow/Head validation. Final owner/Head decision distinguishes `PASS live GitHub/manual Issues portability` from `NOT CERTIFIED provider-universal or autonomous cloud runtime`.

## Gate matrix

| Gate | Required proof | Current status |
|---|---|---|
| G0 — accepted template source | Tested `45ecbdc...` + canonical `2cdc66f...` zero-file-diff promotion | **PASS** |
| G1 — separate real repository exists and is approved for testing | Actual repo URL, ownership and authorized writes | **NOT RUN** |
| G2 — three real issue channels and home branches | Live GitHub readbacks and exact branch/issue refs | **NOT RUN** |
| G3 — clean install without old history | New 52-file manifest verification; 17 per team copied independently | **NOT RUN** |
| G4 — safe activation/INCALL live trial | Actual branch, issue-comment and ledger receipts; no authority escalation | **NOT RUN** |
| G5 — independent logical Purple acceptance | Reviewed exact live-install receipts, limitations and Head decision | **NOT RUN** |

## Release boundary

Do not describe this as implemented merely because the instructions and fixture exist. `v0.0.1` is approved for its existing nine on-demand Color-Team-OPS workcells; a successful real second-project trial may support portability **to other GitHub/manual-Issues projects only**. No provider-universal, unattended or independently authenticated agent guarantee follows. Never deploy to Vercel or register persistent execution just to satisfy this bounded trial.

**Prepared by Yellow Team; Head decision:** G0 PASS, G1–G5 pending an expressly designated independent repository. No live project was provisioned, no test was dispatched, and no other repository was changed by preparing this plan.
