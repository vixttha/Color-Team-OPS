"""M2 nine-team directory unit tests: metadata only, not real grants."""
import copy
import json
import unittest
from pathlib import Path
from policy_v002.team_directory import TeamDirectory, RegistryRejected, EXPECTED_TEAMS, VERSION

ROOT=Path(__file__).resolve().parents[1] / "registry" / "v0.0.2" / "teams.json"

def raw():
    return json.loads(ROOT.read_text(encoding="utf-8"))

class DirectoryTests(unittest.TestCase):
    def setUp(self):
        self.doc=raw()
        self.directory=TeamDirectory()
    def rejects(self, mutate):
        mutate(self.doc)
        with self.assertRaises(RegistryRejected):
            TeamDirectory(self.doc)
    def test_nine_exact_team_ids(self):
        self.assertEqual(set(self.directory.teams()),EXPECTED_TEAMS)
    def test_registry_version(self):
        self.assertEqual(VERSION,"cto-v002-registry-1")
    def test_18_unique_capabilities(self):
        c=[x["id"] for t in self.doc["teams"] for x in t["capabilities"]]
        self.assertEqual(len(c),18)
        self.assertEqual(len(c),len(set(c)))
    def test_one_playbook_pointer_only(self):
        self.assertEqual(self.directory.playbook_ref("yellow-team"),"skills/yellow-team/SKILL.md")
    def test_unknown_team_has_no_playbook(self):
        self.assertIsNone(self.directory.playbook_ref("gold-team"))
    def test_search_requires_explicit_allowed_teams(self):
        result=self.directory.search(query="backend",permitted_teams=())
        self.assertEqual((result.status,len(result.matches)),("ABSTAIN",0))
    def test_yellow_backend_discovery(self):
        out=self.directory.search(query="backend",permitted_teams=("yellow-team",))
        self.assertEqual(out.matches[0].capability_id,"yellow.feature-build")
        self.assertEqual(out.status,"CAPABILITY_BLOCKED")
    def test_missing_tools_not_inferred(self):
        out=self.directory.search(query="backend",permitted_teams=("yellow-team",))
        self.assertEqual(out.matches[0].status,"TOOL_ACCESS_UNVERIFIED")
        self.assertIn("repo-write",out.matches[0].missing_tools)
    def test_tools_explicitly_supplied_candidate_only(self):
        out=self.directory.search(query="backend",permitted_teams=("yellow-team",),
                                  available_tools=("repo-read","repo-write"))
        self.assertEqual(out.status,"CANDIDATES")
        self.assertEqual(out.matches[0].status,"CANDIDATE_ONLY")
    def test_yellow_never_recommends_orange_when_disallowed(self):
        out=self.directory.search(query="authorization",permitted_teams=("yellow-team",))
        self.assertEqual(out.status,"ABSTAIN")
    def test_auth_review_routes_to_orange_metadata(self):
        out=self.directory.search(query="oauth",permitted_teams=("orange-team",),
                                  available_tools=("repo-read",))
        self.assertEqual(out.matches[0].capability_id,"orange.auth-review")
    def test_gray_cell_is_not_gold_or_silver(self):
        out=self.directory.search(query="accessibility",permitted_teams=("gray-cell",))
        self.assertEqual(out.matches[0].team_id,"gray-cell")
    def test_white_is_not_internal_auditor(self):
        self.assertNotIn("internal-auditor",self.directory.teams())
    def test_required_capability_can_find_no_keyword(self):
        out=self.directory.search(query="",permitted_teams=("yellow-team",),
                                  required_capabilities=("yellow.regression-test",),
                                  available_tools=("repo-read",))
        self.assertEqual(out.matches[0].capability_id,"yellow.regression-test")
    def test_wrong_required_capability_abstains(self):
        out=self.directory.search(query="backend",permitted_teams=("yellow-team",),
                                  required_capabilities=("orange.auth-review",))
        self.assertEqual(out.status,"ABSTAIN")
    def test_unapproved_team_rejected_at_search(self):
        with self.assertRaises(RegistryRejected):
            self.directory.search(query="build",permitted_teams=("gold-team",))
    def test_repeated_team_not_accepted(self):
        with self.assertRaises(RegistryRejected):
            self.directory.search(query="build",permitted_teams=("yellow-team","yellow-team"))
    def test_invalid_limit_fails(self):
        with self.assertRaises(RegistryRejected):
            self.directory.search(query="build",permitted_teams=("yellow-team",),limit=0)
    def test_limit_is_bounded(self):
        out=self.directory.search(query="test",permitted_teams=tuple(EXPECTED_TEAMS),
                                  available_tools=(),limit=1)
        self.assertLessEqual(len(out.matches),1)
    def test_missing_ninth_team(self):
        self.rejects(lambda d:d["teams"].pop())
    def test_duplicated_team_id(self):
        self.rejects(lambda d:d["teams"][0].update(id="orange-team"))
    def test_malformed_team_id_not_crash(self):
        self.rejects(lambda d:d["teams"][0].update(id=["yellow-team"]))
    def test_wrong_playbook_cross_team(self):
        self.rejects(lambda d:d["teams"][0].update(playbook_ref="skills/orange-team/SKILL.md"))
    def test_path_traversal_blocked(self):
        self.rejects(lambda d:d["teams"][0].update(playbook_ref="../../secrets"))
    def test_extra_privilege_property_blocked(self):
        self.rejects(lambda d:d["teams"][0].update(granted_tokens=True))
    def test_duplicate_capability_id_blocked(self):
        self.rejects(lambda d:d["teams"][0]["capabilities"].append(
            copy.deepcopy(d["teams"][0]["capabilities"][0])))
    def test_foreign_capability_id_blocked(self):
        self.rejects(lambda d:d["teams"][0]["capabilities"][0].update(id="orange.auth-review"))
    def test_invalid_tool_requirement_record(self):
        self.rejects(lambda d:d["teams"][0]["capabilities"][0].update(requires_tools=["ROOT_ACCESS!"]))
    def test_boolean_schema_version_blocked(self):
        self.rejects(lambda d:d.update(schema_version=True))
    def test_no_cloud_vendor_required(self):
        body=ROOT.read_text(encoding="utf-8").lower()
        self.assertNotIn("vercel",body)
        self.assertNotIn("supabase",body)
        self.assertNotIn("owner-runner",body)
    def test_registry_metadata_not_grants(self):
        self.assertEqual(self.doc["source_classification"],"development_metadata_not_grants")

if __name__=="__main__":
    unittest.main()
