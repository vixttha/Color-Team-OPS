"""v0.0.2 installed-skill continuity and release identity regression checks.

These are file-contract checks, NOT authenticated host skill mission trials.
"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TEAMS={"yellow-team","orange-team","green-team","blue-team","red-team",
       "purple-team","white-team","black-team","gray-cell"}
COORD={"mission-control","ops-director","verification-gate"}
V001_TEAM_BLOBS={
 "black-team":"8669e3db2910b608ea583e973348e473d2a35f44",
 "blue-team":"b61cecb82d00c642dcdc1239b8e23d60c9506e3e",
 "gray-cell":"45b453b1c6ae568ccd7833ced2067aea31f16f87",
 "green-team":"8b0fcb47d8488ef72ae0db5427cd81ea406c118e",
 "orange-team":"22d5bf13e05d8295c0c7c20e1ea5d543fdc631db",
 "purple-team":"6ec440dd83b834e201e8892ed4598a25d5b45860",
 "red-team":"a382fae6ef41ca3487fc4ff76e321553f3ec6108",
 "white-team":"06c9a10ff7ffaa3a4b65effe44ddd36a180e28b6",
 "yellow-team":"322035806be2579bfee13791fb19963eaa7b8cf0"
}
V001_COORD_BLOBS={
 "mission-control":"d356113c5169ca4818c0dbb8a7c4f95de9c7ac7f",
 "ops-director":"f06b71585db13598e8be794062a8178817be0082",
 "verification-gate":"2dd966c7bdfbf6f3b35d0f321b8b684b4a1ef658"
}

def skill(name):
    return (ROOT/"skills"/name/"SKILL.md").read_text(encoding="utf-8")

def git_blob_hash(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

class V002SkillContinuity(unittest.TestCase):
    def test_exactly_twelve_and_no_new_roles(self):
        names={p.parent.name for p in (ROOT/"skills").glob("*/SKILL.md")}
        self.assertEqual(names,TEAMS|COORD)

    def test_all_skill_frontmatter_and_constitution_preserved(self):
        for name in sorted(TEAMS|COORD):
            with self.subTest(name=name):
                text=skill(name)
                self.assertTrue(text.startswith("---\n"))
                self.assertIn("\n---\n",text)
                self.assertIn(f"name: {name}",text.split("---",2)[1])
                self.assertIn("description:",text.split("---",2)[1])
                self.assertIn("docs/CONSTITUTION.md",text)
                self.assertIn("Cloud-only",text)
                self.assertIn("never require or invoke user-owned hardware",text)

    def test_all_nine_specialist_files_exactly_v001(self):
        for name,expected in V001_TEAM_BLOBS.items():
            with self.subTest(name=name):
                path=ROOT/"skills"/name/"SKILL.md"
                self.assertEqual(git_blob_hash(path.read_bytes()),expected)

    def test_only_three_coordinators_intentionally_updated(self):
        for name,original in V001_COORD_BLOBS.items():
            with self.subTest(name=name):
                path=ROOT/"skills"/name/"SKILL.md"
                self.assertNotEqual(git_blob_hash(path.read_bytes()),original)
                self.assertIn("v0.0.2",skill(name))

    def test_one_thread_without_routine_user_prompts(self):
        self.assertIn("do not ask the user to approve routine internal",skill("mission-control"))
        self.assertIn("same thread",skill("ops-director"))
        self.assertIn("without prompting the user",skill("verification-gate"))

    def test_one_active_worker_and_no_fixed_nine_team_queue(self):
        self.assertIn("one active Worker",skill("mission-control"))
        self.assertIn("at most one",skill("ops-director"))
        self.assertIn("Do not force all nine teams",skill("ops-director"))

    def test_verification_is_distinct_not_fake_human(self):
        text=skill("verification-gate")
        self.assertIn("Internal Auditor",text)
        self.assertIn("not proof of separate authenticated human",text)
        self.assertIn("NOT RUN",text)
        self.assertIn("UNVERIFIED",text)

    def test_no_synthetic_host_promotion(self):
        for name in COORD:
            with self.subTest(name=name):
                self.assertIn("synthetic",skill(name).lower())
        self.assertIn("CAPABILITY_BLOCKED",skill("mission-control"))

    def test_no_automatic_merge_or_publication(self):
        for name in ("mission-control","verification-gate"):
            text=skill(name).lower()
            self.assertIn("merge",text)
            self.assertTrue("publish" in text or "publication" in text)

    def test_manifest_identity_stable_at_candidate_version(self):
        manifest=json.loads((ROOT/"plugin.json").read_text(encoding="utf-8"))
        compat=json.loads((ROOT/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"],"color-team-ops")
        self.assertEqual((manifest["version"],compat["version"]),("0.0.2","0.0.2"))
        self.assertEqual(compat["name"],manifest["name"])

    def test_directory_references_are_optional_not_new_skills(self):
        text=skill("ops-director")
        self.assertIn("when actually available in the host",text)
        self.assertIn("never assume those Python files execute inside ChatGPT",text)
        self.assertIn("recommendation-only",text)
        self.assertIn("Head",text)

if __name__=="__main__":unittest.main()
