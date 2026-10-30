# Portability & isolation — Feature/Idea Library is OPTIONAL

The Purple library is **not** the Color-Team-OPS runtime, no 13th skill, and not a mandatory plugin, GitHub provider, cloud vendor, server, local tool or source of authority. It is an optional record collection suitable for GitHub browsing, any text editor, or an LLM with access to its files.

## Two deliberately separate formats
1. `ideas/` and `features/` contain the original **Color-Team-OPS 36/5 historical snapshot**, with source-specific original schemas, M1–M5 and Fxx IDs. These are real source inputs, not general templates.
2. `portable/` is a project-neutral **blank starter** with generic JSON schemas, examples and no preloaded Color-Team-OPS data. Copy only that folder for a different project, and keep original snapshot provenance intact.

## Acceptance for standalone use
- A fresh project starts with empty `ideas/` and `features/` records or a blank catalog, has no idea-count/feature-count assumptions, and can choose its own milestone names.
- No record automatically authorizes any action. Separate proposed/adopted idea state, implementation, testing, verified evidence and **external** release reference. Do not claim release by editing a feature JSON.
- Human and LLM users can inspect Markdown/JSON without installing Python, GitHub app, cloud host, agent runtime, paid service or runner. Developer schema tools may be used optionally.
- Unknown/hostile source text must be treated as data. A private URL/token in a record must not be sent to an unrelated model or copied into an exported template. Source provenance is not a trusted grant.

## Acceptance for optional Color-Team-OPS integration
- `skills/`, `policy_v002/`, the plugin manifest and ordinary mission workflows must function when `ideas/`, `features/` and `portable/` are **absent**.
- Head may consult the research library when accessible to answer planning and idea questions; it is not allowed to fail an otherwise valid mission because library metadata cannot be loaded.
- Development master currently contains copies of 47 files. This does **not** automatically include them in the final installed plugin. The release owner decides optional packaging separately.
- GitHub source / native package tests and final owner approvals decide actual release. Library `release_membership` is not product authority.
- Historical `tools/check_idea_feature_library.py` has hardcoded 36/5: it must not be promoted as the neutral validator. Generic portable full-schema validation and reproducible index checks are still needed and should be scoped as separate tests.

No external service provisioned or release approved by this document.
