# Locked design policy — Cloud-only runtime and optional runners

**Status: ACCEPTED. Effective: 2026-10-29. Scope: all product versions and integrations.**

## Constitutional distinction

Repository release infrastructure and installed-plugin runtime are separate systems. All necessary plugin functions MUST work through supported browser-accessible platforms and authorized cloud services without user-owned compute, local daemons, local databases, localhost or owner-managed GitHub runners. This rule also applies to any future autonomous cloud backend.

| Activity | Owner runners | Binding condition |
| --- | --- | --- |
| Running development tests | Allowed | Optional only |
| Performing independent audits | Allowed | Optional, and independence must be evidenced |
| Validating plugin packages | Allowed | Optional only |
| Testing releases | Allowed | Supplement, never a requirement |
| Running the installed Color Team OPS plugin | Never required | No runtime dependency |
| Powering its autonomous operations | Never required | Cloud-managed infrastructure only |
| Serving as its database or cloud backend | Never required | Cloud-managed state only |

## Release CI

GitHub-hosted Ubuntu and Windows run the mandatory package, policy and workflow validation matrix on pull requests to main and pushes to main. No personal runner label or fallback is allowed in the baseline. The baseline may consume GitHub-hosted minutes for a private repo; that is a release-development cost, not an installed-plugin dependency.

A separate, opt-in workflow may run supplemental Windows/Linux tests on the owner's labeled GitHub self-hosted runners. It MUST use manual workflow_dispatch, explicit affirmative input, trusted main source only, minimal token permissions, no secrets and no automatic PR triggers. It MUST NOT be a prerequisite for cloud CI or release acceptance. If owner runners are absent or offline, only optional supplemental results are unavailable.

GitHub self-hosted runners can be compromised by untrusted code and cannot be treated as ephemeral clean environments. Never dispatch untrusted pull request source to persistent owner machines. A reviewer must understand the trusted main code before manually triggering this workflow.

## Enforcement and governance

Automated tests verify the split, required GitHub-hosted CI, opt-in only supplemental jobs, version alignment and README policy. The canonical decision is [ADR-0001](../decisions/ADR-0001-runner-separation.md). Update through a new explicit owner-approved ADR and independent review, never silent weakening of the cloud-only law.

Every version updates README.md, CHANGELOG.md, evidence files and affected design docs before release promotion. See [release process](../RELEASE-PROCESS.md).
