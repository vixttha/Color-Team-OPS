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

**Release CI is not plugin runtime.** GitHub-hosted Linux/Windows validation is the mandatory repository release baseline; owner runners are opt-in supplemental validation only. The cloud baseline must pass with both personal runners offline. No untrusted PR code is permitted on personal runners.

Canonical law: [Constitution](docs/CONSTITUTION.md), [Runner policy](docs/design/RUNNER-POLICY.md), [ADR-0001](docs/decisions/ADR-0001-runner-separation.md).

## Versions and repository hygiene

**Every version must update this README, CHANGELOG.md, exact-SHA test evidence, and the affected design and compatibility documentation.** Changes are reviewed in PRs; no secret material, opaque build outputs, local machine paths, automatic merges, or unverified green status.

See [Changelog](CHANGELOG.md), [Release process](docs/RELEASE-PROCESS.md), [Contributor rules](CONTRIBUTING.md), [Security](SECURITY.md), [Architecture](docs/ARCHITECTURE.md), [Portability](docs/PORTABILITY.md), [Acceptance](docs/ACCEPTANCE.md) and [Test evidence](docs/TEST-RESULTS.md).

## CI structure

- Mandatory GitHub-hosted Ubuntu/Windows matrix: .github/workflows/cloud-ci.yml (PRs to main and pushes to main).
- Optional owner Windows/Linux: .github/workflows/optional-self-hosted.yml (manual workflow_dispatch, trusted main only, explicit opt-in, never a required check).
- Developer convenience only: python -B -m unittest discover -s tests -p "test_*.py" -v. Running this on your own computer is never a requirement for installing or using the plugin.

## Basic usage

Invoke mission-control with a bounded authorized goal, then ops-director to select one permitted team. Skills are individually usable. Completion claims without authenticated evidence remain UNVERIFIED. Actual cloud source changes require an independently authorized connected cloud tool.

Host compatibility on chatgpt.com, kimi.ai, z.ai, grok.com and other browser services must be separately verified. See portability guidance. A ChatGPT private plugin is not automatically installed elsewhere.

## Security hardening in the v0.0.1 draft

Orange/Yellow added cross-field mission authorization, evidence provenance and routing constraints. Red/Purple added Draft 2020-12 adversarial cases and parsed GitHub Actions workflow policy and mutation tests. These are source-level controls, not an independently authenticated cloud runtime.

The required GitHub-hosted CI remains blocked **before runner assignment** ([issue #2](https://github.com/vixttha/Color-Team-OPS/issues/2)); cloud-only independent tests are supplemental evidence, not GitHub CI PASS. The installed private v0.0.1 plugin **does not yet contain the updated contracts and governance docs**. Plugin Creator requires an actual release update, which may advance the version; do not silently promote a new version during v0.0.1 review.

See [contract trust boundaries](docs/CONTRACT-TRUST-MODEL.md), [test coverage](docs/TESTING.md), and [Purple Team review issue #3](https://github.com/vixttha/Color-Team-OPS/issues/3).

The [five-team execution and release-gate audit](docs/audits/v0.0.1-five-team-execution.md) records the evidence and remaining blockers; no internal audit is represented as an independent approval.

## Current status

The private plugin v0.0.1 was created before the new CI and README work. GitHub changes do not update that installed package automatically. Draft [PR #1](https://github.com/vixttha/Color-Team-OPS/pull/1) remains unmerged; cloud CI, live skill acceptance, review and plugin/source reconciliation must be recorded before release approval. GitHub-hosted CI is currently **BLOCKED before any test step** ([issue #2](https://github.com/vixttha/Color-Team-OPS/issues/2)); personal runners must not replace its baseline.
