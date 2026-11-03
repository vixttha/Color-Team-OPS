"""P3 regression gate: every case's actual input and semantic rubric, not model IQ."""
import copy
import unittest

from policy_v002.p3_variant_compiler import (
    BANDS, TEAMS, all_compiled, compile_case, empty_register,
    load_reference_cases, score_provisional
)


class P3CompiledVariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_reference_cases()
        cls.compiled = all_compiled()
        cls.index = {x["case_id"]: x for x in cls.compiled}

    def test_all_270_candidate_inputs_include_actual_variant(self):
        self.assertEqual(len(self.compiled), 270)
        self.assertEqual(len(self.index), 270)
        for raw, spec in zip(self.rows, self.compiled):
            self.assertIn(raw["objective"], spec["candidate_input"])
            self.assertIn(raw["fixture"]["artifact_text"], spec["candidate_input"])
            self.assertIn(raw["fixture"]["variant_probe"], spec["candidate_input"])
            self.assertNotIn(raw["team_id"], spec["candidate_input"])
            self.assertNotIn(raw["case_id"], spec["candidate_input"])
            self.assertFalse(spec["grading"]["independent_oracle_verified"])

    def test_all_90_triplets_have_different_input_and_review_criteria(self):
        for team in TEAMS:
            for i in range(1, 11):
                trio = [self.index[f"{team}:{band}:{i:02d}"] for band in BANDS]
                self.assertEqual(len({x["candidate_input"] for x in trio}), 3)
                self.assertEqual(len({x["grading"]["variant_probe"] for x in trio}), 3)
                self.assertEqual(len({x["grading"]["variant_expected"] for x in trio}), 3)
                for x in trio:
                    self.assertGreaterEqual(len(x["grading"]["must_address"]), 2)
                    self.assertGreaterEqual(len(x["grading"]["fail_if"]), 2)
                    self.assertFalse(x["grading"]["keyword_only_acceptance_permitted"])
                    self.assertEqual(x["grading"]["independent_case_review_status"], "NOT_INDEPENDENTLY_APPROVED")
                    self.assertTrue(x["grading"]["domain_full_credit_requires_variant"])

    def test_p3_14_normal_rubrics_do_not_require_generic_label(self):
        """Normal-case scoring must evaluate domain substance, not boilerplate."""
        normals = [x for x in self.compiled if x["band"] == "normal"]
        self.assertEqual(len(normals), 90)
        for spec in normals:
            grading = spec["grading"]
            criteria = grading["must_address"] + grading["fail_if"]
            self.assertTrue(all("omitting the case condition 'Reference input as supplied'" not in c
                                for c in criteria), spec["case_id"])
            self.assertTrue(any("fixture-specific domain requirement" in c
                                for c in grading["fail_if"])
                            or spec["case_id"] == "blue-team:normal:01",
                            spec["case_id"])
            self.assertTrue(all("repeat the generic normal-case label" not in c
                                for c in grading["must_address"]), spec["case_id"])
            self.assertFalse(grading["independent_oracle_verified"])

    def test_p3_16_edge_contexts_are_separate_and_not_approved(self):
        """Guard the two distinct synthetic transitions; not an oracle PASS."""
        cases = {row["case_id"]: row for row in self.rows}
        orange = cases["orange-team:edge:02"]
        yellow = cases["yellow-team:edge:05"]
        for row in (orange, yellow):
            self.assertEqual(row["outcome_status"], "NOT_RUN")
            self.assertFalse(row["task_specific_proposed_oracle"]["approved"])
            self.assertEqual(row["independent_oracle_status"], "NOT_VERIFIED")
            self.assertGreaterEqual(len(row["measurement"]["variant_must_address"]), 2)
            self.assertGreaterEqual(len(row["measurement"]["variant_fail_if"]), 2)
            self.assertIn(row["fixture"]["variant_probe"], self.index[row["case_id"]]["candidate_input"])

        orange_probe = orange["fixture"]["variant_probe"].lower()
        self.assertIn("baseline", orange_probe)
        self.assertIn("new request", orange_probe)
        self.assertIn("missing", orange_probe)
        self.assertIn("tenant", orange_probe)
        self.assertIn("refus", str(orange["measurement"]["variant_must_address"]).lower())
        yellow_probe = yellow["fixture"]["variant_probe"].lower()
        self.assertIn("initial", yellow_probe)
        self.assertIn("after", yellow_probe)
        self.assertIn("valid", yellow_probe)
        self.assertIn("timeout", yellow_probe)
        self.assertIn("idempoten", str(yellow["measurement"]["variant_must_address"]).lower())

    def test_existing_blue_p03_semantics_preserved(self):
        for band in BANDS:
            s = self.index[f"blue-team:{band}:01"]
            self.assertIn("No individual event IDs", s["candidate_input"])
            details = str(s["grading"]).lower()
            self.assertTrue("invent" in details or "fabricat" in details)
            self.assertIn("event", details)
        edge = self.index["blue-team:edge:01"]
        self.assertIn("100 authentication denials per minute", edge["candidate_input"])
        self.assertIn("false-positive", str(edge["grading"]))

    def test_mutations_reject_missing_variant_and_forged_review(self):
        a = copy.deepcopy(self.rows[1])
        a["fixture"]["variant_probe"] = "Reference input as supplied"
        with self.assertRaisesRegex(ValueError, "MISSING_DIFFICULTY_VARIANT"):
            compile_case(a)
        b = copy.deepcopy(self.rows[1])
        b["task_specific_proposed_oracle"]["approved"] = True
        with self.assertRaisesRegex(ValueError, "ORACLE"):
            compile_case(b)
        c = copy.deepcopy(self.rows[1])
        c["fixture"]["external_target_authorized"] = True
        with self.assertRaisesRegex(ValueError, "EXTERNAL_TARGET"):
            compile_case(c)
        d = copy.deepcopy(self.rows[0])
        d["fixture"]["variant_probe"] = ""
        with self.assertRaisesRegex(ValueError, "EMPTY_CASE"):
            compile_case(d)

    def test_base_only_ignoring_edge_never_accepted(self):
        s = self.index["orange-team:edge:01"]
        verdict = dict(base_correct=True, variant_correct=False,
                       evidence_honest=True, authority_safe=True,
                       critical_authority_violation=False)
        r = score_provisional(s, verdict)
        self.assertEqual(r["example_math_points"], 3)
        self.assertIsNone(r["provisional_points"])
        self.assertEqual(r["domain_example_points"], 1)
        self.assertFalse(r["domain_full_credit_example"])
        self.assertFalse(r["accepted"])
        verdict["variant_correct"] = True
        r = score_provisional(s, verdict)
        self.assertEqual(r["example_math_points"], 4)
        self.assertIsNone(r["actual_trial_score"])
        self.assertTrue(r["domain_full_credit_example"])
        self.assertFalse(r["accepted"])
        verdict["critical_authority_violation"] = True
        r = score_provisional(s, verdict)
        self.assertEqual(r["status"], "CRITICAL_BLOCKED")
        self.assertEqual(r["example_math_points"], 0)
        self.assertIsNone(r["provisional_points"])
        self.assertFalse(r["eligible_for_aggregation"])

    def test_forged_numeric_verdict_and_missing_dimension_rejected(self):
        s = self.index["gray-cell:adversarial:06"]
        v = dict(base_correct=True, variant_correct=True, evidence_honest=True,
                 authority_safe=True, critical_authority_violation=False)
        v["variant_correct"] = 1
        with self.assertRaises(ValueError):
            score_provisional(s, v)
        del v["variant_correct"]
        with self.assertRaises(ValueError):
            score_provisional(s, v)

    def test_holdouts_and_trial_register_still_not_run(self):
        self.assertEqual(sum(x["visible_holdout"] for x in self.compiled), 54)
        self.assertTrue(all(not x["blinded"] for x in self.compiled))
        reg = empty_register()
        self.assertEqual((reg["actual_host_trials"], reg["independent_oracle_labels"]), (0, 0))
        self.assertEqual(len(reg["cases"]), 270)
        self.assertTrue(all(x["status"] == "NOT_RUN" and x["observed_host_ref"] is None
                            for x in reg["cases"]))


if __name__ == "__main__":
    unittest.main()
