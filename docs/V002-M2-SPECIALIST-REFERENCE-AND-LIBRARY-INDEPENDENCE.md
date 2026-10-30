# Issue #8 / M2 Yellow: specialized team-reference packs, optional-library independence

**Development source:** `integration/v0.0.2-master-single-thread`. **Scope:** existing nine specialists + three coordination skills. No new team and no production permission.

One specialist competency reference is added for each of Yellow, Orange, Green, Red, Blue, Purple, White, Black, and Gray Cell. They give four grounded role/specialization examples, activation/exclusion criteria, source-bound evidence requirements, cross-team division of labor and a Head-controlled return contract. The nine existing specialist `SKILL.md` files remain exactly v0.0.1; only the existing OPS Director coordinator is amended to **load the selected team's reference pack lazily** when the supported ChatGPT host actually exposes it. Role descriptions do not create tool permission or authenticated identity.

The optional Purple Idea/Feature Library remains an isolated research companion. The master candidate contains 36 historical ideas and five candidate feature umbrellas, but the core directory/router modules must not **read or require** those files. `tests/test_v002_optional_library_independence.py` adds six **authored, not yet natively executed** tests: exact nine reference paths, evidence and exclusion guidance, deterministic directory search with optional-library reads forcibly blocked, one-team advisory routing with those reads blocked, skill count and coordinator lazy loading.

No installed-plugin trial has demonstrated that ChatGPT can open these references yet. No developer-runner or paid cloud infrastructure was invoked, and no special provider is required.

**Validate gate:** source parity and six authored cases need exact-SHA native testing; real supported-host playbook loading is still `UNVERIFIED`. **Internal Auditor:** verify privacy, prompt injection, no auto-grants, role overlap and failure behavior. **Head:** must not mark M2 release-complete on file presence alone.
