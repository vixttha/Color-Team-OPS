# Clean PrismCell v0.0.1 workcell starter

This starter is **project-neutral**. It renders `TEAM-WORKBENCH/` for every configured team and an installation manifest. It is an offline *document provisioning utility*, not an agent host or an installed runtime dependency.

## New project, no existing history

1. Copy the `PRISMCELL/core/`, `PRISMCELL/tools/initialize-project.mjs` and `PRISMCELL/config/example.json` sources at a reviewed exact source commit.
2. Replace `project_id`, `repository`, `repository_url` and every team/branch/INCALL issue mapping with **real** details of the new project. Every team may have different names and branches. Provision the GitHub branches/issues separately; no provider resources are created by the offline renderer.
3. For a temporary development test workspace only, use `node PRISMCELL/tools/initialize-project.mjs --config <project-config.json> --out <new-empty-output-folder> --source-sha <40-char-reviewed-sha>`. This requires Node only to generate files; once committed to GitHub, workcell operation is through ChatGPT+GitHub without a required owner-computer runtime.
4. Confirm `MANIFEST.json` lists the exact intended home branches. Create each branch from a clean project baseline and add **only its own** rendered `TEAM-WORKBENCH/` files; never merge other agent history, the entire source tree or development runner workflows.
5. Verify the actual branch HEAD, open canonical issue, source pin, permissions, inbox/comment evidence and compare-and-swap behavior **before** changing `BOOTSTRAPPED_PENDING_LIVE_VERIFICATION` to `READY_ON_INVOCATION`. Offline generated documents **never** assert completed provider verification.
6. Run the local schema/installer regression tests on the owner's authorized development machines if available. This is optional, never a required production service.

## Project reuse compatibility

This v0.0.1 distribution supports **GitHub repository plus manual GitHub Issues transport**, 1–50 named workcells and source-pinned on-demand Head workflows. Non-GitHub providers, autonomous dispatch, separately authenticated specialist principals and enforced per-branch scopes are not shipped or certified. The consumer must supply real provider evidence and authority controls.

The `PRISMCELL/config/color-team-ops.json`, `PRISMCELL/tools/guard.mjs`, legacy `PRISMCELL/schemas/` and existing Color-Team-OPS agent branches are **not** generic starter payloads.
