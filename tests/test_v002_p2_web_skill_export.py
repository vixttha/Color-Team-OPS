"""Optional per-skill ZIP source parity; not host installed test."""
import io, tempfile, unittest, zipfile
from pathlib import Path
from devtools.export_v002_web_skills import export_skill, SKILLS, SPECIALISTS
ROOT=Path(__file__).resolve().parents[1]
SHA="a"*40
class PortableSkillExporterTests(unittest.TestCase):
    def test_twelve_deterministic_individual_exports(self):
        for name in SKILLS:
            first,d1=export_skill(ROOT,name,SHA)
            second,d2=export_skill(ROOT,name,SHA)
            self.assertEqual((first,d1),(second,d2),name)
            with zipfile.ZipFile(io.BytesIO(first)) as z:
                files=z.namelist()
                self.assertIn(f"{name}/SKILL.md",files)
                self.assertIn(f"{name}/docs/CONSTITUTION.md",files)
                self.assertIn(f"{name}/registry/v0.0.2/teams.json",files)
                self.assertEqual(len([f for f in files if "/schemas/" in f]),3)
                self.assertEqual(any("/references/v002-competencies.md" in f for f in files),
                                 name in SPECIALISTS)
                self.assertTrue(all(f.startswith(name+"/") for f in files))
    def test_unapproved_thirteenth_skill_rejected(self):
        with self.assertRaises(ValueError):
            export_skill(ROOT,"gold-team",SHA)
    def test_bad_sha_rejected(self):
        with self.assertRaises(ValueError):
            export_skill(ROOT,"yellow-team","not-a-sha")
    def test_source_files_required(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                export_skill(Path(temp),"yellow-team",SHA)
    def test_never_requires_local_executor_in_skill(self):
        for name in SKILLS:
            with zipfile.ZipFile(io.BytesIO(export_skill(ROOT,name,SHA)[0])) as z:
                text=z.read(f"{name}/SKILL.md").decode()
                self.assertIn("Cloud-only",text)
                self.assertIn("never require",text.lower())
    def test_no_implicit_host_installation_field(self):
        for name in SKILLS:
            with zipfile.ZipFile(io.BytesIO(export_skill(ROOT,name,SHA)[0])) as z:
                self.assertNotIn("plugin.json",z.namelist())
                self.assertFalse(any(f.endswith(".py") for f in z.namelist()))
if __name__=="__main__":unittest.main()
