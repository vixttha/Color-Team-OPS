# Idea + Feature Library — v0.0.2 development candidate

**Status: unreleased v0.0.2 development candidate. Optional side template; NOT a Color-Team-OPS product release, a Governance dependency, or independently accepted for unrelated adopters.**

The frozen [v0.0.1 branch](https://github.com/vixttha/Color-Team-OPS/tree/idea-feature-library-v0.0.1) remains the comparison baseline. See the [six-team one-lane audit](docs/V002-SIX-TEAM-ONE-LANE-AUDIT.md) for confirmed source findings, development patches, missing executed test receipts and release gates.

This branch contains exactly two portable record libraries:

- [Ideas](ideas/README.md): possibilities, pros/cons, reasons, exploration, and human decisions.
- [Features](features/README.md): stable capability identities, implementation status, scoped evidence, and references to ideas.

A human can use the files directly in GitHub. An LLM can read and suggest edits by following [the agent guide](LIBRARY-AGENT-GUIDE.md). No plugin, Governance installation, cloud service, runner, Python, or local environment is required to *use the records*.

**Starts empty.** `ideas/records/` and `features/records/` intentionally contain no project-specific ideas or features. Example documents in `templates/` are examples only, never canonical records. The source Color-Team-OPS library's 36 ideas and 5 candidate features are *not* included in this portable template.

## Quick use (GitHub website only)

1. Copy `ideas/`, `features/`, **and `templates/` if following the examples below** into an isolated, collision-free location in your repository. The agent guide is optional. Never overwrite existing paths. See [adoption instructions](docs/ADOPTION.md).
2. For a new idea, copy [the example](templates/idea.example.json) into `ideas/records/IDEA-000001.json`, edit its ID, title, and facts. For a new feature, use [the feature example](templates/feature.example.json) at `features/records/FEAT-000001.json`. Use the next unused ID, never recycle an ID.
3. Link features to existing ideas by `idea_ids`; keep decisions, implementation, tests, and release claims separate.
4. Edit or regenerate `INDEX.md` as a **read-only view** of records; records always prevail if an index becomes stale. An optional standard-library-only Python helper can validate and generate indexes, but is *not required*.

Run optional checks when Python happens to be available: `python tools/library.py check`, `python tools/library.py build`, `python -m unittest discover -s tests -v`. Copy `tools/` and `tests/` if those helpers are wanted. **v0.0.2 adds count-neutral populated-adopter tests, a bounded validator, local `maxLength` schema support and read-only `python tools/adopter.py <host-library-root>` no-clobber planning.** Starter publishers can also use `python tools/library.py check --expect-empty`; do **not** apply that flag to populated adopters.

[One-lane ChatGPT + owner GitHub runner contract](docs/V002-ONE-LANE-SELFHOSTED-PIPELINE.md) is an optional development/test workflow, never a runtime dependency. The pinned one-shot CI pipeline must not be used to imply an independent human/security audit.

## One-way Governance isolation

[The one-way boundary contract](docs/ONE-WAY-BOUNDARY.md) prohibits a Governance-Branch dependency on this side template, upstream registration, automatic synchronization, and overwriting Governance-owned `ideas/` or `features/` paths. The template may know the concept of Governance but cannot make Governance know it exists.

## Authority and trust

An idea is not approval to implement. A feature record is not permission to run a tool, proof of test success, or evidence of release. This library never supersedes project owner decisions, `AGENTS.md`, code owners, protected branches, official release records or external acceptance gates.

Only an actual project's release authority can assert shipped versions. The template's `release_membership` field must stay `NOT_ASSERTED`. Evidence references and SHAs are *claims to independently check*, not authenticated receipts.

## Read next

- [Library agent guide](LIBRARY-AGENT-GUIDE.md)
- [Lifecycle and state meanings](docs/LIFECYCLE.md)
- [Zero-install adoption](docs/ADOPTION.md)
- [Isolation / threat boundaries](docs/ISOLATION.md)
- [Provenance and source separation](docs/PROVENANCE.md)

Development target: `0.0.2` (**not released**); frozen baseline: `0.0.1`. Neither is an adopting project's product version.
