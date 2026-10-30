"""Owner-locked CTO-LOCK-001: core neutrality acceptance checks."""
import ast
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
ADR=ROOT/"docs"/"23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md"
LAW="Keep Color Team OPS cloud-only, provider-neutral, and independent of any specific hosting platform."


class NeutralityLawTests(unittest.TestCase):
    def test_owner_exact_law_documented(self):
        self.assertIn(LAW,ADR.read_text(encoding="utf-8"))
    def test_owner_decision_is_binding_not_vendor_selection(self):
        text=ADR.read_text(encoding="utf-8")
        self.assertIn("OWNER-LOCKED / BINDING",text)
        self.assertIn("No hosting vendor was selected",text)
    def test_runner_independence_law_is_preserved(self):
        text=ADR.read_text(encoding="utf-8")
        self.assertIn(
            "Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate.",
            text)
    def test_schema_requires_cloud_only_without_owner_runner(self):
        schema=json.loads((ROOT/"contracts"/"v0.0.2"/"mission.schema.json").read_text(encoding="utf-8"))
        self.assertIs(schema["properties"]["cloud_only"]["const"],True)
        self.assertIs(schema["properties"]["runner_required"]["const"],False)
    def test_policy_core_has_no_provider_specific_import(self):
        tree=ast.parse((ROOT/"policy_v002"/"verifier.py").read_text(encoding="utf-8"))
        modules=[
            n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)
        ]+[alias.name for n in ast.walk(tree) if isinstance(n,ast.Import) for alias in n.names]
        self.assertFalse(any(m and any(p in m.lower() for p in
            ("github_provider","supabase","vercel","boto3","azure","google.cloud"))
            for m in modules))
    def test_mission_contract_does_not_require_github_vendor(self):
        schema=json.loads((ROOT/"contracts"/"v0.0.2"/"mission.schema.json").read_text(encoding="utf-8"))
        self.assertNotIn("provider",schema["required"])
        self.assertNotIn("github",schema["required"])
    def test_readme_links_locked_law(self):
        md=(ROOT/"README.md").read_text(encoding="utf-8")
        self.assertIn("docs/23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md",md)

if __name__=="__main__":unittest.main()
