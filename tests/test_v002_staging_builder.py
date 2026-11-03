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
    def test_staging_startup_prompt_exactly_matches_candidate(self):
        # Launch-time instructions must be release-equivalent, unlike staging labels.
        with zipfile.ZipFile(BytesIO(self.src)) as source, zipfile.ZipFile(BytesIO(self.staged)) as staged:
            prompts = []
            for path in ("plugin.json", ".codex-plugin/plugin.json"):
                candidate = json.loads(source.read(path))
                preview = json.loads(staged.read(path))
                if path == "plugin.json":
                    c_ui = candidate["extensions"]["com.openai"]["interface"]
                    s_ui = preview["extensions"]["com.openai"]["interface"]
                else:
                    c_ui = candidate["interface"]
                    s_ui = preview["interface"]
                self.assertIsInstance(c_ui["defaultPrompt"], str)
                self.assertTrue(c_ui["defaultPrompt"].strip())
                self.assertEqual(s_ui["defaultPrompt"], c_ui["defaultPrompt"], path)
                prompts.append(s_ui["defaultPrompt"])
            self.assertEqual(prompts[0], prompts[1])

    def test_staging_descriptors_only_change_identity_and_branding(self):
        allowed = ("name", "description")
        allowed_ui = ("displayName", "shortDescription", "longDescription")
        with zipfile.ZipFile(BytesIO(self.src)) as source, zipfile.ZipFile(BytesIO(self.staged)) as staged:
            for path in ("plugin.json", ".codex-plugin/plugin.json"):
                original = json.loads(source.read(path))
                preview = json.loads(staged.read(path))
                for key in allowed:
                    preview[key] = original[key]
                if path == "plugin.json":
                    a = original["extensions"]["com.openai"]["interface"]
                    b = preview["extensions"]["com.openai"]["interface"]
                else:
                    a = original["interface"]
                    b = preview["interface"]
                for key in allowed_ui:
                    b[key] = a[key]
                self.assertEqual(preview, original, path)

    def test_mismatched_source_entry_prompts_fail_closed(self):
        # Construct a source archive with valid content digests but divergent
        # canonical manifest prompts; never allow arbitrary staging behavior.
        from hashlib import sha256
        with zipfile.ZipFile(BytesIO(self.src)) as src:
            files = {name: src.read(name) for name in src.namelist()}
        descriptor = json.loads(files[".codex-plugin/plugin.json"])
        descriptor["interface"]["defaultPrompt"] = "A different startup instruction"
        changed = (json.dumps(descriptor, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf8")
        files[".codex-plugin/plugin.json"] = changed
        manifest = json.loads(files["RELEASE-SOURCE-MANIFEST.json"])
        for row in manifest["files"]:
            if row["path"] == ".codex-plugin/plugin.json":
                row["sha256"] = sha256(changed).hexdigest()
                row["bytes"] = len(changed)
        files["RELEASE-SOURCE-MANIFEST.json"] = (
            json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf8")
        buff = BytesIO()
        with zipfile.ZipFile(buff, "w", compression=zipfile.ZIP_STORED) as z:
            for name, data in sorted(files.items()):
                z.writestr(name, data)
        with self.assertRaisesRegex(PackageError, "STAGING_SOURCE_STARTUP_PROMPT_MISMATCH"):
            build_staging(buff.getvalue(), SHA)

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
