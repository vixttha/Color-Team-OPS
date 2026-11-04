import unittest
from devtools import cli_eval as e
from devtools import solo_eval as s


class SoloExecutionTests(unittest.TestCase):
    def test_history_cannot_enter_new_namespace(self):
        historical=e.load(e.ROOT/e.EVAL/'CLI-EVAL-FREEZE-2026-11-04.json')
        with self.assertRaises(e.Invalid):s.location(historical)

    def test_statistics_use_actual_graded_denominators(self):
        rows=[{'case_id':'yellow-team:normal:01','arm':'generic','grade':{'metrics':{'task_correctness':{'status':'PASS'}}}},
              {'case_id':'yellow-team:normal:01','arm':'full','grade':{'metrics':{'task_correctness':{'status':'FAIL'}}}},
              {'case_id':'yellow-team:normal:02','arm':'full','grade':None}]
        a=s.statistics(rows,'full')
        self.assertEqual(a['graded_denominator'],1)
        self.assertEqual(a['strict_correctness'],0)
        self.assertEqual(a['paired_n'],1)
        self.assertEqual(a['paired_delta'],-1)
        self.assertEqual(s.statistics([], 'full')['strict_correctness'],None)

    def test_completion_does_not_imply_pilot_quality_acceptance(self):
        summary={'candidate_completed':36,'graded':36,'critical_pairs':1,'contradiction_pairs':0,'high_uncertainty':0}
        with self.assertRaises(e.Invalid):s.quality_gate(summary)
        for key in ('candidate_completed','graded'):
            bad=dict(summary,critical_pairs=0,**{key:35})
            with self.assertRaises(e.Invalid):s.quality_gate(bad)
        self.assertTrue(s.quality_gate(dict(summary,critical_pairs=0)))


if __name__=='__main__':unittest.main()
