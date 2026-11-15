"""Synthetic, no-Codex integration tests for Gate 2 one-shot orchestrator."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from devtools import cli_eval as e
from devtools import solo_eval_candidate_recovery_pipeline as p


class Gate2Pipeline(unittest.TestCase):
    def setUp(self):
        self.ctx = tempfile.TemporaryDirectory()
        self.addCleanup(self.ctx.cleanup)
        self.base = Path(self.ctx.name)
        self.original = self.base / 'candidates' / 'fake' / '1'
        self.original.mkdir(parents=True)
        for name in ('input.json','stdout.jsonl','stderr.txt','receipt.json'):
            (self.original/name).write_bytes(('immutable-' + name).encode())
        self.frozen = {'source_sha': p.recovery.EXPECTED_SOURCE_SHA,
                       'cases': {p.TARGET[0]: {'rubric_sha256': 'synthetic-rubric'}}}
        self.case = {'case_id': p.TARGET[0], 'team_id': 'blue-team'}
        self.target = {'first': self.original, 'case': self.case}
        self.rec = {'case_id': p.TARGET[0], 'arm': p.TARGET[1], 'grade': None}
        self.saved = [{'case_id': f'case-{n}', 'arm': 'full', 'grade': {'overall': 'PASS'}}
                      for n in range(209)]
        self.a0 = {'audit_only': True, 'source_sha': p.recovery.EXPECTED_SOURCE_SHA,
                   'freeze_sha256': p.recovery.EXPECTED_FREEZE_SHA,
                   'verified_completed_candidate_pairs': 209,
                   'verified_graded_pairs': 209,
                   'pilot_acceptance_present_and_bound': True,
                   'supervisor_lock_present': False,
                   'candidate_terminal_obstructions': [
                       {'case_id': p.TARGET[0], 'arm': p.TARGET[1], 'status': 'QUOTA_BLOCKED'}],
                   'grader_terminal_obstructions': []}
        self.a1 = dict(self.a0, verified_completed_candidate_pairs=210,
                       verified_graded_pairs=210,
                       candidate_terminal_obstructions=[])
        self.snapshot = p.original_hashes(self.original)

    def test_original_hashes_match_actual_bytes(self):
        self.assertEqual(len(self.snapshot), 4)
        p.check_original(self.original, self.snapshot)

    def test_original_mutation_rejected(self):
        (self.original/'receipt.json').write_text('forged')
        with self.assertRaisesRegex(e.Invalid, 'ORIGINAL_ATTEMPT_1_MUTATED'):
            p.check_original(self.original, self.snapshot)

    def test_missing_original_file_rejected(self):
        (self.original/'stderr.txt').unlink()
        with self.assertRaisesRegex(e.Invalid, 'ORIGINAL_ATTEMPT_1_MISSING'):
            p.original_hashes(self.original)

    def test_preflight_is_read_only_and_preserves_209(self):
        with patch.object(p.recovery, 'check', return_value=(self.frozen,self.base,self.saved,self.target)), \
             patch.object(p.audit, 'audit', return_value=self.a0) as auditor:
            f, base, target, original = p.preflight(Path('freeze.json'))
        self.assertEqual((f,base,target), (self.frozen,self.base,self.target))
        self.assertEqual(original,self.snapshot)
        auditor.assert_called_once()
        self.assertEqual(p.original_hashes(self.original),self.snapshot)

    def test_wrong_checkpoint_count_rejected(self):
        with patch.object(p.recovery, 'check', return_value=(self.frozen,self.base,self.saved[:-1],self.target)), \
             patch.object(p.audit,'audit',side_effect=AssertionError('must not audit')):
            with self.assertRaisesRegex(e.Invalid,'HISTORICAL_209_CHECKPOINT_CHANGED'):
                p.preflight(Path('freeze.json'))

    def test_wrong_audit_obstruction_rejected(self):
        bad = dict(self.a0, candidate_terminal_obstructions=[])
        with patch.object(p.recovery,'check',return_value=(self.frozen,self.base,self.saved,self.target)), \
             patch.object(p.audit,'audit',return_value=bad):
            with self.assertRaisesRegex(e.Invalid,'LIVE_ORIGINAL_CHECKPOINT_AUDIT_MISMATCH'):
                p.preflight(Path('freeze.json'))

    def test_no_model_without_explicit_ack(self):
        with patch.object(p,'preflight',side_effect=AssertionError('no reads beyond ack')):
            with self.assertRaisesRegex(e.Invalid,'SEPARATE_OWNER_ONE_CALL_ACK_REQUIRED'):
                p.execute_once(Path('freeze.json'),None)

    def run_synthetic(self, retry=None, grade=None, post=None, before=None):
        if retry is None:
            retry={'disposition':'COMPLETED','candidate_model_calls':1,'new_append_only_attempt':2}
        if grade is None:
            grade=({'status':'GRADED'},
                   {'critical_violations':[],'contradictions':[],'uncertainty':'LOW'})
        if before is None:
            before=[*self.saved, self.rec]
        candidate_receipt={'attempt':2,'status':'COMPLETED','raw_sha256': 'synthetic-candidate-hash'}
        with patch.object(p,'preflight',return_value=(self.frozen,self.base,self.target,self.snapshot)), \
             patch.object(p.recovery,'execute_one',return_value=retry) as candidate, \
             patch.object(p.recovery,'recovered_for_resume',return_value=(candidate_receipt,'real-only-in-production')) as recovered, \
             patch.object(p.s,'rows',return_value=before), \
             patch.object(p.e,'load',return_value={'cases':{p.TARGET[0]:{'required_observable_findings':['synthetic']}}}), \
             patch.object(p.e,'executable',return_value='mock-codex'), \
             patch.object(p.g,'grade',return_value=grade) as grader, \
             patch.object(p.audit,'audit',return_value=self.a1 if post is None else post):
            try:
                output=p.execute_once(Path('freeze.json'), p.recovery.ONE_CALL_ACK)
            finally:
                self.assertFalse((self.base/'supervisor.lock').exists())
        return output,candidate,grader,recovered

    def test_frozen_one_candidate_and_one_grade_then_full_receipt_reaudit(self):
        result,candidate,grader,recovered = self.run_synthetic()
        candidate.assert_called_once()
        recovered.assert_called_once()
        grader.assert_called_once()
        self.assertEqual(result['disposition'],'RECOVERED_AND_RECEIPTS_VERIFIED')
        self.assertEqual(result['candidate_completed'],210)
        self.assertEqual(result['provisional_grades'],210)
        self.assertFalse(result['quality_independent'])
        self.assertTrue(result['original_attempt_1_retained'])
        self.assertEqual(p.original_hashes(self.original),self.snapshot)

    def test_failed_retry_never_grades(self):
        bad={'disposition':'QUOTA_BLOCKED','candidate_model_calls':1,'new_append_only_attempt':2}
        with self.assertRaisesRegex(e.Invalid,'CANDIDATE_RETRY_FAILED_NO_GRADER_CALL'):
            self.run_synthetic(retry=bad)

    def test_grader_quota_rejected_and_original_retained(self):
        with self.assertRaisesRegex(e.Invalid,'GRADER_BLOCKED_CHECKPOINT_RETAINED'):
            self.run_synthetic(grade=({'status':'QUOTA_BLOCKED'},None))
        self.assertEqual(p.original_hashes(self.original),self.snapshot)

    def test_post_audit_wrong_grade_count_rejected(self):
        broken=dict(self.a1,verified_graded_pairs=209)
        with self.assertRaisesRegex(e.Invalid,'POST_RECOVERY_RECEIPT_AUDIT_MISMATCH'):
            self.run_synthetic(post=broken)

    def test_duplicate_recovered_pair_rejected(self):
        dup = [*self.saved,self.rec,self.rec]
        with self.assertRaisesRegex(e.Invalid,'NEW_CANDIDATE_NOT_UNIQUELY_BOUND'):
            self.run_synthetic(before=dup)

    def test_model_provisional_critical_grade_requires_review(self):
        grade=({'status':'GRADED'},
               {'critical_violations':[{'reason':'synthetic','quotes':['x']}],
                'contradictions':[], 'uncertainty':'HIGH'})
        result,_,_,_=self.run_synthetic(grade=grade)
        self.assertEqual(result['disposition'],'REQUIRES_SEMANTIC_REVIEW')


if __name__ == '__main__':
    unittest.main()
