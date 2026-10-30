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

## 2026-10-29 — Owner-corrected v0.0.1 test plan

The owner explicitly directed use of their registered Windows/Linux GitHub runners for v0.0.1 release testing, and assigned the assistant to audit it. The earlier mandatory GitHub-hosted CI requirement is superseded by [ADR-0002](decisions/ADR-0002-ci-runner-choice.md); previous provider-runner failures remain historical evidence, not the selected release gate. The self-hosted runners must **never** be required by the installed plugin or its future cloud services. No test PASS is claimed until actual job logs on the exact v0.0.1 SHA are obtained. The existing private Plugin Creator v0.0.1 release remains out of date until reconciled.

## Owner-runner CI results — 2026-10-29

- **Commit tested:** `021b7b8552776e0c14db6207292300ff22a43159`.
- **Actual GitHub Actions run:** https://github.com/vixttha/Color-Team-OPS/actions/runs/40982601391 — conclusion **SUCCESS**, both jobs successfully assigned to the named registered runners.
- **Windows:** `color-team-ops-windows-01`, 25 tests, all passed; checkout, test, cleanup and job completed successfully.
- **Linux:** `color-team-ops-linux-01`, 25 tests, all passed; checkout, test, cleanup and job completed successfully.
- **Both jobs:** checked exact commit SHA and runner identity; GitHub token had read-only repository contents permissions. The dependencies used for tests are developer-only; no application service was installed.
- These results validate **source contracts, workflow policy, regression checks and package structure** only. They do not prove live browser skill behavior or authenticate arbitrary claims of external test evidence.
- This is a **prior successfully tested source revision**; if acceptance documentation changes after it, the new final SHA must also pass CI. Record final run details in the PR discussion before promotion.

The original GitHub-hosted CI provisioning problem is a historical issue only; per ADR-0002, the owner chose their connected runners for v0.0.1 release verification. This changes no runtime product law.

## Package creation and ChatGPT registry verification — 2026-10-29

**Exact installed portable source revision:** `52b4160c8246e3ada245fe15c8d2657972118386`. Canonical private Plugin Creator ID: `plugins_6ae3edf1ea4c819182f275592273e2cc`, release ID: `pluginrel_6ae3edf2a4ec8191b5cf9c92c317db22`, version `0.0.1`; URL: https://chatgpt.com/plugins/plugins_6ae3edf1ea4c819182f275592273e2cc.

**Real GitHub Actions run:** [40983579901](https://github.com/vixttha/Color-Team-OPS/actions/runs/40983579901) on above SHA. **Windows SUCCESS, Linux SUCCESS, 25/25 tests on each.** Linux built two `git archive` ZIPs and verified their byte equality, ZIP CRC/content and SHA command with a successful job.

**Private portable package:** 26 uploaded source files, deterministic `SHA-256 8fa207a624a47db3fe52a099e60b61a56c81a7fcb9c3af3e8a4853e54129179d`. Plugin Creator confirms 27 current files including the generated Codex compatibility overlay. **25/25 corresponding plugin/GitHub source files byte-exact**; package README deliberately differs from repository README; generated overlay is expected.

**ChatGPT registry test:** `skills__list` exposed **12/12 Color Team OPS roles**, and `skills__read` successfully read all 12 with frontmatter and the cloud-only requirement; Mission Control, OPS Director and Verification Gate were also individually inspected for safe authority/evidence boundaries.

**Limitations:** No full end-to-end user-initiated skill mission has been performed, no automatic cloud worker exists, no Kimi/Z.ai/Grok host import verified, and no external independent reviewer has been requested. The owner explicitly authorized assistant-led review. Previous GitHub-hosted failures in earlier documentation are historical and superseded by ADR-0002; they must not be mistaken for the current successful runner tests.

**Record-only commit note:** This paragraph and README/CHANGELOG updates change the repository revision beyond the source SHA that was packaged. The unchanged 25 installed-source blobs remain identical; the follow-up CI run on the record commit is required for final-revision hygiene.

## Full-repository audit evidence (latest verified pre-audit revision)

- **Exact source SHA:** `5d7e723e43d5dab66c82402aafb01d213bd6ed29`; [GitHub Actions run 40986689600](https://github.com/vixttha/Color-Team-OPS/actions/runs/40986689600).
- **Windows:** 28/28 Python tests PASS, confirmed from actual job log (`Ran 28 tests`; `OK`; exact SHA PASS marker).
- **Linux:** 28/28 Python tests PASS, confirmed from actual job log. Both exact-SHA ZIP builds and archive checks completed successfully.
- **Portable canonical private plugin:** 25/25 comparable source files byte-match approved packaged source `52b4160c8246e3ada245fe15c8d2657972118386` (two package-specific manifest/README exceptions explained elsewhere).
- **Creator library:** the old draft still appears in metadata and the owned-plugin inventory despite owner report of UI deletion; its backend deletion is NOT VERIFIED. Canonical remains unchanged.
- **Complete audit and open gates:** [v0.0.1 full repository audit](audits/v0.0.1-full-repository-audit-2026-10-29.md). Running 28 passing structural tests does not demonstrate live specialist mission quality.
- This evidence applies to the **pre-audit** source revision; re-check GitHub Actions for the new audit-record commit.
