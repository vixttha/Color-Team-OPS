# Release process and repository hygiene

## Every version

1. Work in a narrow PR branch, review diff and maintain exact-SHA evidence. Never force-push an accepted revision.
2. Keep the root plugin.json and compatibility manifest versions identical. If the plugin version changes, align all version references.
3. Update README.md and CHANGELOG.md **every release** with functionality, limitations, host compatibility, runner policy and review status.
4. Update docs/TEST-RESULTS.md with the final SHA, workflow run URLs and evidence; adjust architecture, decision and portability docs as needed.
5. Require GitHub-hosted Ubuntu and Windows CI success on the release candidate SHA; optional self-hosted tests can augment but never replace or block this gate.
6. Run independent security and code review, resolve issues, and test real plugin behavior where supported. Do not equate package validation with operational acceptance.
7. Reconcile the installed private plugin version and source with the intended repository revision. GitHub-only changes do not silently update Plugin Creator's installed package.
8. Obtain release approval before marking a PR ready, merging or announcing acceptance.

## Hygiene

Use CODEOWNERS, .editorconfig, .gitattributes, .gitignore, CONTRIBUTING.md and SECURITY.md. Never commit secrets, personal machine paths, unnecessary binaries, generated caches or undocumented changes. CODEOWNERS does not itself enable required PR reviews or branch protection; GitHub repository rulesets need separate settings.

## Trusted CI

The cloud baseline on pull requests/main has read-only permissions, immutable checkout SHA, and no user-runner requirements. The optional personal-runner workflow is manual on trusted main only. See [locked runner policy](design/RUNNER-POLICY.md).

The installed plugin's use must remain unaffected by CI, runner availability or any local tooling.
