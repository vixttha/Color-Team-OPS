"""M2/M5 idea/feature library preservation checks.

Records are historical proposal metadata. Their presence does not certify
features, approve code, authenticate users or grant release membership.
"""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
IDEAS=ROOT/"ideas"/"records"
FEATURES=ROOT/"features"/"records"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

class LibraryPreservationTests(unittest.TestCase):
    def test_exact_36_idea_identifiers(self):
        paths=sorted(IDEAS.glob("IDEA-*.json"))
        self.assertEqual([p.stem for p in paths],
            [f"IDEA-{i:06d}" for i in range(1,37)])

    def test_exact_five_candidate_feature_identifiers(self):
        paths=sorted(FEATURES.glob("FEAT-*.json"))
        self.assertEqual([p.stem for p in paths],
            [f"FEAT-{i:06d}" for i in range(1,6)])

    def test_adopted_idea_is_not_implemented_or_shipped(self):
        rows=[load(p) for p in IDEAS.glob("*.json")]
        adopted=[i for i in rows if i.get("lifecycle_status")=="adopted"]
        self.assertEqual(len(adopted),5)
        self.assertTrue(all(i["implementation_status"]=="not_planned" for i in rows))
        self.assertTrue(all(i["schema_version"]==1 for i in rows))

    def test_idea_states_are_only_source_claims(self):
        rows=[load(p) for p in IDEAS.glob("*.json")]
        self.assertEqual({x["lifecycle_status"] for x in rows},
                         {"captured","adopted"})
        self.assertTrue(all(isinstance(x.get("evidence"),list) for x in rows))

    def test_feature_registry_all_proposed(self):
        rows=[load(p) for p in FEATURES.glob("*.json")]
        for x in rows:
            with self.subTest(feature=x["id"]):
                self.assertEqual(x["lifecycle_status"],"proposed")
                self.assertEqual(x["implementation_status"],"not_planned")
                self.assertEqual(x["release_membership"],"NOT_ASSERTED")
                self.assertEqual(x["verified_evidence"],[])
                self.assertEqual(x["schema_version"],1)

    def test_feature_to_idea_references_exist(self):
        ids={load(p)["id"] for p in IDEAS.glob("*.json")}
        for path in FEATURES.glob("*.json"):
            x=load(path)
            self.assertTrue(x["idea_ids"],path)
            self.assertEqual(len(x["idea_ids"]),len(set(x["idea_ids"])))
            self.assertTrue(set(x["idea_ids"]).issubset(ids),path)

    def test_indexes_are_marked_generated_not_owners(self):
        self.assertIn("generated", (ROOT/"ideas"/"INDEX.md").read_text().lower())
        self.assertIn("generated", (ROOT/"features"/"INDEX.md").read_text().lower())

    def test_json_schemas_are_present(self):
        for path in ("ideas/schema/v1/idea.schema.json",
                     "features/schema/v1/feature.schema.json"):
            schema=load(ROOT/path)
            self.assertEqual(schema["$schema"],
                             "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(schema["properties"]["schema_version"]["const"],1)

if __name__=="__main__":
    unittest.main()
