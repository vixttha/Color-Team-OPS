"""Development harness negatives; synthetic events here are NOT model trials."""
import copy
import json
import unittest
from pathlib import Path

from devtools import cli_eval as e

ROOT = Path(__file__).resolve().parents[1]


class CorpusTests(unittest.TestCase):
    def test_complete_frozen_corpus(self):
        c = e.corpus(ROOT)
        self.assertEqual(len(c), 270)
        self.assertEqual(sum(x['holdout_reserved'] for x in c), 54)
        self.assertEqual(len(e.select_cases(c, 'pilot')), 9)
        self.assertTrue(all(x['case_id'].endswith(':normal:01') for x in e.select_cases(c, 'pilot')))

    def test_no_oracle_in_candidate_input(self):
        c = e.corpus(ROOT)[0]
        p = e.candidate_input(c)
        self.assertEqual(c['fixture']['artifact_text'], json.loads(p)['fixture']['artifact_text'])
        self.assertNotIn(c['task_specific_proposed_oracle']['expected_core_finding'], p)
        self.assertNotIn('task_specific_proposed_oracle', p)
        self.assertNotIn('reviewer-case-criteria', p)

    def test_real_ablations(self):
        arms = e.arm_material(ROOT, 'yellow-team')
        self.assertEqual(len(set(e.digest(x) for x in arms.values())), 4)
        self.assertIn('Built-in compact team capability directory', arms['full'])
        self.assertNotIn('Built-in compact team capability directory', arms['no_directory'])
        self.assertNotIn('"registry_version"', arms['no_directory'])
        self.assertIn('completion-event.schema.json', arms['full'])
        self.assertNotIn('completion-event.schema.json', arms['no_handoff'])
        self.assertNotIn('Color Team OPS', arms['generic'])

    def test_deterministic_paired_order(self):
        c = e.select_cases(e.corpus(ROOT), 'pilot')
        a = e.order(c, 20261104)
        self.assertEqual(a, e.order(c, 20261104))
        self.assertEqual(len(a), len(set(a)))
        self.assertEqual(len(a), 36)


class IngestTests(unittest.TestCase):
    def events(self):
        return [
            {'type':'thread.started', 'thread_id':'synthetic-test-thread'},
            {'type':'turn.started'},
            {'type':'item.completed','item':{'id':'i1','type':'agent_message','text':'Proposal only.'}},
            {'type':'turn.completed','usage':{'input_tokens':10,'cached_input_tokens':0,'output_tokens':5}},
        ]

    def parse(self, events=None, **kw):
        raw = ''.join(json.dumps(x)+'\n' for x in (events or self.events())).encode()
        return e.parse_trace(raw, 0, **kw)

    def test_complete_trace_not_independent_grade(self):
        r = self.parse()
        self.assertEqual(r['status'], 'COMPLETED')
        self.assertEqual(r['grading'], 'EXPLORATORY_CLI_TEST_UNVERIFIED_INDEPENDENCE')
        self.assertEqual(r['usage']['output_tokens'], 5)

    def test_corrupt_truncated_missing_identity_and_duplicate_events(self):
        for raw in [b'not json\n', b'{"type":"turn.completed"}\n', b'']:
            with self.assertRaises(e.Invalid): e.parse_trace(raw, 0)
        for events in [self.events()[:-1], self.events()[1:], self.events()+[self.events()[-1]]]:
            with self.assertRaises(e.Invalid): self.parse(events)

    def test_writer_or_external_tool_event_rejected(self):
        for kind in ['command_execution','mcp_tool_call','web_search','file_change']:
            events=self.events()
            events.insert(2, {'type':'item.completed','item':{'id':'bad','type':kind,'status':'completed'}})
            with self.assertRaises(e.Invalid): self.parse(events)

    def test_quota_and_timeout_never_success(self):
        self.assertEqual(e.failure_kind('usage limit reached', 1), 'QUOTA_BLOCKED')
        self.assertEqual(e.failure_kind('rate limit exceeded', 1), 'RATE_LIMIT_BLOCKED')
        self.assertEqual(e.failure_kind('', None), 'TIMEOUT')
        with self.assertRaises(e.Invalid): e.parse_trace(b'', 1)

    def test_duplicate_and_stale_environment(self):
        r={'case_id':'yellow-team:normal:01','arm':'full','source_sha':'a'*40,
           'environment_digest':'b'*64,'raw_sha256':'c'*64}
        e.bind_receipt(r, 'a'*40, 'b'*64, set())
        with self.assertRaises(e.Invalid): e.bind_receipt(r, 'd'*40, 'b'*64, set())
        with self.assertRaises(e.Invalid): e.bind_receipt(r, 'a'*40, 'd'*64, set())
        with self.assertRaises(e.Invalid): e.bind_receipt(r, 'a'*40, 'b'*64, {(r['case_id'],r['arm'])})


class ReviewTests(unittest.TestCase):
    def test_forged_role_and_approval_never_certify(self):
        for receipt in [{}, {'independent':True,'approved':True,'reviewer':'Purple'},
                        {'reviewer':'new-codex-session','decision':'APPROVED'}]:
            with self.assertRaises(e.Invalid): e.verify_review(receipt, {}, '2026-11-04T00:00:00+00:00')

    def test_nonblind_and_unobservable_metrics(self):
        c=next(x for x in e.corpus(ROOT) if x['holdout_reserved'])
        r=e.ungraded(c)
        self.assertEqual(r['holdout'], 'NONBLIND_REGRESSION_ONLY')
        self.assertEqual(r['task_correctness'], 'UNVERIFIED')
        self.assertEqual(r['unhinted_routing'], 'NOT_OBSERVABLE')
        self.assertEqual(r['host_skill_activation'], 'NOT_OBSERVABLE')
        self.assertEqual(e.wilson(0,0), None)
        self.assertAlmostEqual(e.wilson(1,1)[1],1)

    def test_command_has_no_privileged_inheritance(self):
        cmd=e.command('codex', Path('scratch'), Path('instructions.txt'))
        self.assertIn('read-only', cmd)
        self.assertIn('--ignore-user-config',cmd)
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox',cmd)
        self.assertIn('forced_login_method="chatgpt"',cmd)
        self.assertIn('features.shell_tool=false',cmd)
        self.assertIn('model_reasoning_effort="medium"',cmd)
        self.assertIn('gpt-6.1-sol',cmd)


if __name__=='__main__': unittest.main()
