# Pre-release validation

The following are checks of the **package itself**, not claims of a live cloud service: strict JSON parsing, JSON schema self-check, sample validation, skill frontmatter, role cardinality, local-dependency prohibition, ZIP integrity, archive reproducibility. Tests run on an ephemeral hosted build environment; runtime does not require this environment or any user-owned machine.

Actual browser host acceptance, persistent event handling, verified remote GitHub writes, and other-host imports remain NOT TESTED until those specific capabilities are connected.
