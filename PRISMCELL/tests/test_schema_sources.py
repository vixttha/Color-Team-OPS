"""Schema source-of-truth audit for PrismCell v0.0.1: universal plus archival legacy."""
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'SCHEMA-SOURCES.json').read_text(encoding='utf8'))

class SchemaSourceIntegrity(unittest.TestCase):
    def test_four_schema_sources_declared(self):
        self.assertEqual(manifest['version'],'0.0.1')
        self.assertEqual(set(x['name'] for x in manifest['schemas']),{'message','project','state','work-item'})
    def test_canonical_and_public_compatibility_aliases_match_exact_bytes(self):
        for item in manifest['schemas']:
            with self.subTest(name=item['name']):
                canonical=(ROOT.parent/item['canonical']).read_bytes()
                alias=(ROOT.parent/item['alias']).read_bytes()
                self.assertEqual(canonical,alias)
    def test_all_current_schemas_valid_draft_2020_12(self):
        for item in manifest['schemas']:
            with self.subTest(name=item['name']):
                schema=json.loads((ROOT.parent/item['canonical']).read_text(encoding='utf8'))
                Draft202012Validator.check_schema(schema)
    def test_original_color_team_ops_schema_snapshots_preserved_not_active(self):
        for item in manifest['schemas']:
            with self.subTest(name=item['name']):
                original=(ROOT.parent/item['legacy_snapshot'])
                self.assertTrue(original.is_file())
                self.assertTrue(json.loads(original.read_text(encoding='utf8'))['$schema'].endswith('2020-12/schema'))
        legacy=json.loads((ROOT/'adapters/color-team-ops/legacy-schemas/project.schema.json').read_text(encoding='utf8'))
        current=json.loads((ROOT/'core/schemas/project.schema.json').read_text(encoding='utf8'))
        self.assertEqual(legacy['properties']['teams']['minProperties'],2)
        self.assertEqual(current['properties']['teams']['minProperties'],1)

if __name__=='__main__':unittest.main()
