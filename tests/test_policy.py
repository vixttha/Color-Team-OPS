"""Cloud-only design law and README-per-version regression tests."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


class PolicyTests(unittest.TestCase):
    def test_runner_policy_preserved(self):
        text = read("docs/design/RUNNER-POLICY.md")
        self.assertIn("Status: ACCEPTED", text)
        for phrase in (
            "Running development tests", "Performing independent audits",
            "Validating plugin packages", "Testing releases",
            "Running the installed Color Team OPS plugin",
            "Powering its autonomous operations",
            "Serving as its database or cloud backend",
        ):
            self.assertIn(phrase, text)
        self.assertGreaterEqual(text.count("Never required"), 3)
        self.assertIn("manual workflow_dispatch", text)
        self.assertIn("GitHub-hosted", text)

    def test_constitution_and_architecture(self):
        law = read("docs/CONSTITUTION.md")
        for phrase in (
            "L1 — Cloud-only", "L2 — Runners optional", "L10 — No forced runner CI",
            "development tests", "independent audits", "README.md", "CHANGELOG.md",
            "ADR-0001",
        ):
            self.assertIn(phrase, law)
        self.assertIn("design/RUNNER-POLICY.md", read("docs/ARCHITECTURE.md"))

    def test_readme_and_changelog_version(self):
        version = json.loads(read("plugin.json"))["version"]
        self.assertIn(version, read("README.md"))
        self.assertIn("[" + version + "]", read("CHANGELOG.md"))
        for path in (
            "docs/design/RUNNER-POLICY.md",
            "docs/decisions/ADR-0001-runner-separation.md",
            "docs/RELEASE-PROCESS.md",
        ):
            self.assertIn(path, read("README.md"))
            self.assertTrue((ROOT / path).is_file())
        self.assertIn("README.md", read("docs/RELEASE-PROCESS.md"))

    def test_design_decision_accepted(self):
        decision = read("docs/decisions/ADR-0001-runner-separation.md")
        self.assertIn("ACCEPTED", decision)
        self.assertIn("manual approval", decision)
        self.assertIn("README", decision)


if __name__ == "__main__":
    unittest.main()
