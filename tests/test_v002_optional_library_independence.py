"""M2 runtime independence + lazy-specialist reference contract.

Uses a synthetic denial of optional-library reads; not a live plugin trial.
"""
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from policy_v002.team_directory import TeamDirectory
from policy_v002.route_advice import RouteIntent, recommend_one

ROOT=Path(__file__).resolve().parents[1]
NAMES=("yellow-team","orange-team","green-team","red-team","blue-team",
       "purple-team","white-team","black-team","gray-cell")
SHA="a"*40

class M2OptionalIndependenceTests(TestCase):
    def test_all_nine_reference_packs_exist(self):
        for team in NAMES:
            with self.subTest(team=team):
                f=ROOT/"skills"/team/"references"/"v002-competencies.md"
                self.assertTrue(f.is_file(),f)

    def test_references_have_distinct_roles_and_evidence(self):
        for team in NAMES:
            with self.subTest(team=team):
                s=(ROOT/"skills"/team/"references"/"v002-competencies.md").read_text()
                self.assertIn("Distinct engineering / operational roles",s)
                self.assertIn("Required evidence",s)
                self.assertIn("Activation guidance",s)
                self.assertIn("Exclusions and safe handoffs",s)
                self.assertIn("CAPABILITY_BLOCKED",s)

    def test_directory_search_with_optional_library_unavailable(self):
        original=Path.read_text
        def deny_library(path,*args,**kwargs):
            if any(p in ("ideas","features","portable") for p in path.parts):
                raise FileNotFoundError("intentional optional-library outage")
            return original(path,*args,**kwargs)
        with patch.object(Path,"read_text",new=deny_library):
            d=TeamDirectory()
            result=d.search(query="backend",permitted_teams=("yellow-team",),
                            available_tools=("repo-read","repo-write"))
            self.assertEqual(result.status,"CANDIDATES")
            self.assertEqual(result.matches[0].team_id,"yellow-team")

    def test_router_recommends_only_one_without_library(self):
        original=Path.read_text
        def deny_library(path,*args,**kwargs):
            if any(p in ("ideas","features","portable") for p in path.parts):
                raise FileNotFoundError("optional library unavailable")
            return original(path,*args,**kwargs)
        intent=RouteIntent(mission_id="mission-1",source_sha=SHA,observed_sha=SHA,
             mission_revision=2,observed_revision=2,
             permitted_teams=("yellow-team","orange-team"),
             required_capabilities=("yellow.regression-test",),
             available_tools=("repo-read",),task_text="regression test",
             active_worker=None,prior_gate_status="VALIDATED_AND_AUDITED",
             dispatch_count=1,max_handoffs=2,forbidden_capabilities=())
        with patch.object(Path,"read_text",new=deny_library):
            outcome=recommend_one(intent,directory=TeamDirectory())
            self.assertEqual(outcome.status,"SUGGEST_ONLY")
            self.assertEqual(outcome.suggested_team,"yellow-team")
            self.assertNotEqual(outcome.code,"AUTHORIZED")

    def test_unchanged_nine_skills_plus_three_coordinators(self):
        self.assertEqual({p.parent.name for p in (ROOT/"skills").glob("*/SKILL.md")},
          set(NAMES)|{"mission-control","ops-director","verification-gate"})

    def test_ops_director_declares_lazy_loading_only(self):
        s=(ROOT/"skills"/"ops-director"/"SKILL.md").read_text()
        self.assertIn("only that team's",s)
        self.assertIn("when the supported host actually exposes bundled references",s)
        self.assertIn("never fabricate",s)

if __name__=="__main__":
    import unittest
    unittest.main()
