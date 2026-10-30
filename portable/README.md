# Portable Feature + Idea Library

**Recommended portable version:** [v0.0.1](v0.0.1/README.md). That subdirectory is the *complete host-neutral template* with empty `ideas/records` and `features/records` directories, example records, deterministic indexes, optional structural checker and no-clobber adoption helper.

- To adopt without executing anything, copy `v0.0.1/ideas`, `v0.0.1/features`, `v0.0.1/templates`, and its agent guide into a project with nonconflicting paths.
- If standard-library Python is already installed, `python v0.0.1/tools/adopt.py /path/to/existing/project` optionally performs a conservative copy. Add `--with-tools` for the optional validators/tests/docs.
- Existing destinations are never intentionally overwritten. Check the target first; there is no transaction across directories if another writer races the copy.

## Compatibility

The older `catalog.json`, `schema/v1/`, and `templates/` directly under this folder are **retained legacy research prototypes**, NOT a competing required registry. Those schemas are a different profile (for example, `release_refs` versus `release_membership: NOT_ASSERTED`). Do not combine their records with the v0.0.1 record folders, invent release status, or perform automatic lossy field conversion.

See [profile mapping](../docs/SCHEMA-PROFILES-AND-COMPATIBILITY.md), [isolation](../docs/PORTABILITY-AND-ISOLATION.md), and [historical/engineering distinction](../docs/HISTORICAL-STATUS-VS-ENGINEERING.md).

No Governance-Branch, Color-Team-OPS plugin, cloud service, runner or local execution environment is required merely to **read or hand-edit** the template.
