# Locked design policy — Cloud-only runtime and optional runners

**Status: ACCEPTED. Effective: 2026-10-29. Scope: all product versions and integrations.**

> **Binding product law (verbatim):** Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate.

## Constitutional distinction

Repository release infrastructure and installed-plugin runtime are separate systems. All necessary plugin functions MUST work through supported browser-accessible platforms and authorized cloud services without user-owned compute, local daemons, local databases, localhost or owner-managed GitHub runners. This rule also applies to any future autonomous cloud backend.

| Activity | Owner runners | Binding condition |
| --- | --- | --- |
| Running development tests | Allowed | Optional only |
| Performing independent audits | Allowed | Optional, and independence must be evidenced |
| Validating plugin packages | Allowed | Optional only |
| Testing releases | Allowed | The owner chooses whether to use them for a release; never required by the installed plugin |
| Running the installed Color Team OPS plugin | Never required | No runtime dependency |
| Powering its autonomous operations | Never required | Cloud-managed infrastructure only |
| Serving as its database or cloud backend | Never required | Cloud-managed state only |

## Release CI — v0.0.1 owner decision

For v0.0.1 the owner explicitly authorized executing tests and this assistant's audits using the registered Windows and Linux GitHub self-hosted runners. The version-scoped workflow runs only on the controlled `release/v0.0.1-cloud-only` branch, uses read-only GitHub permissions, pinned checkout and a clean checkout at the exact event SHA. It has no PR, fork, `pull_request_target` or `workflow_run` trigger and no secrets.

This choice is part of how **developers verify the release**, not a condition for **using the installed plugin**. No cloud-hosted CI requirement remains for v0.0.1; the earlier selection is superseded by ADR-0002. This selected development runner test path may fail if the owner's runners go offline, but the plugin must continue to function without them.

GitHub self-hosted runners can be compromised by untrusted code and cannot be treated as ephemeral clean environments. Never dispatch untrusted pull request source to persistent owner machines. A reviewer must understand the trusted main code before manually triggering this workflow.

## Enforcement and governance

Automated tests verify the boundary, authorized v0.0.1 workflow, version alignment and README policy. [ADR-0002](../decisions/ADR-0002-ci-runner-choice.md) supersedes ADR-0001 only on CI provider/mandatory external-review selection; the permanent cloud-only product law is unchanged. Future CI choices require an explicit owner decision and updated regression tests.

Every version updates README.md, CHANGELOG.md, evidence files and affected design docs before release promotion. See [release process](../RELEASE-PROCESS.md).
