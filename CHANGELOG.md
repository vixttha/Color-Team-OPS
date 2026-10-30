# Changelog

Newest version first. Every version updates README.md, this changelog, acceptance evidence and relevant architecture documents.

## [0.0.1] — Draft; release acceptance incomplete

### Added
- Nine color-team roles plus OPS Director, Verification Gate and Mission Control (12 skills).
- Cloud-only constitution, cross-host portability notes, contracts and examples.
- v0.0.1 owner-authorized Windows/Linux GitHub self-hosted release tests, confined to the trusted v0.0.1 branch.
- The plugin and any future cloud backend remain independent of those developer runners.
- Design-stage runner policy and accepted ADR-0001.
- README-per-version rule, evidence-backed assistant audits and repository hygiene files.

### Hardened on draft branch (not yet installed)
- Mission and evidence JSON Schema Draft 2020-12 cross-field requirements, disallowing incomplete OBSERVED/PASS and branch-write claims.
- Adversarial negative-schema regressions, semantically parsed workflow policy, and CI mutation tests.
- Cloud-only development test dependencies, explicitly absent from installed skill runtime.
- Corrected preflight evidence so source/installed package divergence remains clearly visible.

### Corrected CI and review policy
- ADR-0002 supersedes the mandatory GitHub-hosted baseline portion of ADR-0001. Hosted CI startup failures are historical and no longer the chosen test path for this release.
- The owner selected the assistant to audit this release; outside independent review is not a prerequisite.

### Outstanding
- Real successful Windows/Linux runner tests on the final version source SHA and complete assistant audit.
- Real installed-plugin skill acceptance, host integrations and plugin/repository source reconciliation.
- Persistent autonomous cloud execution is not part of the skills-only v0.0.1 release.

The already-created Plugin Creator v0.0.1 release predates these GitHub-only maintenance changes. GitHub changes are not automatically installed.
