"""Legacy snapshot regression and adversarial tests; offline stdlib-only."""
import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_idea_feature_library import validate, check_indexes, read_json
from build_idea_feature_index import render_indexes, build


class HistoricalLibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for kind in ("ideas", "features"):
            shutil.copytree(ROOT / kind, self.root / kind)

    def record(self, kind, ident):
        return self.root / kind / "records" / (ident + ".json")

    def mutate(self, kind, ident, **updates):
        file = self.record(kind, ident)
        row = json.loads(file.read_text(encoding="utf-8"))
        row.update(updates)
        file.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")

    def test_actual_historical_records_and_indexes(self):
        self.assertEqual(validate(ROOT), [])
        self.assertEqual(check_indexes(ROOT), [])

    def test_no_required_snapshot_record_count(self):
        idea_file = self.record("ideas", "IDEA-000036")
        item = read_json(idea_file)
        item["id"] = "IDEA-000037"
        item["related_ideas"] = []
        self.record("ideas", "IDEA-000037").write_text(
            json.dumps(item) + "\n", encoding="utf-8")
        feat = read_json(self.record("features", "FEAT-000001"))
        feat["id"] = "FEAT-000006"
        self.record("features", "FEAT-000006").write_text(
            json.dumps(feat) + "\n", encoding="utf-8")
        self.assertEqual(validate(self.root), [])
        build(self.root)
        self.assertEqual(check_indexes(self.root), [])

    def test_bad_reference_rejected(self):
        self.mutate("features", "FEAT-000001", idea_ids=["IDEA-999999"])
        self.assertIn("unresolved idea", " ".join(validate(self.root)))

    def test_false_verified_claim_rejected(self):
        self.mutate("features", "FEAT-000001", lifecycle_status="verified")
        self.assertIn("verified", " ".join(validate(self.root)))

    def test_false_release_claim_rejected(self):
        self.mutate("features", "FEAT-000001", release_membership="shipped")
        self.assertIn("release", " ".join(validate(self.root)).lower())

    def test_unknown_fields_rejected(self):
        self.mutate("ideas", "IDEA-000001", automatic_dispatch=True)
        self.assertIn("unknown field", " ".join(validate(self.root)))

    def test_invalid_sha_rejected(self):
        feat = read_json(self.record("features", "FEAT-000001"))
        feat["source_refs"][0]["commit"] = "not-a-sha"
        self.mutate("features", "FEAT-000001", source_refs=feat["source_refs"])
        self.assertIn("pattern mismatch", " ".join(validate(self.root)))

    def test_traversal_rejected(self):
        feat = read_json(self.record("features", "FEAT-000001"))
        feat["source_refs"][0]["path"] = "../secret"
        self.mutate("features", "FEAT-000001", source_refs=feat["source_refs"])
        self.assertIn("unsafe source path", " ".join(validate(self.root)))

    def test_stale_index_rejected(self):
        self.mutate("ideas", "IDEA-000001", title="Changed but index not updated")
        self.assertIn("stale index", " ".join(check_indexes(self.root)))

    def test_builder_is_deterministic(self):
        first = render_indexes(self.root)
        build(self.root)
        second = render_indexes(self.root)
        self.assertEqual(first, second)
        self.assertEqual(check_indexes(self.root), [])

    def test_malformed_json_rejected(self):
        self.record("ideas", "IDEA-000001").write_text("{", encoding="utf-8")
        self.assertIn("invalid JSON", " ".join(validate(self.root)))

    def test_duplicate_json_field_rejected(self):
        path = self.record("ideas", "IDEA-000001")
        path.write_text('{"id":"IDEA-000001","id":"IDEA-000001"}', encoding="utf-8")
        self.assertIn("duplicate JSON key", " ".join(validate(self.root)))

    def test_symlink_not_followed(self):
        target = self.record("ideas", "IDEA-000001")
        target.unlink()
        try:
            target.symlink_to(self.record("ideas", "IDEA-000002"))
        except (NotImplementedError, OSError):
            self.skipTest("symlinks unavailable on this host")
        self.assertIn("symlink", " ".join(validate(self.root)))

    def test_adopted_requires_decision_scope(self):
        self.mutate("ideas", "IDEA-000001", decision={"decided_by": "assistant", "reason": "model said yes", "decision_scope": "full_release"})
        self.assertIn("adopted idea without scoped decision", " ".join(validate(self.root)))

    def test_broken_relation_rejected(self):
        self.mutate("ideas", "IDEA-000001", related_ideas=["IDEA-999999"])
        self.assertIn("idea relation", " ".join(validate(self.root)))

    def test_portable_starter_is_empty_and_separate(self):
        package = ROOT / "portable" / "v0.0.1"
        for kind in ("ideas", "features"):
            self.assertEqual(list((package / kind / "records").glob("*.json")), [])
        self.assertTrue((package / "tests/test_library.py").is_file())


if __name__ == "__main__":
    unittest.main()
