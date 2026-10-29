# Contributing

Use reviewable branches and narrow PRs; explain exact source SHA, scope, risk, test evidence, what was not tested, and version impact. Never commit passwords, personal data, private logs, local machine paths or unpublished credentials.

Every new version MUST update README.md, CHANGELOG.md, docs/TEST-RESULTS.md and affected design docs. Follow [release process](docs/RELEASE-PROCESS.md) and [runner policy](docs/design/RUNNER-POLICY.md).

GitHub-hosted CI is the mandatory release baseline. Running Python tests on a developer's computer is optional convenience only. Owner Windows/Linux runners are strictly manual supplements and must never execute untrusted PR code.

The CODEOWNERS file expresses review ownership; protections and required reviews need separate GitHub ruleset settings.
