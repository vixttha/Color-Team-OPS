# v0.0.1 contract trust boundaries

JSON Schema Draft 2020-12 enforces **shape and cross-field constraints only**. A passing schema validation is **not proof** that an event, authorization or verifier is genuine.

## Mission authorization

An AUTHORIZED mission requires an `authorization_ref`; a proposed branch write or draft PR also needs `repository`, an exact 40-hex-character `source_sha` and a non-default `authorized_branch`. The reference and fields are *claims* until validated against a trusted host/cloud authorization source. Reject spoofed or stale authority, unapproved repositories and revoked permissions even when JSON validates.

## Completion evidence

An OBSERVED event requires a source revision, nonempty evidence references and `observed_by`. Values from an LLM, repository file, issue body or caller alone are **untrusted**. Verify event IDs, referenced tools, exact revision, evidence integrity and scope from independent cloud resources. Missing trust anchors => UNVERIFIED.

## Routing decisions

DISPATCH requires `next_team`; all other actions forbid it. PASS requires verifier identity, verification time, evidence references and the exact source revision, but the fields **do not establish independence**. Do not treat a PASS string as an authenticated release gate. No trust service or persistent background dispatcher exists in v0.0.1.

## Tests and validation

The CI verifier must use a genuine Draft 2020-12 validator for conditional `allOf/if/then/else`, `contains`, patterns and item cardinality. Its regression suite must check both accepted examples and adversarial negative examples. Local owner-runner execution is never necessary.
