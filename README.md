# Color Team OPS

**Development version: v0.0.1 — private skills-only plugin; acceptance incomplete.**

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

Previous GitHub-hosted CI runs failed before runner assignment ([historical issue #2](https://github.com/vixttha/Color-Team-OPS/issues/2)). The project owner has now selected the registered Windows/Linux runners for v0.0.1 development and acceptance tests instead. The installed private v0.0.1 plugin **does not yet contain the updated contracts and governance docs**. Plugin Creator requires an actual release update, which may advance the version; keep version 0.0.1 until the release is ready; do not silently start v0.0.2.

See [contract trust boundaries](docs/CONTRACT-TRUST-MODEL.md), [test coverage](docs/TESTING.md), and [Purple Team review issue #3](https://github.com/vixttha/Color-Team-OPS/issues/3).

The [five-team execution and release-gate audit](docs/audits/v0.0.1-five-team-execution.md) records the earlier review. A fresh v0.0.1 owner-directed audit will use real test evidence; the assistant can audit the work but does not mislabel its own assessment as an external independent review.

## Current status

The private plugin v0.0.1 was created before the new CI and README work. GitHub changes do not update that installed package automatically. Draft [PR #1](https://github.com/vixttha/Color-Team-OPS/pull/1) remains unmerged. Remaining acceptance is actual runner test evidence, the assistant's evidence-based audit, live plugin acceptance and source/plugin reconciliation. Test hardware is never required for plugin use.
