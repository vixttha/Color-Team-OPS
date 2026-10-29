"""Red/Purple semantic validation of effective GitHub Actions policies."""
import copy
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
HOSTED = (ROOT / ".github/workflows/cloud-ci.yml").read_text(encoding="utf-8")
OPTIONAL = (ROOT / ".github/workflows/optional-self-hosted.yml").read_text(encoding="utf-8")
CHECKOUT = "actions/checkout@11d5960a326750d5838078e36cf38b85af677262"
REPO_OWNER = "vixttha"
MAIN = "refs/heads/main"
DOLLAR = chr(36)


class DuplicateRejectingLoader(yaml.BaseLoader):
    def construct_mapping(self, node, deep=False):
        pairs = self.construct_pairs(node, deep=deep)
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate YAML key: " + key)
            result[key] = value
        return result


def parse_yaml(text):
    workflow = yaml.load(text, Loader=DuplicateRejectingLoader)
    if not isinstance(workflow, dict):
        raise AssertionError("YAML root is not an object")
    return workflow


def ensure_cloud(text):
    flow = parse_yaml(text)
    assert set(flow) == {"name", "on", "permissions", "jobs"}
    assert set(flow["on"]) == {"pull_request", "push"}
    for event in ("pull_request", "push"):
        assert flow["on"][event]["branches"] == ["main"]
    assert flow["permissions"] == {"contents": "read"}
    assert set(flow["jobs"]) == {"cloud-validation"}
    job = flow["jobs"]["cloud-validation"]
    assert "if" not in job and "needs" not in job and "environment" not in job
    assert job["runs-on"] == DOLLAR + "{{ matrix.os }}"
    assert job["strategy"]["matrix"]["os"] == ["ubuntu-24.04", "windows-2022"]
    assert job["timeout-minutes"] == "10"
    steps = job["steps"]
    assert len(steps) in (2, 3)
    assert steps[0]["uses"] == CHECKOUT
    assert steps[0]["with"]["persist-credentials"] == "false"
    assert any("unittest discover" in step.get("run", "") for step in steps)
    assert not any("secrets" in repr(step) for step in steps)
    return True


def ensure_optional(text):
    flow = parse_yaml(text)
    assert set(flow) == {"name", "on", "permissions", "jobs"}
    assert set(flow["on"]) == {"workflow_dispatch"}
    approval = flow["on"]["workflow_dispatch"]["inputs"]["allow_personal_runners"]
    assert approval["required"] == "true" and approval["type"] == "boolean"
    assert approval["default"] == "false"
    assert flow["permissions"] == {"contents": "read"}
    assert set(flow["jobs"]) == {"supplemental-windows", "supplemental-linux"}
    condition = "github.actor == 'vixttha' && github.ref == 'refs/heads/main' && inputs.allow_personal_runners"
    for name, labels in (
        ("supplemental-windows", ["self-hosted", "Windows", "X64", "color-team-ops"]),
        ("supplemental-linux", ["self-hosted", "Linux", "X64", "color-team-ops"]),
    ):
        job = flow["jobs"][name]
        assert job["if"] == condition
        assert job["runs-on"] == labels
        assert "needs" not in job and "environment" not in job
        assert job["timeout-minutes"] == "10"
        steps = job["steps"]
        assert len(steps) in (2, 3)
        assert steps[0]["uses"] == CHECKOUT
        assert steps[0]["with"] == {"ref": "main", "persist-credentials": "false"}
        assert any("unittest discover" in step.get("run", "") for step in steps)
    return True


class WorkflowPolicyTests(unittest.TestCase):
    def test_hosted_baseline(self):
        self.assertTrue(ensure_cloud(HOSTED))

    def test_optional_trusted_owner(self):
        self.assertTrue(ensure_optional(OPTIONAL))

    def test_mutation_removing_effective_guard_is_caught(self):
        changed = OPTIONAL.replace(
            "if: github.actor == 'vixttha' && github.ref == 'refs/heads/main' && inputs.allow_personal_runners",
            "if: true # github.actor == 'vixttha' && github.ref == 'refs/heads/main' && inputs.allow_personal_runners")
        with self.assertRaises(AssertionError):
            ensure_optional(changed)

    def test_mutation_adding_trigger_is_caught(self):
        changed = OPTIONAL.replace("  workflow_dispatch:", "  workflow_call:\n  workflow_dispatch:")
        with self.assertRaises(AssertionError):
            ensure_optional(changed)

    def test_mutation_additional_required_runner_is_caught(self):
        changed = HOSTED.replace("    runs-on: " + DOLLAR + "{{ matrix.os }}",
                                 "    runs-on: [self-hosted, Windows, X64, color-team-ops]")
        with self.assertRaises(AssertionError):
            ensure_cloud(changed)

    def test_mutation_duplicate_yaml_trigger_is_caught(self):
        changed = OPTIONAL.replace("on:\n", "on:\n  push: \n", 1)
        with self.assertRaises(AssertionError):
            ensure_optional(changed)


if __name__ == "__main__":
    unittest.main()
