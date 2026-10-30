# Purple → Yellow → Validate → Internal Auditor — optional library repair

**Boundary:** development/reference branch only; not Color-Team-OPS runtime, M1–M5 integration promotion, publication, runner provisioning, authority change or release acceptance.

## Intended acceptance
- No hardcoded idea/feature counts in the **checker**. Existing 36+5 records preserved byte-for-byte.
- Generic count-neutral local validation, complete checked-in historical schema-keyword subset, unknown-field rejection, dangling links, unsafe paths, unsupported `verified`, and dishonest release claims rejected.
- Deterministic generated indexes, with a read-only checker detecting stale contents.
- Versioned portable `portable/v0.0.1` starter containing empty record folders and the v0.0.1 schema/examples, optional tools and tests.
- Optional local adopter performs preflight and refuses existing destinations; hosted GitHub hand-copy works without Python. Concurrency cannot be made fully atomic across independent directories by this helper.
- Historical vs engineering status shown in separate dated evidence note, not overwritten on speculation.
- No imported Color-Team-OPS records in the reusable starter; original source snapshots and the v0.0.2 master remain separate.

## Local checks, only if an interpreter is already available
```sh
python tools/check_idea_feature_library.py
python -m unittest discover -s tests -p 'test_idea_feature_library.py' -v
python portable/v0.0.1/tools/library.py check
python -m unittest discover -s portable/v0.0.1/tests -v
```
No cloud CI, runner, external service, login or special plugin is required. Tests authenticate neither historical decisions nor any external evidence.

## Unresolved acceptance boundaries
- The tool's structural checks do not authenticate provenance or perform a formally complete generic JSON Schema 2020-12 implementation beyond bundled keywords.
- Concurrent filesystem changes and hostile existing host symlinks require host-level controls; never describe the optional copy helper as globally atomic.
- Separate independent/security review and any official shipping decisions remain external.
