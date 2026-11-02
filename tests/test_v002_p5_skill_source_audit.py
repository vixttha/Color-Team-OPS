"""Source skill audit, not actual hosted skill activation."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEAMS=("yellow-team","orange-team","green-team","red-team","blue-team",
       "purple-team","white-team","black-team","gray-cell")
COORD=("mission-control","ops-director","verification-gate")
class SkillSourceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads((ROOT/"docs"/"V002-P5-SKILL-LEVEL-AUDIT.json").read_text(encoding="utf8"))
    def test_exactly_twelve_skills(self):
        self.assertEqual({p.parent.name for p in (ROOT/"skills").glob("*/SKILL.md")},set(TEAMS)|set(COORD))
        self.assertEqual(len(self.a["specialists"]),9)
    def test_nine_competency_refs_and_boundaries(self):
        for team in TEAMS:
            s=(ROOT/"skills"/team/"SKILL.md").read_text(encoding="utf8")
            r=(ROOT/"skills"/team/"references"/"v002-competencies.md").read_text(encoding="utf8")
            for field in ("## Trigger","## Procedure","## Deliverable","Obey `docs/CONSTITUTION.md`"):
                self.assertIn(field,s,team)
            self.assertIn("## Distinct engineering / operational roles",r)
            self.assertIn("## One-lane execution",r)
            self.assertGreaterEqual(len([line for line in r.splitlines()
                if line[:1].isdigit() and ". " in line]),3,team)
    def test_coordinators_head_rules(self):
        mc=(ROOT/"skills"/"mission-control"/"SKILL.md").read_text(encoding="utf8")
        op=(ROOT/"skills"/"ops-director"/"SKILL.md").read_text(encoding="utf8")
        vg=(ROOT/"skills"/"verification-gate"/"SKILL.md").read_text(encoding="utf8")
        self.assertIn("one active Worker",mc)
        self.assertIn("bounded mission budget exhausted",mc)
        self.assertIn("CAPABILITY_BLOCKED",mc)
        self.assertIn("NOT_RUN",mc)
        self.assertIn("Built-in compact team capability directory",op)
        self.assertIn("Internal Auditor",vg)
    def test_source_evidence_not_real_host(self):
        self.assertTrue(all(x["host_activation"]=="NOT_RUN" for x in
                    self.a["specialists"]+self.a["coordinators"]))
        self.assertTrue(all(x["reference_host_load"]=="NOT_RUN"
                            for x in self.a["specialists"]))
        self.assertTrue(self.a["no_new_skills"])
if __name__=="__main__":unittest.main()
