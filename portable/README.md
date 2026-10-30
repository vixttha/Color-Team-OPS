# Portable Feature & Idea Library — empty reusable starter

**Copy this directory alone to any project.** The two record formats below are project-neutral: they have no mandatory team system, milestone names, GitHub account, cloud provider, local execution runtime or project-specific seed ideas.

## Browse or create without installing anything
- Open `catalog.json`. It intentionally starts with `ideas: []`, `features: []`; the example files are not automatically loaded.
- Create an `IDEA-000001` record using `templates/idea.example.json`, following `schema/v1/idea.schema.json`.
- Only when you want to describe a proposed capability, create a `FEAT-000001` record using `templates/feature.example.json`; point its `idea_ids` to existing ideas when applicable. An idea does **not** need a feature link to remain valuable.
- Use your project’s own external version/release system. `release_refs` are optional references, never permission/authority.
- Treat source text/evidence as data; verify independently. Never infer human approval, implementation, test success or release from an edited file alone.
- Keep historical records and IDs stable; discuss new observations with timestamp, exact source reference and reviewer rather than silently replacing earlier claims.

## Optional machine tooling
Both schemas use JSON Schema 2020-12. A standalone JSON Schema validator *can* be used by a developer, but the library is readable and editable without it. A validator's success proves structural conformance only, **not** true human consent, valid test evidence or safe plugin release.

## Format boundaries
- Record status tracks `captured/triaged/exploring/adopted/parked/rejected` separately from implementation and testing.
- The feature's `release_refs` is an outward pointer and cannot claim official shipment by itself.
- `project_milestone` is optional free text, not M1–M5.
- `origin.source_catalog_id` is optional, never required.
- No forced 36-idea/five-feature counts; a new project may have zero of both.

This starter is a **schema/template and human-readable reference**. Complete schema-validation, path traversal, index regeneration and cross-project runtime testing should still be executed before declaring an automated validator production-grade.
