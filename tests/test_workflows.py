"""Enforce required cloud CI and manual, opt-in personal runner supplements."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOSTED = (ROOT / ".github/workflows/cloud-ci.yml").read_text(encoding="utf-8")
OPTIONAL = (ROOT / ".github/workflows/optional-self-hosted.yml").read_text(encoding="utf-8")


class WorkflowPolicyTests(unittest.TestCase):
    def test_cloud_baseline(self):
        self.assertIn("pull_request:", HOSTED)
        self.assertIn("push:", HOSTED)
        self.assertIn("ubuntu-24.04", HOSTED)
        self.assertIn("windows-2022", HOSTED)
        self.assertIn("runs-on: " + chr(36) + "{{ matrix.os }}", HOSTED)
        self.assertNotIn("self-hosted", HOSTED.lower())
        self.assertIn("permissions:\n  contents: read", HOSTED)
        self.assertIn("persist-credentials: false", HOSTED)
        self.assertRegex(HOSTED, r"actions/checkout@[a-f0-9]{40}")
        self.assertIn("unittest discover", HOSTED)

    def test_optional_trusted_main_only(self):
        events = OPTIONAL.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", events)
        self.assertNotIn("\n  pull_request:", events)
        self.assertNotIn("\n  push:", events)
        self.assertIn("allow_personal_runners:", OPTIONAL)
        self.assertIn("default: false", OPTIONAL)
        self.assertIn("refs/heads/main", OPTIONAL)
        self.assertIn("ref: main", OPTIONAL)
        self.assertIn("runs-on: " + chr(36) + "{{ matrix.labels }}", OPTIONAL)
        self.assertIn("self-hosted", OPTIONAL)
        self.assertIn("Windows", OPTIONAL)
        self.assertIn("Linux", OPTIONAL)
        self.assertIn("permissions:\n  contents: read", OPTIONAL)
        self.assertIn("persist-credentials: false", OPTIONAL)
        self.assertRegex(OPTIONAL, r"actions/checkout@[a-f0-9]{40}")
        self.assertNotIn("secrets.", OPTIONAL)

    def test_no_cloud_dependency_on_owner_hardware(self):
        self.assertNotIn("needs:", HOSTED)
        self.assertNotIn("pull_request_target:", OPTIONAL)
        self.assertNotIn("workflow_run:", OPTIONAL)
        self.assertNotIn("schedule:", OPTIONAL)


if __name__ == "__main__":
    unittest.main()
