# Idea + Feature Library v0.0.2 — ChatGPT.com + owner runner ONE-LANE execution contract

**Development contract (2026-11-11):** User approved bounded v0.0.2 development and use of existing Color-Team-OPS self-hosted GitHub runners. No separately authenticated independent external reviewer is required for the requested *internal* process; the label **INTERNAL AUDITOR** is logical role separation in one ChatGPT thread, NOT independent human/security attestation. Never claim "bulletproof", "fully independently audited", "release authorized by GitHub Actions", "all hosts updated" or "zero bugs".

## Authority, provenance and verified sources

- Dedicated source: `vixttha/Color-Team-OPS`, `idea-feature-library-v0.0.2`, review-only draft PR #22 against `review/idea-feature-library-v0.0.2-staging`. The immutable v0.0.1 baseline is `7b22c0417faa7ec11bab22f4dc4e12caea69ce87`. Do not merge to the frozen branch, `main`, the v0.0.2 Color Team OPS product, Governance or another project as a side effect.
- Verified runner identity from prior Color-Team-OPS GitHub run [42160529828](https://github.com/vixttha/Color-Team-OPS/actions/runs/42160529828): Linux runner `color-team-ops-linux-01` and Windows runner `color-team-ops-windows-01`, both carrying `self-hosted`, OS, `X64`, `color-team-ops` labels. Earlier successful runs do not establish that they are online now or secure against compromise.
- GitHub [secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use): persistent self-hosted runners have risks from untrusted workflow code; restrictive token settings do not provide a sandbox or identity attestation.
- GitHub [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): `needs` gives sequential jobs, permissions can be scoped to `contents: read`, concurrency prevents overlap.
- GitHub [manual workflow trigger](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow): a `workflow_dispatch` workflow must be present on the default branch to be dispatchable. Our development-only one-shot arm therefore uses a **path-filtered push event**; nothing is installed on default `main`.
- Verified pinned [actions/checkout commit](https://github.com/actions/checkout/commit/11d5960a326750d5838078e36cf38b85af677262) is 40 hexadecimal characters; the first arm mistakenly used a nonexistent 37-character SHA. The corrected pin must be enforced by `tests/test_pipeline_contract.py` prior to a single retest.
- GitHub [runner labels](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow): jobs target existing confirmed runner labels, not unspecified `self-hosted` hardware.
- Host-specific observed source: [MONDEX](https://github.com/vixttha/MONDEX) had 20 ideas, 27 features and a real Linux+Windows library acceptance [41906796137](https://github.com/vixttha/MONDEX/actions/runs/41906796137). [D-D-World](https://github.com/vixttha/D-D-World) had 7 ideas, 1 feature and passing repo registry run [41260377480](https://github.com/vixttha/D-D-World/actions/runs/41260377480). These receipts predate this candidate and do not certify a v0.0.2 upgrade. See the [cross-project audit](V002-CROSS-PROJECT-ADOPTION-AUDIT-2026-11-10.md).

## One ordinary ChatGPT.com conversation, ONE active writer

**HEAD → one WORKER → VALIDATE → logical INTERNAL AUDITOR → HEAD**, repeated only for bounded repairs. ChatGPT coordinates tasks and reads GitHub evidence; **GitHub Actions is an external test executor, not an LLM worker or a release approver**. Each step must cite repo/branch/exact SHA, changed files, test receipts and unknowns. No unattended promise, no implicit background continuation, no parallel writes or circular team dispatch.

1. **HEAD preflight**: inspect exact current GitHub branch and draft PR, all changed paths, no other active branch writer, required owner approval, run budget, runner trust. Keep source/adopter/Governance boundaries. Allocate ONE task and acceptance criteria.
2. **WORKER / source fixes**: maintain reusable host-neutral v0.0.2 library and tests; preserve both v0.0.1 schemas; explicitly support project schema extensions (`maxLength`, `limitations`, `project_milestone`). Avoid direct project-data imports. No automatic GitHub runner execution as each file is saved.
3. **VALIDATE / one owner-arm event**: after Head verifies final source and workflow YAML, make exactly ONE reviewed commit creating `ops/acceptance/idea-feature-library-v002-arm.txt` containing a reviewed arm line. The first arm used `APPROVED-SCOPED-V002-ONE-LANE`; after the verified pre-step checkout-pin failure, the one allowed correction uses `APPROVED-SCOPED-V002-ONE-LANE-RETEST-01`. Only that path triggers `.github/workflows/idea-feature-library-v002.yml`. The event runs Linux first and then Windows on the same exact event SHA. There is **no pull_request trigger**. Both jobs assert SHA and runner identity; Windows uses a one-run scratch clone with non-CRLF Git settings. Python dependency-free regression tests, schema checks, synthetic populated-adopter profiles and deterministic index checks run inside the existing owner runner capacity. No secrets, package installs, elevated permissions, hosting services or cross-repository clones.
4. **INTERNAL AUDITOR**: challenge the actual GitHub run/log/job-step evidence, negative tests, source boundaries, index diff, schema profile compatibility, missed cases and misleading PASS claims; report unverified and repair tasks back to Head. Windows scripted internal checks only cover limited invariants; they **cannot** authenticate an independent reviewer or externally verify the correctness of source claims.
5. **HEAD disposition**: if both jobs PASS at the same SHA, grant **scoped source regression PASS only**. If not, repair on the same branch, re-audit and authorize at most one new arm trigger after reviewing failure. Do not re-run failing jobs speculatively or spend runner budget without evidence. Real adopter rollout remains a separate conditional gate.

## Three modes, not three products

| Mode | What is actually proved | Required evidence |
|---|---|---|
| `SOURCE_REGRESSION` | Reusable source shape, parser, index, path checks and synthetic profiles on Linux and Windows | Exact-SHA completed successful Linux and Windows jobs and source-diff check |
| `ADOPTER_CANDIDATE` | A **host-specific** review branch in MONDEX or D-D-World safely merges additive hardening without replacing host records, local schemas, runner workflows or canonical indexes | Read-only `python tools/adopter.py <host-root>` plan, host before/after Git diffs and host-local tests; no cross-repo installation by this source workflow |
| `RELEASE_REVIEW` | Owner accepts the specific limitations and receives a reproducible portable package | SHA-bound record, resolved P1 findings, no-clobber adopter evidence, explicit owner release approval; no independent auditor claim when no such actor participated |

The source acceptance job alone may not silently promote into either adopter mode.

## No-clobber rules for live adopters

- MONDEX preserves `idea-feature-library/`, 47 canonical records, 64 KiB file cap, 10,000-record file cap, NaN rejection, host lifecycle semantics, custom index columns and existing self-hosted CI. Generic v0.0.2 helper must not replace MONDEX's custom source byte-for-byte.
- D-D-World preserves its root `ideas/` and `features/`, 7+1 canonical records, local feature-schema fields `limitations` and `project_milestone`, and the distinct Session Chronicle product/decision authority.
- Both hosts must receive additive reviews on distinct project-owned branches before any merge. Never edit `main`, workflow settings, secrets or another repository through the generic source CI.
- A Governance-style root `ideas/` (EvilMon-Bible, CLEANSPACE-Bible, Gauntlet or Meta-AI-Bible) is a **namespace collision**: DO NOT copy over or automatically convert it. Governance remains wholly unaware of this side template.
- `tools/adopter.py` is **plan-only**; it never writes to the source or host. It reports KEEP_HOST/REVIEW_LOCAL_DIFFERENCE/ADD statuses. Existing symlink paths block the preflight, but a hostile concurrent filesystem actor can still race these checks. Test only in a trusted disposable location with least-privileged OS user.

## Hard stops

Missing exact SHA; unexpected commit; unaudited workflow modification; unknown/unsafe runner; failed tests; dirty checkout; unapproved cost; source-data leak; stale index; unsupported schema keyword; path collision; unexpected host changes; no authenticated proof for an external test or approval; anyone inferring `verified` or `shipped` from metadata.

**No automatic merge, publication, cross-project update, runner installation, Governance modification or final release attestation.**

## Gate ledger (fill from live evidence only)

- Pipeline source SHA: **PENDING**
- First arm SHA: `52cfd9a76b703a76fd26ec5d62fd353a7a8707a4`; first GitHub Actions run [43108868818](https://github.com/vixttha/Color-Team-OPS/actions/runs/43108868818) **FAILED in setup, before test execution**. Job [130819270641](https://github.com/vixttha/Color-Team-OPS/actions/runs/43108868818/job/130819270641) log: checkout action pin had 37 hex characters, was unavailable. Linux runner was assigned; Windows was skipped. **No regression PASS claim.**
- Retest arm: **NOT ARMED** until exact repaired source is audited
- Linux regression: **NOT EXECUTED** (first job failed before checkout).
- Windows regression: **NOT EXECUTED** (first job failed; Windows skipped).
- MONDEX upgrade: **NOT APPLIED**
- D-D-World upgrade: **NOT APPLIED**
- Independently authenticated review: **NOT REQUESTED / NOT CLAIMED**
- v0.0.2 final release: **NOT AUTHORIZED**
