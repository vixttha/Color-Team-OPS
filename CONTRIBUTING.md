# Contributing

Use reviewable branches and narrow PRs; explain exact source SHA, scope, risk, test evidence, what was not tested, and version impact. Never commit passwords, personal data, private logs, local machine paths or unpublished credentials.

Every new version MUST update README.md, CHANGELOG.md, docs/TEST-RESULTS.md and affected design docs. Follow [release process](docs/RELEASE-PROCESS.md) and [runner policy](docs/design/RUNNER-POLICY.md).

For v0.0.1 the owner has authorized GitHub Actions tests on the registered Windows/Linux self-hosted runners; the trusted version branch is the only trigger. This choice never turns development runners into installed plugin infrastructure. Do not test untrusted PR code.

The CODEOWNERS file expresses review ownership; protections and required reviews need separate GitHub ruleset settings.
