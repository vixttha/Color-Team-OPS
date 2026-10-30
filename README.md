# Color Team OPS

**Current version: v0.0.1 — private skills-only ChatGPT release accepted; interactive missions not verified, GitHub PR #1 still draft.**

Color Team OPS is a cloud-only, browser-first plugin providing nine specialist color teams and three coordinating skills (12 total). v0.0.1 provides portable instructions and evidence contracts; it does not provide an unattended cloud runtime, autonomous GitHub writing, a hosted MCP service, or verified installation on every browser LLM host.

## Locked cloud-only design law

> Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate.


Neither plugin use nor future autonomous cloud operations may require an owner's PC, desktop tools, local services, a locally managed database, or GitHub self-hosted runners.

| Activity | Owner's GitHub runners |
| --- | --- |
| Running development tests | Allowed, optional |
| Performing independent audits | Allowed, optional |
| Validating plugin packages | Allowed, optional |
| Testing releases | Allowed, optional |
| Running the installed Color Team OPS plugin | Never required |
| Powering its autonomous operations | Never required |
| Serving as its database or cloud backend | Never required |

**Release CI is not plugin runtime.** For v0.0.1, the owner explicitly authorized running the release tests on the registered Windows and Linux GitHub self-hosted runners. The plugin remains usable when those runners are off or unregistered. No untrusted pull-request code may run on personal machines. The earlier GitHub-hosted-only CI policy has been superseded by ADR-0002.

Canonical law: [Constitution](docs/CONSTITUTION.md), [Runner policy](docs/design/RUNNER-POLICY.md), [ADR-0001](docs/decisions/ADR-0001-runner-separation.md).

## Canonical plugin identity and version safety

**Canonical ChatGPT v0.0.1:** [Color Team OPS](https://chatgpt.com/plugins/plugins_6ae3edf1ea4c819182f275592273e2cc), plugin ID `plugins_6ae3edf1ea4c819182f275592273e2cc`, release `pluginrel_6ae3edf2a4ec8191b5cf9c92c317db22`, packaged GitHub source SHA `52b4160c8246e3ada245fe15c8d2657972118386`.

**OLD DRAFT — DELETE MANUALLY:** `plugins_6ae3ccf13f548191bdcba269f33085d3` has the visible label **"OLD Color Team OPS - DELETE"**. The old draft was updated to its own version `0.0.2` for this label change **without changing the canonical project's v0.0.1 release**. Its Plugin Creator record **still exists**: the exact-ID uninstall action returned `not_installed`, which only applies to the installed connection, not removal of the Creator record. The owner has explicitly authorized deletion, but the current Plugin Creator connection exposes **no delete-record action**. Use the private-plugin management UI to remove **only** the old ID; do not touch canonical `plugins_6ae3edf1ea4c819182f275592273e2cc`. [Cleanup issue #5](https://github.com/vixttha/Color-Team-OPS/issues/5) stays open pending confirmed deletion.

[ADR-0003](docs/decisions/ADR-0003-canonical-plugin-identity.md) and the [identity registry](docs/PLUGIN-RELEASE-REGISTRY.json) lock a single canonical plugin ID. Future versions must use the same ID or stop for an explicit identity/version decision; never silently duplicate a private plugin or bump SemVer.

## Versions and repository hygiene

**Every version must update this README, CHANGELOG.md, exact-SHA test evidence, and the affected design and compatibility documentation.** Changes are reviewed in PRs; no secret material, opaque build outputs, local machine paths, automatic merges, or unverified green status.

See [Changelog](CHANGELOG.md), [Release process](docs/RELEASE-PROCESS.md), [Contributor rules](CONTRIBUTING.md), [Security](SECURITY.md), [Architecture](docs/ARCHITECTURE.md), [Portability](docs/PORTABILITY.md), [Acceptance](docs/ACCEPTANCE.md) and [Test evidence](docs/TEST-RESULTS.md).

## CI structure

- **Authorized v0.0.1 verification:** `.github/workflows/v0.0.1-runner-ci.yml` runs Linux and Windows tests only on the dedicated v0.0.1 release branch, with read-only GitHub credentials and pinned source revision.
- **No GitHub-hosted requirement:** GitHub-hosted jobs are not required for v0.0.1. This testing choice is version-specific, not a dependency of the plugin.
- [ADR-0002](docs/decisions/ADR-0002-ci-runner-choice.md) supersedes the CI-selection portion of ADR-0001.
- Developer convenience only: python -B -m unittest discover -s tests -p "test_*.py" -v. Running this on your own computer is never a requirement for installing or using the plugin.

## Basic usage

Invoke mission-control with a bounded authorized goal, then ops-director to select one permitted team. Skills are individually usable. Completion claims without authenticated evidence remain UNVERIFIED. Actual cloud source changes require an independently authorized connected cloud tool.

Host compatibility on chatgpt.com, kimi.ai, z.ai, grok.com and other browser services must be separately verified. See portability guidance. A ChatGPT private plugin is not automatically installed elsewhere.

## Security hardening in the v0.0.1 draft

Orange/Yellow added cross-field mission authorization, evidence provenance and routing constraints. Red/Purple added Draft 2020-12 adversarial cases and parsed GitHub Actions workflow policy and mutation tests. These are source-level controls, not an independently authenticated cloud runtime.

Historical GitHub-hosted CI failures were superseded by the owner's CI decision (ADR-0002). **A new canonical private ChatGPT plugin v0.0.1 has been created with the hardened contracts and governance source**, without changing the semantic version to v0.0.2. The old draft was relabeled for manual deletion and remains listed in Plugin Creator; only its archival version changed to 0.0.2. This is **not** the canonical product's v0.0.2.

See [contract trust boundaries](docs/CONTRACT-TRUST-MODEL.md), [test coverage](docs/TESTING.md), and [Purple Team review issue #3](https://github.com/vixttha/Color-Team-OPS/issues/3).

The [five-team execution and release-gate audit](docs/audits/v0.0.1-five-team-execution.md) records the earlier review. A fresh v0.0.1 owner-directed audit will use real test evidence; the assistant can audit the work but does not mislabel its own assessment as an external independent review.

## Current status

**Canonical private ChatGPT plugin:** [Color Team OPS v0.0.1](https://chatgpt.com/plugins/plugins_6ae3edf1ea4c819182f275592273e2cc) (ID `plugins_6ae3edf1ea4c819182f275592273e2cc`, release `pluginrel_6ae3edf2a4ec8191b5cf9c92c317db22`). All **12/12 skills are discoverable and readable in ChatGPT**; 25/25 installed portable-source files match GitHub revision `52b4160c8246e3ada245fe15c8d2657972118386` byte-for-byte; the package-specific README and generated compatibility manifest are expected exceptions. Development Windows and Linux runners **both passed 25/25 tests** on `52b4160c8246e3ada245fe15c8d2657972118386` ([run #40983579901](https://github.com/vixttha/Color-Team-OPS/actions/runs/40983579901)), and the Linux ZIP build passed its double-build byte comparison. The v0.0.1 package SHA-256 is `8fa207a624a47db3fe52a099e60b61a56c81a7fcb9c3af3e8a4853e54129179d`. The installed plugin **does not** supply a background orchestrator, independently authenticated remote verifier, or universal browser host integration. Draft [PR #1](https://github.com/vixttha/Color-Team-OPS/pull/1) remains unmerged pending a separate merge authorization; plugin runtime never needs the test runners.
