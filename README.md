# Color Team OPS — v0.0.1 (cloud-only)

A **skills-only** private plugin intended for browser-accessible AI platforms. Twelve skills: nine specialist teams, OPS Director, independent Verification Gate procedure, and Mission Control. **No local hardware, local executor, desktop app, self-hosted runner, or GitHub Actions job is necessary for installation or basic skill workflows.**

**Important:** v0.0.1 provides portable role instructions, evidence contracts, and bounded in-session routing guidance; it **does not** run a 24/7 autonomous process, host an MCP server, authenticate a real security verifier, invoke GitHub on its own, or guarantee cross-platform installs. For actual repo changes a user must separately connect a cloud-capable GitHub app with the required permissions in their chosen host.

Hard laws: [docs/CONSTITUTION.md](docs/CONSTITUTION.md). Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Cross-host expectations: [docs/PORTABILITY.md](docs/PORTABILITY.md). Acceptance: [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md).

This repository tracks version source; the `runner-audit/2026-10-29` branch is NOT a runtime dependency and is deliberately not used. No runners are invoked as part of plugin operation.

Run a mission by invoking **mission-control** with a bounded, authorized goal, then **ops-director** to recommend the next eligible skill. Other skills remain individually invocable. Host tools and permissions must be checked, never assumed. Skills can explain what to do without a connected service. Completing tasks or persistent unattended dispatch requires host support that v0.0.1 does not provide.
