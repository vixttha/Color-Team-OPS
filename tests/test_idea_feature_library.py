"""Developer-only stdlib tests for canonical idea and feature records; not plugin runtime."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from check_idea_feature_library import validate

class IdeaFeatureLibraryTests(unittest.TestCase):
    def test_registry_structural_integrity(self):
        self.assertEqual(validate(),[])
    def test_no_release_claims(self):
        for p in (ROOT/"features"/"records").glob("*.json"):
            data=json.loads(p.read_text(encoding="utf-8"))
            self.assertEqual(data["release_membership"],"NOT_ASSERTED")
            self.assertEqual(data["verified_evidence"],[])
    def test_adopted_ideas_do_not_claim_implementation(self):
        for p in (ROOT/"ideas"/"records").glob("*.json"):
            d=json.loads(p.read_text(encoding="utf-8"))
            if d["lifecycle_status"]=="adopted":
                self.assertEqual(d["decision"]["decision_scope"],"idea_direction_only")
                self.assertEqual(d["implementation_status"],"not_planned")

if __name__=="__main__":unittest.main()
