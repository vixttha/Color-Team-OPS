"""Guard a single canonical private plugin identity and honest retirement status."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/PLUGIN-RELEASE-REGISTRY.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
ID = re.compile(r"^plugins_[0-9a-f]+$")


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PluginIdentityTests(unittest.TestCase):
    def test_one_canonical_version_and_source(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        manifest = json.loads(read("plugin.json"))
        compatibility = json.loads(read(".codex-plugin/plugin.json"))
        self.assertEqual(registry["product"], "color-team-ops")
        self.assertEqual(registry["schema_version"], 1)
        canonical = registry["canonical"]
        self.assertRegex(canonical["plugin_id"], ID)
        self.assertRegex(canonical["source_sha"], SHA40)
        self.assertEqual(canonical["status"], "active_private")
        self.assertEqual(canonical["version"], manifest["version"])
        self.assertEqual(canonical["version"], compatibility["version"])
        self.assertTrue(canonical["plugin_url"].endswith(canonical["plugin_id"]))
        self.assertIn(canonical["plugin_url"], read("README.md"))
        self.assertIn(canonical["release_id"], read("README.md"))
        self.assertIn(canonical["source_sha"], read("README.md"))

    def test_superseded_plugin_not_falsely_retired(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        canonical = registry["canonical"]
        retired = registry["superseded"]
        all_ids = [canonical["plugin_id"]] + [p["plugin_id"] for p in retired]
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertEqual(len(retired), 1)
        for entry in retired:
            self.assertRegex(entry["plugin_id"], ID)
            self.assertNotEqual(entry["plugin_id"], canonical["plugin_id"])
            self.assertEqual(entry["status"], "superseded_creator_record_present")
            self.assertEqual(entry["uninstallation"], "owner_authorized_creator_deletion_pending")
            self.assertTrue(entry["owner_authorized_deletion"])
            self.assertTrue(entry["creator_record_present"])
            self.assertFalse(entry["creator_delete_operation_available_in_session"])
            self.assertEqual(entry["connection_uninstall_result"], "not_installed")
            self.assertIn("OLD", entry["display_name"])
            self.assertEqual(entry["version"], "0.0.2")
            self.assertRegex(entry["release_id"], r"^pluginrel_[0-9a-f]+$")
        self.assertIn("SUPERSEDED BUT STILL INSTALLED", read("docs/decisions/ADR-0003-canonical-plugin-identity.md"))

    def test_upgrade_policy_is_fail_closed(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertTrue(all(registry["policies"].values()))
        process = read("docs/RELEASE-PROCESS.md")
        for phrase in (
            "PLUGIN-RELEASE-REGISTRY.json",
            "existing canonical plugin ID",
            "explicit owner approval",
            "actual uninstall evidence",
        ):
            self.assertIn(phrase, process)
        self.assertIn("ADR-0003", read("README.md"))
        self.assertIn("Your runners can help develop and verify Color Team OPS", read("README.md"))


if __name__ == "__main__":
    unittest.main()
