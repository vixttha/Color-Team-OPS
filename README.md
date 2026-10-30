# Purple Feature & Idea Library — Color-Team-OPS example

**Status:** Optional, isolated, human-readable and LLM-readable research/development library. **Not a dependency of the Color-Team-OPS plugin, Head mission engine or v0.0.2 release.** This branch preserves the original 36 Color-Team-OPS idea records, five umbrella feature proposals and their historical source provenance.

## Browse
- [36 ideas](ideas/INDEX.md) — opportunities, drawbacks, relationships and source decision state
- [5 feature candidates](features/INDEX.md) — broad capability bundles, **not the count of implemented product functionality**
- [Current dated evidence / 36-idea synergy and conflict audit](docs/IDEA-FEATURE-SYNERGY-CONFLICT-AUDIT-2026-10-30.md) — do not confuse the older proposal status with live engineering
- [LLM + human reading guide](LIBRARY-AGENT-GUIDE.md)
- [Standalone reusable starter](portable/README.md) — use the empty catalog and generic schemas; **do not copy these 36 example records into an unrelated project**
- [Portability and product isolation](docs/PORTABILITY-AND-ISOLATION.md)

## How to use this optional library
Read `ideas/INDEX.md`, `features/INDEX.md` and the dated audit. For a specific concept, open the original JSON record. Cross-check live engineering state from its exact GitHub branch+SHA; source snapshots may be stale. Discuss pros/cons, combinations, conflicts and approval boundaries. Proposed records never authorize work, team dispatch, merge, budget spend or publication.

Color-Team-OPS runtime **must work when `ideas/`, `features/`, `portable/` and these research docs are completely absent**. The master v0.0.2 candidate currently contains copied proposal records, but that is historical integration provenance, not evidence they must ship or execute. Exclude this optional library from the final runtime package unless the owner separately approves it, and test absence.

## Provenance guard
The existing idea records intentionally retain `captured/adopted`, `not_planned`, `untested` **as the status of the original proposal import**. This is not a live implementation index: the team registry, host prototype, router, and evaluation scaffold have advanced on other branches. The current audit documents these differences without rewriting approval or test history. A human owner decides approval, and verified source evidence—not text assertions—supports implementation/testing/release states.

No Python, external account, cloud vendor, GitHub Actions runner, plugin, or local execution environment is needed to read, copy or edit the JSON/Markdown library. Existing `tools/` scripts are optional developer helpers and currently contain **project-specific assumptions**; use `portable/` for a blank reusable format.
