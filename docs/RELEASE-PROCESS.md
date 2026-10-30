# Release process and repository hygiene

## Single-canonical-plugin guard — required before every Plugin Creator operation

1. Read `docs/PLUGIN-RELEASE-REGISTRY.json` and `docs/decisions/ADR-0003-canonical-plugin-identity.md`, then verify the **existing canonical plugin ID** with the Plugin Creator live read APIs.
2. Before create/update, confirm exact source SHA and existing version. If a Creator update will auto-increment the version, stop instead of making a second same-name plugin; get **explicit owner approval** for a new version or replacement.
3. If the registry lists a superseded plugin, label it `superseded_still_installed` until a permitted uninstall succeeds; keep **actual uninstall evidence** before claiming it has been retired.
4. After update/release, verify every portable installed file and all twelve skills; record canonical plugin ID, exact Creator release ID, GitHub revision, ZIP digest, real test run and supported-host limitations.
5. Treat any duplicate-identity ambiguity or unverified installed state as a release blocker. Never mark a plugin `retired_uninstalled` based only on its README or this registry.
6. Update README and CHANGELOG for every version; never modify the accepted v0.0.1 package silently. This governance guard is for release work, not installed-plugin runtime.

## Every version

1. Work in a narrow PR branch, review diff and maintain exact-SHA evidence. Never force-push an accepted revision.
2. Keep the root plugin.json and compatibility manifest versions identical. If the plugin version changes, align all version references.
3. Update README.md and CHANGELOG.md **every release** with functionality, limitations, host compatibility, runner policy and review status.
4. Update docs/TEST-RESULTS.md with the final SHA, workflow run URLs and evidence; adjust architecture, decision and portability docs as needed.
5. For v0.0.1, verify real GitHub Actions jobs executed on the owner's specifically authorized Windows and Linux test runners at the exact candidate SHA. The installed plugin never depends on those tests or machines.
6. Run the assistant's evidence-based Red/Purple/White audit as the owner requested, resolve issues and test real plugin behavior where supported. An outside independent reviewer is optional. Do not equate package validation with operational acceptance.
7. Reconcile the installed private plugin version and source with the intended repository revision. GitHub-only changes do not silently update Plugin Creator's installed package.
8. Obtain release approval before marking a PR ready, merging or announcing acceptance.

## Hygiene

Use CODEOWNERS, .editorconfig, .gitattributes, .gitignore, CONTRIBUTING.md and SECURITY.md. Never commit secrets, personal machine paths, unnecessary binaries, generated caches or undocumented changes. CODEOWNERS does not itself enable required PR reviews or branch protection; GitHub repository rulesets need separate settings.

## Trusted CI

The v0.0.1 runner test workflow has read-only permissions and uses only a controlled source branch, not untrusted pull-request code; its purpose is development/release verification only. See [ADR-0002](decisions/ADR-0002-ci-runner-choice.md). See [locked runner policy](design/RUNNER-POLICY.md).

The installed plugin's use must remain unaffected by CI, runner availability or any local tooling.
