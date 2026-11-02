"""P2 five-host source matrix: documentation compatibility is never host trial."""
import json
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"docs"/"V002-P2-WEB-HOST-COMPATIBILITY.json"

class WebHostMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.d=json.loads(P.read_text(encoding="utf8"))
    def test_five_distinct_browser_hosts(self):
        self.assertEqual({x["name"] for x in self.d["providers"]},
                         {"ChatGPT","Claude","Grok","Kimi","Z.ai"})
    def test_all_are_documentation_only(self):
        self.assertEqual(self.d["candidate_host_trials_executed"],0)
        self.assertTrue(all(not x["host_tried"] for x in self.d["providers"]))
        self.assertTrue(all(x["sources"] and
            all(s.startswith("https://") for s in x["sources"]) for x in self.d["providers"]))
    def test_zcode_not_zai_web_certification(self):
        zai=next(x for x in self.d["providers"] if x["name"]=="Z.ai")
        self.assertIn("UNVERIFIED",zai["custom_plugin"])
    def test_no_required_desktop(self):
        self.assertTrue(all(x["website"].startswith("https://") for x in self.d["providers"]))
        self.assertIn("NO",self.d["source_only_bundle_status"])

if __name__=="__main__": unittest.main()
