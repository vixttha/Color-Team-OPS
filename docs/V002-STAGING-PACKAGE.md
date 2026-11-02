# Approved private staging package (development only)

Owner permitted **exactly one PRIVATE v0.0.2 staging plugin identity** in Issue #8 comment 6590306287. Canonical v0.0.1 `plugins_6ae3edf1ea4c819182f275592273e2cc` must be unchanged. No main merge, release, public sharing, paid host or production tool grants.

Builder `devtools/build_v002_staging.py` starts from an actual complete Git-tree-verified 32-file source ZIP; changes only `plugin.json`, `.codex-plugin/plugin.json` and regenerates `RELEASE-SOURCE-MANIFEST.json`. All twelve SKILL.md and nine competency reference bytes are unchanged. Staging slug is `color-team-ops-v002-staging`, displayName `Color Team OPS v0.0.2 STAGING — NOT RELEASED` (separate from the canonical identity).

A branch-scoped Linux development workflow, pinned third-party GitHub actions and one-day artifact retention are used to retain a ZIP from the exact SHA that passed all native tests. CI ZIP hash is not an installed plugin hash; GitHub artifact wrapper ZIP may be an additional archive layer. Verify the inner source/staging ZIPs and manifests independently before passing an **absolute local archive path** to Plugin Creator; do not pass URLs or arbitrary GitHub file references to `create_plugin`.

**Safety:** If connector/tool boundaries cannot materialize the true ZIP to an absolute local file, stop only the staging creation. Never fabricate a path or issue duplicate plugin creation calls. The user, not this agent, deletes the test plugin. Provider rename method must be verified before attempting.
