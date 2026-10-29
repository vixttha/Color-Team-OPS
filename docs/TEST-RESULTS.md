# Pre-release validation

The following are checks of the **package itself**, not claims of a live cloud service: strict JSON parsing, JSON schema self-check, sample validation, skill frontmatter, role cardinality, local-dependency prohibition, ZIP integrity, archive reproducibility. Tests run on an ephemeral hosted build environment; runtime does not require this environment or any user-owned machine.

Actual browser host acceptance, persistent event handling, verified remote GitHub writes, and other-host imports remain NOT TESTED until those specific capabilities are connected.

## Cloud CI and hygiene extension

A GitHub-hosted CI matrix, optional manual self-hosted workflow, executable policy checks, and design documents are being added to the v0.0.1 draft branch. Actual CI PASS must be recorded for the final SHA from GitHub run evidence; otherwise this remains PENDING.

The successful runner-acceptance workflow on the separate runner-audit branch did not verify this release candidate. The Plugin Creator release was created before these GitHub-only changes and is not automatically synchronized.
