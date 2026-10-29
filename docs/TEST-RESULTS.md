# Pre-release validation

The following are checks of the **package itself**, not claims of a live cloud service: strict JSON parsing, JSON schema self-check, sample validation, skill frontmatter, role cardinality, local-dependency prohibition, ZIP integrity, archive reproducibility. Tests run on an ephemeral hosted build environment; runtime does not require this environment or any user-owned machine.

Actual browser host acceptance, persistent event handling, verified remote GitHub writes, and other-host imports remain NOT TESTED until those specific capabilities are connected.

## Cloud CI and hygiene extension

A GitHub-hosted CI matrix, optional manual self-hosted workflow, executable policy checks, and design documents are being added to the v0.0.1 draft branch. Actual CI PASS must be recorded for the final SHA from GitHub run evidence; otherwise this remains PENDING.

The successful runner-acceptance workflow on the separate runner-audit branch did not verify this release candidate. The Plugin Creator release was created before these GitHub-only changes and is not automatically synchronized.

## Observed GitHub Actions evidence — 2026-10-29

**Review candidate examined:** `22d607540767b82571dfb99524715b9fad349496` (before this audit-record commit). This is not the final SHA.

**Mandatory hosted CI:** [run 40971448503](https://github.com/vixttha/Color-Team-OPS/actions/runs/40971448503), event `pull_request`, conclusion `failure`. Both `ubuntu-24.04` and `windows-2022` jobs reported `runner_id: 0`, no runner name, zero steps and no test output. Therefore **tests were NOT RUN**; do not call this a test failure or PASS. An earlier [run 40970882875](https://github.com/vixttha/Color-Team-OPS/actions/runs/40970882875) showed the same pre-execution failure. GitHub-hosted runner allocation/account eligibility is unresolved; the exact cause is not authenticated.

**Optional workflow:** Earlier versions of the optional workflow generated failed push-event registration runs with zero jobs. The explicit, manual-only Windows/Linux revision on `22d6075...` generated no new optional push-event failure. No owner-runner jobs were dispatched. Its `workflow_dispatch` execution is **not tested**, since this workflow is not on `main`.

**Evidence status:** cloud CI BLOCKED / INCOMPLETE; optional CI unexecuted; package/source policy checks configured but unexecuted on GitHub runners. [Blocker issue #2](https://github.com/vixttha/Color-Team-OPS/issues/2). Do not merge PR #1 or declare release acceptance.

**Security boundary:** owner-runner jobs remain opt-in only, restricted to authenticated owner `vixttha` and trusted `main`. Neither source CI nor future plugin runtime may automatically fall back to personal runners.

