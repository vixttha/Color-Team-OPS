"""Red/Purple negative contract tests: exact cross-field, evidence, and authority semantics."""
import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("mission", "completion-event", "routing-decision")


def get(name):
    schema = json.loads((ROOT / "schemas" / (name + ".schema.json")).read_text("utf-8"))
    example = json.loads((ROOT / "examples" / (name + ".json")).read_text("utf-8"))
    return Draft202012Validator(schema, format_checker=FormatChecker()), example


class ContractAdversarialTests(unittest.TestCase):
    def test_validated_schema_and_examples(self):
        for name in NAMES:
            with self.subTest(name=name):
                validator, example = get(name)
                validator.check_schema(validator.schema)
                validator.validate(example)

    def test_mission_authority_negative(self):
        validator, base = get("mission")
        sha = "a" * 40
        cases = {
            "missing-authorizer": lambda x: x.pop("authorization_ref"),
            "empty-team-list": lambda x: x.update(allowed_teams=[]),
            "empty-action-list": lambda x: x.update(allowed_actions=[]),
            "unsigned-branch-write": lambda x: x.update(allowed_actions=["write_authorized_branch"]),
            "spoofed-HEAD": lambda x: x.update(source_sha="HEAD"),
            "bad-repo": lambda x: x.update(repository="https://evil.invalid/repo"),
            "wrong-cloud-law": lambda x: x.update(cloud_only=False),
            "mandatory-user-runner": lambda x: x.update(runner_required=True),
        }
        for case, mutate in cases.items():
            with self.subTest(case=case):
                payload = copy.deepcopy(base)
                mutate(payload)
                with self.assertRaises(ValidationError):
                    validator.validate(payload)
        for branch in ("main", "master"):
            payload = copy.deepcopy(base)
            payload.update(allowed_actions=["write_authorized_branch"],
                           repository="vixttha/Color-Team-OPS",
                           source_sha=sha, authorized_branch=branch)
            with self.subTest(branch=branch), self.assertRaises(ValidationError):
                validator.validate(payload)

    def test_valid_branch_write_contract_is_not_identity_proof(self):
        validator, payload = get("mission")
        payload.update(allowed_actions=["write_authorized_branch"],
                       repository="vixttha/Color-Team-OPS",
                       source_sha="a" * 40, authorized_branch="release/test-contract")
        validator.validate(payload)

    def test_observed_evidence_negative(self):
        validator, base = get("completion-event")
        base.update(evidence_state="OBSERVED", source_sha="a" * 40,
                    evidence_refs=["cloud://verified/test"], observed_by="trusted-connector")
        validator.validate(base)
        for key in ("source_sha", "evidence_refs", "observed_by"):
            with self.subTest(key=key):
                payload = copy.deepcopy(base)
                del payload[key]
                with self.assertRaises(ValidationError):
                    validator.validate(payload)
        for bad in ("HEAD", "ref/main", "deadbeef"):
            payload = copy.deepcopy(base)
            payload["source_sha"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                validator.validate(payload)
        payload = copy.deepcopy(base)
        payload["evidence_refs"] = []
        with self.assertRaises(ValidationError):
            validator.validate(payload)

    def test_dispatched_team_required_and_forbidden_elsewhere(self):
        validator, base = get("routing-decision")
        payload = copy.deepcopy(base)
        payload.update(action="DISPATCH")
        with self.assertRaises(ValidationError):
            validator.validate(payload)
        payload["next_team"] = "orange-team"
        validator.validate(payload)
        payload["action"] = "BLOCK"
        with self.assertRaises(ValidationError):
            validator.validate(payload)

    def test_pass_requires_evidence_and_provenance(self):
        validator, base = get("routing-decision")
        good = copy.deepcopy(base)
        good.update(verification="PASS", source_sha="b" * 40,
                    evidence_refs=["cloud://ci/runs/123"],
                    verifier_identity="independent-ci-trust-anchor",
                    verification_time="2026-10-29T23:00:00Z")
        validator.validate(good)
        for key in ("source_sha", "evidence_refs", "verifier_identity", "verification_time"):
            payload = copy.deepcopy(good)
            payload.pop(key)
            with self.subTest(key=key), self.assertRaises(ValidationError):
                validator.validate(payload)
        payload = copy.deepcopy(good)
        payload["evidence_refs"] = []
        with self.assertRaises(ValidationError):
            validator.validate(payload)
        payload = copy.deepcopy(good)
        payload["verification_time"] = "not-a-time"
        with self.assertRaises(ValidationError):
            validator.validate(payload)


if __name__ == "__main__":
    unittest.main()
