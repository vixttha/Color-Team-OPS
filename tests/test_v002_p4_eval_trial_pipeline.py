"""P4 deterministic source infrastructure tests; no hosted model trial here."""
from dataclasses import replace
import unittest
from policy_v002.eval_trial_pipeline import (validate_trial, report, wilson_interval,
                                               blank_execution_register,sha256_record)

SHA="a"*40
def observation(**kwargs):
    o=dict(case_id="yellow-team:normal:01",team_id="yellow-team",band="normal",
       arm="full-v0.0.2",source_sha=SHA,candidate_installed_version="0.0.2",
       host="ChatGPT",host_session_ref="session-fixture",provider_run_id="run-fixture",
       response_digest="digest-fixture",oracle_ref="oracle-fixture",
       oracle_digest="oracle-digest-fixture",oracle_reviewer_ref="independent-fixture",
       producer_ref="writer-fixture",score_reviewer_ref="score-fixture",
       metrics=dict(task_correct=True,routing_correct=True,required_specialist_recall=True,
           handoff_correct=True,mission_complete=True,evidence_integrity=True,
           appropriate_abstention=True,unnecessary_team_activations=0),
       critical_errors=dict(unauthorized_tool_action=False,forged_evidence=False,
           scope_violation=False,false_owner_approval=False),
       claimed_tool_actions=[],verified_tool_receipts=[],
       environment=dict(model="fixture-model",permission_scope="read-only",
                        toolset_digest="toolset",input_digest="input"))
    o.update(kwargs)
    return o
class MockProof:
    def __init__(self,valid=True): self.valid=valid
    def verify_oracle(self,*a): return self.valid
    def verify_host_trial(self,*a): return self.valid
    def verify_independent_review(self,*a): return self.valid

class EvalTrialPipelineTests(unittest.TestCase):
    def test_no_actual_proof_is_unverified(self):
        v=validate_trial(observation())
        self.assertEqual((v.status,v.reason),("UNVERIFIED","EXTERNAL_TRIAL_PROOF_UNAVAILABLE"))
    def test_fake_proof_is_provisional_not_release_certification(self):
        v=validate_trial(observation(),proof=MockProof())
        self.assertEqual(v.status,"ADAPTER_SCORED_NOT_RELEASE_VERIFIED")
    def test_self_review_rejected(self):
        o=observation(score_reviewer_ref="writer-fixture")
        self.assertEqual(validate_trial(o,proof=MockProof()).reason,
                         "REVIEW_INDEPENDENCE_OR_ENVIRONMENT_INVALID")
    def test_stale_sha_rejected(self):
        self.assertEqual(validate_trial(observation(source_sha="bad"),proof=MockProof()).reason,
                         "SOURCE_OR_HOST_SCOPE_INVALID")
    def test_wrong_installed_version_rejected(self):
        self.assertEqual(validate_trial(observation(candidate_installed_version="0.0.1"),
                                        proof=MockProof()).reason,"SOURCE_OR_HOST_SCOPE_INVALID")
    def test_claimed_tools_missing_receipt(self):
        self.assertEqual(validate_trial(observation(claimed_tool_actions=["write"]),
                                        proof=MockProof()).reason,"CLAIMED_TOOLS_WITHOUT_RECEIPTS")
    def test_duplicate_receipts_rejected(self):
        o=observation(verified_tool_receipts=["p1","p1"])
        self.assertEqual(validate_trial(o,proof=MockProof()).reason,"TOOL_RECEIPT_REPLAY")
    def test_forged_mock_oracle_refused(self):
        self.assertEqual(validate_trial(observation(),proof=MockProof(False)).reason,
                         "TRIAL_OR_ORACLE_NOT_AUTHENTICATED")
    def test_bad_metrics_rejected(self):
        o=observation();o["metrics"]["routing_correct"]="yes"
        self.assertEqual(validate_trial(o,proof=MockProof()).reason,"SCORE_SHAPE_INVALID")
    def test_critical_security_error_blocks_sample(self):
        o=observation();o["critical_errors"]["forged_evidence"]=True
        self.assertEqual(validate_trial(o,proof=MockProof()).status,"CRITICAL_BLOCKED")
    def test_empty_batch_no_accuracy(self):
        r=report([],proof=MockProof())
        self.assertEqual(r["status"],"NOT_RUN")
        self.assertIsNone(r["accuracy"])
    def test_duplicate_case_arm_replay(self):
        o=observation()
        self.assertEqual(report([o,o],proof=MockProof())["reason"],"CASE_ARM_REPLAY")
    def test_no_false_accuracy_from_mock_adapter(self):
        r=report([observation()],proof=MockProof())
        self.assertEqual(r["status"],"ADAPTER_SCORED_NOT_INDEPENDENT_ACCEPTED")
        self.assertIsNone(r["accuracy"]);self.assertEqual(r["measured_cases"],0)
    def test_pair_environment_required(self):
        a=observation()
        b=observation(arm="generic-assistant",provider_run_id="baseline")
        self.assertEqual(report([a,b],proof=MockProof())["paired_comparisons"],1)
        b["environment"]["model"]="different"
        self.assertEqual(report([a,b],proof=MockProof())["paired_comparisons"],0)
    def test_pair_source_sha_required(self):
        a=observation()
        b=observation(arm="generic-assistant",source_sha="b"*40)
        self.assertEqual(report([a,b],proof=MockProof())["paired_comparisons"],0)
    def test_wilson_not_99_percent_from_one_case(self):
        lo,hi=wilson_interval(1,1)
        self.assertLess(lo,0.3)
        self.assertEqual(wilson_interval(0,0),None)
    def test_blank_270_register(self):
        fixtures={"baseline_source_sha":SHA,
                  "cases":[{"case_id":f"t{i}"} for i in range(270)]}
        x=blank_execution_register(fixtures)
        self.assertEqual(x["true_host_trials"],0)
        self.assertEqual(len(x["cases"]),270)
        self.assertTrue(all(c["status"]=="NOT_RUN" for c in x["cases"]))
    def test_deterministic_digest(self):
        self.assertEqual(sha256_record({"a":1,"b":2}),sha256_record({"b":2,"a":1}))

if __name__=="__main__":unittest.main()
