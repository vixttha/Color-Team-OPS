# Cloud-only repository development tests

`requirements-ci.txt` is **development CI tooling only**, and must never become an end-user plugin dependency. GitHub-hosted Ubuntu and Windows are the required baseline; personal Windows/Linux runners may run the identical suite only by explicit manual opt-in, on reviewed main, and never replace the required baseline.

Tests:
- `test_package.py` checks twelve skills, manifest parity and Draft 2020-12 schemas/examples using `jsonschema`.
- `test_schema_adversarial.py` tests fake authorization, unsupported runner requirements, false observed evidence, misleading PASS and invalid dispatch decisions.
- `test_workflows.py` parses the YAML event/job tree with a duplicate-key-rejecting loader, asserts effective permissions, cloud runner targets, the manual owner+main opt-in and detects known bypass mutations.
- `test_policy.py` preserves the constitutional law and README/CHANGELOG version rules.

Source tests alone cannot prove a model respects untrusted instructions. No tests or features require owner-operated computers. Every PASS must be linked to exact SHA and real hosted job evidence. No CI result is fabricated.
