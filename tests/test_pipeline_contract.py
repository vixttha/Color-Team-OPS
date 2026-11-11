"""Static owner-arm workflow contract (does NOT parse general YAML)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PipelinePolicyTests(unittest.TestCase):
    def test_optional_pipeline_narrow_trigger_and_readonly_token(self):
        path = ROOT / ".github/workflows/idea-feature-library-v002.yml"
        if not path.exists():
            self.skipTest("Optional source workflow not installed on adopter")
        source = path.read_text(encoding="utf-8")
        self.assertIn("branches: [idea-feature-library-v0.0.2]", source)
        self.assertIn("ops/acceptance/idea-feature-library-v002-arm.txt", source)
        self.assertIn("permissions:\n  contents: read", source)
        for forbidden in ("\n  pull_request:", "\n  pull_request_target:",
                          "\n  workflow_run:", "contents: write", "secrets."):
            self.assertNotIn(forbidden, source.lower())
        self.assertIn("github.actor == 'vixttha'", source)
        self.assertIn("needs: [head-and-worker-linux]", source)
        self.assertIn("ref: ${{ github.sha }}", source)
        self.assertIn("persist-credentials: false", source)
        resolved = re.findall(r"uses: (actions/checkout)@([0-9a-f]{40})\b", source)
        self.assertEqual(len(resolved), 2, "both checkout pins must be 40-hex SHA")
        self.assertEqual({sha for name, sha in resolved},
                         {"11d5960a326750d5838078e36cf38b85af677262"})
        self.assertIn("color-team-ops-linux-01", source)
        self.assertIn("color-team-ops-windows-01", source)

    def test_source_has_no_runtime_governance_imports(self):
        for relative in ("tools/library.py", "tools/adopter.py"):
            source = (ROOT / relative).read_text(encoding="utf-8").lower()
            self.assertNotIn("import governance_branch", source)
            self.assertNotIn("from governance_branch", source)


if __name__ == "__main__":
    unittest.main()
