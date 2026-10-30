"""Cloud development-only deterministic candidate package tests (stdlib fixtures).

These do NOT substitute for building the real private GitHub checkout at an
exact source SHA, uploading its ZIP, or running installed ChatGPT plugin trials.
"""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from io import BytesIO
from zipfile import ZipFile

from devtools.build_v002_candidate import build, validate_archive, PackageError

SHA="a"*40
TEAMS=("yellow-team","orange-team","green-team","red-team","blue-team",
       "purple-team","white-team","black-team","gray-cell")
COORD=("mission-control","ops-director","verification-gate")


class DeterministicBuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.write("plugin.json",json.dumps({"name":"color-team-ops","version":"0.0.2"}))
        self.write(".codex-plugin/plugin.json",
                   json.dumps({"name":"color-team-ops","version":"0.0.2"}))
        self.write("docs/CONSTITUTION.md","cloud-only\n")
        self.write("registry/v0.0.2/teams.json","{}\n")
        for i in range(3):
            self.write(f"schemas/schema-{i}.json","{}\n")
            self.write(f"examples/example-{i}.json","{}\n")
        for name in TEAMS+COORD:
            self.write(f"skills/{name}/SKILL.md",f"---\nname: {name}\n---\n")
        for name in TEAMS:
            self.write(f"skills/{name}/references/v002-competencies.md",
                       f"{name} evidence and exclusions\n")

    def write(self,path,content):
        p=self.root/path
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(content,encoding="utf-8")

    def build(self):
        return build(self.root,SHA,check_checkout=False)

    def test_twice_identical_bytes_and_hashes(self):
        a,b=self.build(),self.build()
        self.assertEqual((a.archive,a.sha256_digest),(b.archive,b.sha256_digest))
        self.assertEqual(len(a.sha256_digest),64)

    def test_exactly_12_skills_and_nine_references(self):
        result=self.build()
        with ZipFile(BytesIO(result.archive)) as z:
            names=z.namelist()
        self.assertEqual(len([x for x in names if x.endswith("/SKILL.md")]),12)
        self.assertEqual(len([x for x in names if x.endswith("/v002-competencies.md")]),9)

    def test_python_runtime_and_library_not_included(self):
        result=self.build()
        with ZipFile(BytesIO(result.archive)) as z:
            names=z.namelist()
            self.assertFalse(any(x.startswith(("policy_v002/","ideas/","features/",
                "tests/","portable/")) for x in names))
            manifest=json.loads(z.read("RELEASE-SOURCE-MANIFEST.json"))
            self.assertIs(manifest["python_policy_runtime_included"],False)

    def test_source_manifest_attests_each_payload(self):
        result=self.build()
        self.assertEqual(result.file_count,32)
        validate_archive(result.archive,SHA)

    def test_missing_specialist_fails(self):
        (self.root/"skills/yellow-team/SKILL.md").unlink()
        with self.assertRaises(PackageError):
            self.build()

    def test_missing_team_reference_fails(self):
        (self.root/"skills/gray-cell/references/v002-competencies.md").unlink()
        with self.assertRaises(PackageError):
            self.build()

    def test_corrupted_manifest_identity_fails(self):
        self.write("plugin.json",json.dumps({"name":"color-team-ops","version":"0.0.3"}))
        with self.assertRaises(PackageError):
            self.build()

    def test_invalid_source_sha_fails(self):
        with self.assertRaises(PackageError):
            build(self.root,"not-a-sha",check_checkout=False)

    def test_git_checkout_binding_is_required_by_default(self):
        with patch("devtools.build_v002_candidate.subprocess.check_output",
                   return_value="b"*40+"\n"):
            with self.assertRaises(PackageError):
                build(self.root,SHA)

    def test_dirty_checkout_is_rejected_even_at_exact_head(self):
        with patch("devtools.build_v002_candidate.subprocess.check_output",
                   side_effect=[SHA+"\n"," M skills/yellow-team/SKILL.md\n"]):
            with self.assertRaises(PackageError) as issue:
                build(self.root,SHA)
            self.assertEqual(str(issue.exception),"DIRTY_SOURCE_CHECKOUT")

    def test_clean_checkout_at_matching_sha_is_allowed(self):
        with patch("devtools.build_v002_candidate.subprocess.check_output",
                   side_effect=[SHA+"\n",""]):
            self.assertEqual(build(self.root,SHA).source_sha,SHA)

    def test_git_unavailable_blocks(self):
        with patch("devtools.build_v002_candidate.subprocess.check_output",
                   side_effect=FileNotFoundError("git missing")):
            with self.assertRaises(PackageError):
                build(self.root,SHA)

    def test_corrupted_zip_data_detected(self):
        result=self.build()
        raw=bytearray(result.archive)
        # Corrupt the archived manifest header: structural verification must reject.
        offset=result.archive.find(b'RELEASE-SOURCE-MANIFEST.json')
        self.assertGreater(offset,0)
        raw[offset]=ord("X")
        with self.assertRaises((PackageError,Exception)):
            validate_archive(bytes(raw),SHA)

    def test_symlinked_skill_is_rejected(self):
        path=self.root/"skills/yellow-team/SKILL.md"
        path.unlink()
        target=self.root/"docs/CONSTITUTION.md"
        try:
            path.symlink_to(target)
        except (OSError,NotImplementedError):
            self.skipTest("symlink not supported on this environment")
        with self.assertRaises(PackageError):
            self.build()


if __name__=="__main__":
    unittest.main()
