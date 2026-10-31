"""Keep the installed Markdown Head routing map aligned with the reference registry.

A Python test enforces source consistency; the actual installed skill can use
the plain Markdown map without loading or executing any Python module.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "v0.0.2" / "teams.json"
OPS = ROOT / "skills" / "ops-director" / "SKILL.md"
TEAMS = ROOT / "skills"


def mirror_errors(text, registry):
    start = "## Built-in compact team capability directory (skills-only fallback)"
    end = "## Lazy specialist competency reference (v0.0.2 candidate)"
    if start not in text or end not in text:
        return ["missing standalone host directory"]
    section = text.split(start, 1)[1].split(end, 1)[0]
    errors = []
    for team in registry["teams"]:
        for capability in team["capabilities"]:
            token = "`" + capability["id"] + "`"
            if section.count(token) != 1:
                errors.append(capability["id"])
    return errors


class OpsDirectorHostFallbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.markdown = OPS.read_text(encoding="utf-8")

    def test_all_18_capability_ids_mirrored_exactly_once(self):
        self.assertEqual(len(self.data["teams"]), 9)
        self.assertEqual(sum(len(t["capabilities"]) for t in self.data["teams"]), 18)
        self.assertEqual(mirror_errors(self.markdown, self.data), [])

    def test_each_team_keeps_exactly_two_canonical_ids(self):
        self.assertEqual(len({t["id"] for t in self.data["teams"]}), 9)
        self.assertTrue(all(len(t["capabilities"]) == 2 for t in self.data["teams"]))
        self.assertEqual(len({c["id"] for t in self.data["teams"]
                              for c in t["capabilities"]}), 18)

    def test_detects_missing_host_fallback_capability(self):
        token = "`yellow.regression-test`"
        self.assertIn(token, self.markdown)
        self.assertEqual(
            mirror_errors(self.markdown.replace(token, "missing-capability"), self.data),
            ["yellow.regression-test"],
        )

    def test_red_guard_requires_explicit_authority(self):
        self.assertIn("Explicit owner-approved target", self.markdown)
        self.assertIn("Red's offensive actions need explicit scoped authorization", self.markdown)

    def test_roles_not_issuers_and_python_optional(self):
        self.assertIn("role descriptions, not tool grants", self.markdown)
        self.assertIn("when the host cannot retrieve the optional registry or execute Python",
                      self.markdown)
        self.assertIn("Head alone", self.markdown)
        self.assertIn("CAPABILITY_BLOCKED", self.markdown)

    def test_exactly_nine_specialists_three_coordinators(self):
        actual = {p.parent.name for p in TEAMS.glob("*/SKILL.md")}
        expected = {t["id"] for t in self.data["teams"]} | {
            "mission-control", "ops-director", "verification-gate",
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
