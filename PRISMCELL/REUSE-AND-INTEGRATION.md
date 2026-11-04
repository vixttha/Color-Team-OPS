# PrismCell v0.0.1 — reusable workcell installation and provider boundary

PrismCell is a reusable **on-demand, one-thread workcell framework** for independent project types (software, writing, games, research) using the supported **GitHub repository + manual GitHub Issues** transport. It does **not** require the owner's PC, a self-hosted runner, a particular deployment host, or a continuously running service in production. `PRISMCELL/core/` contains the generic deterministic logic; `config/color-team-ops.json` and the legacy `tools/guard.mjs` are Color-Team-OPS-specific compatibility references.

## Fresh project installation: clean, no copied agent history

1. Create a separate GitHub project/repository, real home branch for each specialist and real incoming Issue. Choose 1–50 team IDs matching `[A-Z][A-Z0-9_]{1,39}`. Project ID must be a single-line safe identifier matching `[A-Za-z0-9][A-Za-z0-9_.-]{0,99}`; never paste free-form project instructions into this field. These are logical specialist workspaces, not new authenticated GitHub principals.
2. Make a **project-specific** config from `PRISMCELL/config/example.json`: assign `schema_version: prismcell-project-config-0.0.1`, `transport: github-issues-manual`, matching `repository` and `repository_url`, unique team branch names and valid issue URL/number.
3. Generate a clean starter document set with the deterministic, network-free `PRISMCELL/core/starter.mjs` or optional one-shot Node provisioning command:

   `node PRISMCELL/tools/initialize-project.mjs --config project.json --out new-empty-folder --source-sha <reviewed-template-git-SHA>`

   The CLI deliberately refuses an existing destination. Invalid Git branch refs (for example `team/`, `team/.lock`, `team/./x`, `HEAD`) are rejected before writing. It does **not** call GitHub APIs or create branches/issues. `MANIFEST.json` identifies each team's branch and provides SHA-256 digests for **all 17 generated workcell files** per team. No old logs, source trees, activity or claims are copied.
4. Run `node PRISMCELL/tools/verify-manifest.mjs new-empty-folder <reviewed-template-git-SHA> <expected-team-count>` and require a full-file inventory/digest PASS. This detects accidental loss, modification, extra files and symlinks. For hostile modifications, supply the **optional fourth argument** `<trusted-manifest-sha256>` obtained from a separate trusted source. Hashes stored beside files cannot prove authenticity if an attacker can rewrite both manifest and content.
5. For each team, copy only its own `TEAM-WORKBENCH/` files to its already established branch via actual authorized GitHub writes. Never merge unrelated home histories or install test workflows into consumer repositories.
6. HEAD must verify the actual branch SHA, canonical live issue, repo permissions, source SHA, inbound comments and state before changing `BOOTSTRAPPED_PENDING_LIVE_VERIFICATION` to `READY_ON_INVOCATION`. Until those provider observations exist, generated workcells are explicitly **not yet activated**.
7. Session loop: HEAD selects exactly one specialist, reads source/queue/INCALL/ledger, validates untrusted receipts, performs bounded work, then Validate → logical Internal Auditor → HEAD with true evidence and durable handoff. A Python schema test or a source checksum is not a role/permission grant.

## Verified development-test scope

`PRISMCELL/tests/fixtures/nebula-project.json` is an **unowned synthetic second-repository fixture**, with ASTRONOMY/STORY/REVIEW teams; it does not assert a real GitHub repository or issues. The clean-room trial runs in fresh temporary directories with no prior histories. Both Linux and Windows development self-hosted runners may execute it when owner-authorized. Neither becomes a product/runtime dependency. Schema and JS parity are regression-tested for representable constraints; the JS engine additionally enforces **cross-field project/team/issue binding**, which generic JSON Schema alone cannot compare without a trusted external context.

## Explicit limitations

The v0.0.1 project schema intentionally requires GitHub Issues manual transport. Additional providers, agent credential isolation, webhook delivery, background execution and real enforced per-team branch ACLs are **not** shipped or certified. Although the pure logic can be adapted to many project types, describing it as compatible with every provider would be inaccurate.

If a member source is invalid, `validateMessage` must deny it, including inherited JavaScript keys such as `constructor` and `toString`. `intake` never authenticates or grants authority. GitHub file-SHA compare-and-swap remains the host's responsibility, not an in-memory revision claim.

## Schema compatibility and decision history

Canonical JSON Schema files are `PRISMCELL/core/schemas/`; the `PRISMCELL/schemas/` aliases are byte-identical and tested. The original Color-Team-OPS-specific schemas are preserved only at `PRISMCELL/adapters/color-team-ops/legacy-schemas/`, not for new projects. See [SCHEMA-SOURCES.json](SCHEMA-SOURCES.json).

The pure intake engine denies malformed ledgers, mismatched destination message IDs, invalid branch references and forged project-identity Markdown. Its decisions retain append-only `decision_history` records and refuse a second decision on the same message; use a separate Head-reviewed correction record for later changes. A ledger revision is not a substitute for real GitHub CAS, and an `ACKNOWLEDGE` still does not grant permission or certify work.
