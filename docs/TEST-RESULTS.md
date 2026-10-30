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


## Orange/Yellow and Red/Purple repair validation — 2026-10-29

**Source revision tested:** `1795f0a87fcffec93d197e88edbc75144c98101c` (superseded by later documentation commit; never reuse as final SHA evidence).

- **Schema contract tests:** Three JSON Schemas self-validate under Draft 2020-12; all three official samples pass. A set of 15 adversarial probes rejects all 15 expected-invalid samples (7 base invalid-input probes plus 8 historical semantic bypasses). A separate 27-case source-level suite was reported earlier; this evidence is bounded to the tested revisions.
- **Workflow policy tests:** 13 source-specific parsed YAML and mutation cases passed using the GitHub workflow file content matched by Git blob hashes. This verifies syntax/policy invariants in the observed files, **not GitHub CI execution**.
- Tests were executed in an ephemeral cloud container, not on any owner computer or personal GitHub runner.
- **Native repository test suite in GitHub Actions:** NOT RUN. Hosted jobs fail before runner assignment. Latest observed [run 40976607605](https://github.com/vixttha/Color-Team-OPS/actions/runs/40976607605) on the above revision: both hosted runners unavailable with zero job steps. Cause unconfirmed; see [issue #2](https://github.com/vixttha/Color-Team-OPS/issues/2).
- **Real cloud authorization/identity checking:** NOT IMPLEMENTED in v0.0.1; JSON schema checks alone are not proof.
- **Installed private plugin reconciliation:** NOT DONE as of this record; Creator's plugin remains `0.0.1` from the earlier source.
- **Independent external reviewer acceptance:** NOT RECEIVED. PR #1 remains draft.

**Result:** Source-level repair evidence is positive; overall release acceptance is BLOCKED.
