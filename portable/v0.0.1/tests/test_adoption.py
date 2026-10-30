"""Unrelated-project adoption and no-clobber acceptance tests (offline)."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "tools"))
import adopt
import library


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "unrelated-product"
        self.project.mkdir()
        (self.project / "AGENTS.md").write_text("UNRELATED_HOST_POLICY\n", encoding="utf-8")
        (self.project / "README.md").write_text("Unrelated application\n", encoding="utf-8")

    def test_clean_unrelated_project_without_tools(self):
        copied = adopt.adopt(self.project)
        self.assertEqual(len(copied), 4)
        self.assertEqual((self.project / "AGENTS.md").read_text(), "UNRELATED_HOST_POLICY\n")
        self.assertEqual((self.project / "README.md").read_text(), "Unrelated application\n")
        self.assertEqual(list((self.project / "ideas/records").glob("*.json")), [])
        self.assertEqual(list((self.project / "features/records").glob("*.json")), [])
        self.assertFalse((self.project / "tools").exists())

    def test_optional_tooling_runs_on_unrelated_host(self):
        adopt.adopt(self.project, with_tools=True)
        self.assertEqual(library.run(self.project, "check"), 0)
        self.assertEqual(library.run(self.project, "build"), 0)

    def test_existing_idea_directory_blocks_all_copy(self):
        (self.project / "ideas").mkdir()
        (self.project / "ideas" / "user.txt").write_text("owner data")
        with self.assertRaises(FileExistsError):
            adopt.adopt(self.project)
        self.assertEqual((self.project / "ideas/user.txt").read_text(), "owner data")
        self.assertFalse((self.project / "features").exists())

    def test_existing_agent_guide_blocks_all_copy(self):
        (self.project / "LIBRARY-AGENT-GUIDE.md").write_text("do not overwrite")
        with self.assertRaises(FileExistsError):
            adopt.adopt(self.project)
        self.assertEqual((self.project / "LIBRARY-AGENT-GUIDE.md").read_text(), "do not overwrite")
        self.assertFalse((self.project / "ideas").exists())

    def test_repeated_installation_never_clobbers(self):
        adopt.adopt(self.project)
        text = (self.project / "ideas/README.md").read_text()
        with self.assertRaises(FileExistsError):
            adopt.adopt(self.project)
        self.assertEqual((self.project / "ideas/README.md").read_text(), text)

    def test_symlink_destination_rejected(self):
        other = Path(self.temp.name) / "outside"
        other.mkdir()
        try:
            (self.project / "features").symlink_to(other, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        with self.assertRaises(FileExistsError):
            adopt.adopt(self.project)
        self.assertEqual(list(other.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
