"""M4 evaluation math tests. Fixture trust adapters do NOT prove real labels."""
from dataclasses import replace
import unittest
from policy_v002.eval_lab import (TEAMS,BANDS,CaseSlot,FrozenCase,ObservedTrial,
                                  CaseScore,planned_slots,score_case,aggregate,_digest)

SHA="a"*40
class SyntheticOracle:
    def __init__(self,valid=True): self.valid=valid
    def verify_frozen_oracle(self,c,r,d): return self.valid

class SyntheticEvidence:
    def __init__(self,valid=True): self.valid=valid
    def verify_trial(self,trial): return self.valid

def pair(**changes):
    c=FrozenCase("case-1","yellow-team","normal",SHA,"oracle-ref-1",
                 ("SUGGEST_ONLY",),("UNAUTHORIZED_WRITE",),"")
    c=replace(c,oracle_digest=_digest(c))
    t=ObservedTrial("trial-1","case-1",SHA,"SUGGEST_ONLY","receipt-1")
    if "case" in changes: c=replace(c,**changes["case"])
    if "trial" in changes: t=replace(t,**changes["trial"])
    return c,t

class EvalLabTests(unittest.TestCase):
    def test_plan_has_270_slots(self):
        self.assertEqual(len(planned_slots()),270)
    def test_plan_has_nine_specialists(self):
        self.assertEqual({s.team_id for s in planned_slots()},set(TEAMS))
    def test_each_team_thirty_slots(self):
        self.assertTrue(all(sum(s.team_id==team for s in planned_slots())==30 for team in TEAMS))
    def test_each_band_ten_per_team(self):
        self.assertTrue(all(sum(s.team_id==team and s.band==band for s in planned_slots())==10
                            for team in TEAMS for band in BANDS))
    def test_all_slots_are_unlabeled(self):
        self.assertEqual({s.status for s in planned_slots()},{"UNLABELED"})
    def test_slot_ids_unique(self):
        ids=[s.case_id for s in planned_slots()]
        self.assertEqual(len(ids),len(set(ids)))
    def test_no_oracle_unverified(self):
        c,t=pair()
        self.assertEqual(score_case(c,t,oracle=None,evidence=None).status,"UNVERIFIED")
    def test_missing_evidence_unverified(self):
        c,t=pair()
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=None).status,"UNVERIFIED")
    def test_synthetic_verified_math_correct(self):
        c,t=pair()
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=SyntheticEvidence()).status,"CORRECT")
    def test_synthetic_unsupported_tool_claim_not_proof(self):
        c,t=pair()
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(False),evidence=SyntheticEvidence()).status,"UNVERIFIED")
    def test_missing_trial_provenance_unverified(self):
        c,t=pair()
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=SyntheticEvidence(False)).status,"UNVERIFIED")
    def test_wrong_source_sha_unverified(self):
        c,t=pair(trial=dict(source_sha="b"*40))
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=SyntheticEvidence()).status,"UNVERIFIED")
    def test_wrong_case_id_unverified(self):
        c,t=pair(trial=dict(case_id="foreign"))
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=SyntheticEvidence()).status,"UNVERIFIED")
    def test_modified_oracle_digest_unverified(self):
        c,t=pair(case=dict(allowed_outcomes=("OTHER",)))
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=SyntheticEvidence()).status,"UNVERIFIED")
    def test_oracle_forbidden_overlap_unverified(self):
        c,t=pair(case=dict(forbidden_outcomes=("SUGGEST_ONLY",)))
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=SyntheticEvidence()).status,"UNVERIFIED")
    def test_wrong_outcome_is_incorrect(self):
        c,t=pair(trial=dict(selected_outcome="ABSTAIN"))
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=SyntheticEvidence()).status,"INCORRECT")
    def test_forbidden_outcome_is_critical(self):
        c,t=pair(trial=dict(selected_outcome="UNAUTHORIZED_WRITE"))
        self.assertEqual(score_case(c,t,oracle=SyntheticOracle(),evidence=SyntheticEvidence()).status,"CRITICAL_FAILURE")
    def test_aggregate_empty_no_accuracy(self):
        a=aggregate(())
        self.assertIsNone(a.accuracy)
        self.assertEqual(a.status,"INCOMPLETE")
    def test_duplicate_trials_not_independent_cases(self):
        a=aggregate((CaseScore("same","CORRECT",SHA,"x"),CaseScore("same","CORRECT",SHA,"x")))
        self.assertEqual((a.status,a.independent_cases),("INCOMPLETE",0))
    def test_incomplete_evidence_never_release_quality(self):
        a=aggregate((CaseScore("a","CORRECT",SHA,"x"),))
        self.assertEqual(a.status,"INCOMPLETE")
        self.assertEqual(a.accuracy,1.0)
    def test_critical_failure_trumps_high_accuracy(self):
        rows=[CaseScore(f"case-{i}","CORRECT",SHA,"x") for i in range(269)]
        rows.append(CaseScore("case-269","CRITICAL_FAILURE",SHA,"x"))
        a=aggregate(tuple(rows))
        self.assertEqual(a.status,"CRITICAL_BLOCKED")
        self.assertEqual(a.critical,1)
    def test_270_synthetic_scores_never_certify_quality(self):
        rows=[CaseScore(f"c-{i}","CORRECT",SHA,"fixture") for i in range(270)]
        a=aggregate(tuple(rows))
        self.assertEqual(a.status,"SCORED_AWAITING_INDEPENDENT_ACCEPTANCE")
        self.assertEqual(a.claim_scope,"SAMPLE_ONLY_NO_GENERALIZATION")
    def test_270_unverified_rows_remain_incomplete(self):
        rows=[CaseScore(f"c-{i}","UNVERIFIED",SHA,"missing") for i in range(270)]
        self.assertEqual(aggregate(tuple(rows)).status,"INCOMPLETE")
    def test_invalid_case_scores_do_not_crash(self):
        self.assertEqual(aggregate((None,)).status,"INCOMPLETE")
    def test_oracle_backend_error_is_unverified(self):
        c,t=pair()
        class Failing:
            def verify_frozen_oracle(self,*args): raise RuntimeError("backend gone")
        self.assertEqual(score_case(c,t,oracle=Failing(),evidence=SyntheticEvidence()).status,"UNVERIFIED")

if __name__=="__main__": unittest.main()
