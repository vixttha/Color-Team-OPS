"""Stdlib-only portable plugin structure and contract checks."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    "orange-team", "yellow-team", "green-team", "blue-team", "red-team",
    "purple-team", "white-team", "black-team", "gray-cell",
    "ops-director", "verification-gate", "mission-control",
}


def obj(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def validate(schema, data):
    if "const" in schema:
        assert data == schema["const"], "const violated"
    if "enum" in schema:
        assert data in schema["enum"], "enum violated"
    kind = schema.get("type")
    if kind == "object":
        assert isinstance(data, dict), "object required"
        assert set(schema.get("required", [])).issubset(data), "required missing"
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            assert set(data).issubset(properties), "unexpected properties"
        for name, value in data.items():
            if name in properties:
                validate(properties[name], value)
    elif kind == "array":
        assert isinstance(data, list), "array required"
        if schema.get("uniqueItems"):
            assert len(data) == len({json.dumps(item, sort_keys=True) for item in data})
        for item in data:
            validate(schema.get("items", {}), item)
    elif kind == "string":
        assert isinstance(data, str) and len(data) >= schema.get("minLength", 0)
    elif kind == "integer":
        assert type(data) is int
        assert schema.get("minimum", data) <= data <= schema.get("maximum", data)
    elif kind == "number":
        assert type(data) in (int, float) and data >= schema.get("minimum", data)


class PackageTests(unittest.TestCase):
    def test_manifest_identity_and_version(self):
        manifest = obj("plugin.json")
        legacy = obj(".codex-plugin/plugin.json")
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertEqual(manifest["name"], legacy["name"])
        self.assertEqual(manifest["version"], legacy["version"])
        self.assertRegex(manifest["version"], r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["displayName"], "Color Team OPS")

    def test_all_twelve_skills(self):
        paths = list((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(paths), 12)
        self.assertEqual({p.parent.name for p in paths}, ROLES)
        for path in paths:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                front = text.split("---", 2)[1]
                self.assertIn("name: " + path.parent.name, front)
                self.assertIn("description:", front)
                self.assertIn("CONSTITUTION.md", text)

    def test_json_schema_examples(self):
        for name in ("mission", "completion-event", "routing-decision"):
            with self.subTest(name=name):
                schema = obj("schemas/" + name + ".schema.json")
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                validate(schema, obj("examples/" + name + ".json"))

    def test_no_installed_local_runtime(self):
        for path in ("mcp.json", ".mcp.json", "runtime", "hooks", "bin", "Dockerfile"):
            self.assertFalse((ROOT / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
