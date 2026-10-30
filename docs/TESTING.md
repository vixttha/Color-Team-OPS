# Cloud-only repository development tests

`requirements-ci.txt` is **development CI tooling only**, and must never become an end-user plugin dependency. For v0.0.1 the owner authorized release validation on the dedicated Windows and Linux GitHub self-hosted runners via the version-scoped, read-only release branch workflow. This developer CI is independent of the installed plugin and is not a runtime prerequisite.

Tests:
- `test_package.py` checks twelve skills, manifest parity and Draft 2020-12 schemas/examples using `jsonschema`.
- `test_schema_adversarial.py` tests fake authorization, unsupported runner requirements, false observed evidence, misleading PASS and invalid dispatch decisions.
- `test_workflows.py` parses the YAML event/job tree with a duplicate-key-rejecting loader, asserts effective permissions, owner-approved runner targets, strict branch triggers and detects known bypass mutations.
- `test_policy.py` preserves the constitutional law and README/CHANGELOG version rules.

Source tests alone cannot prove a model respects untrusted instructions. No tests or features require owner-operated computers. Every PASS must be linked to exact SHA and real executed GitHub Actions job evidence from the selected owner runners. No CI result is fabricated.

## Observed runner execution

Windows used an isolated `.cto-test-venv` in the test workspace. Linux used its already-installed Python, PyYAML and `jsonschema` because system Python lacks the optional ensurepip/pip environment bootstrap; no system packages were installed. Exact SHA `021b7b8552776e0c14db6207292300ff22a43159` passed 25/25 on each runner. The schema also includes a strict syntax pattern to keep date-like claim values from being silently accepted when optional format checkers are absent.

This only concerns **developer tests**, never the installed plugin's requirements. Cloud-only hosting remains the product contract.
