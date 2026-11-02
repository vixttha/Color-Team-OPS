"""Source-only staging transform and safety checks. No plugin Creator mutation."""
from io import BytesIO
import json
import unittest
import zipfile
from pathlib import Path
from devtools.build_v002_candidate import build, PackageError
from devtools.build_v002_staging import build_staging,STAGING_SLUG,STAGING_LABEL

ROOT=Path(__file__).resolve().parents[1]
SHA="a"*40

class StagingVariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=build(ROOT,SHA,check_checkout=False).archive
        cls.staged,cls.report=build_staging(cls.src,SHA)

    def test_actual_archive_has_exact_roles_and_distinct_identity(self):
        self.assertEqual((self.report["files"],self.report["skills"],self.report["competencies"]),(32,12,9))
        with zipfile.ZipFile(BytesIO(self.staged)) as z:
            a=json.loads(z.read("plugin.json"))
            b=json.loads(z.read(".codex-plugin/plugin.json"))
            self.assertEqual((a["name"],b["name"]),(STAGING_SLUG,STAGING_SLUG))
            self.assertEqual((a["version"],b["version"]),("0.0.2","0.0.2"))
            self.assertEqual(a["extensions"]["com.openai"]["interface"]["displayName"],STAGING_LABEL)
            self.assertEqual(b["interface"]["displayName"],STAGING_LABEL)
            m=json.loads(z.read("RELEASE-SOURCE-MANIFEST.json"))
            self.assertEqual(m["source_sha"],SHA)
            self.assertEqual(m["variant"],"PRIVATE_STAGING_NOT_RELEASED")
    def test_original_canonical_archive_unmodified(self):
        with zipfile.ZipFile(BytesIO(self.src)) as z:
            a=json.loads(z.read("plugin.json"))
        self.assertEqual(a["name"],"color-team-ops")
    def test_only_two_plugin_manifest_bytes_changed(self):
        with zipfile.ZipFile(BytesIO(self.src)) as original,zipfile.ZipFile(BytesIO(self.staged)) as changed:
            self.assertEqual(set(original.namelist()),set(changed.namelist()))
            for p in original.namelist():
                if p not in ("plugin.json",".codex-plugin/plugin.json","RELEASE-SOURCE-MANIFEST.json"):
                    self.assertEqual(original.read(p),changed.read(p),p)
    def test_deterministic_staging_two_runs(self):
        again,_=build_staging(self.src,SHA)
        self.assertEqual(again,self.staged)
        self.assertNotEqual(self.src,self.staged)
    def test_tampered_source_fails_closed(self):
        with self.assertRaises((PackageError,zipfile.BadZipFile)):
            build_staging(b"not-a-verified-archive",SHA)
    def test_does_not_include_python_plugin_runtime(self):
        with zipfile.ZipFile(BytesIO(self.staged)) as z:
            self.assertFalse(any(p.endswith(".py") for p in z.namelist()))
            self.assertEqual(len([p for p in z.namelist() if p.endswith("/SKILL.md")]),12)
if __name__ == "__main__": unittest.main()
