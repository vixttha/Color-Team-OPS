"""Development harness negatives; synthetic events here are NOT model trials."""
import copy
import json
import unittest
import tempfile
import zipfile
import subprocess
from unittest.mock import patch
from pathlib import Path

from devtools import cli_eval as e
from devtools import cli_eval_evidence as transfer

ROOT = Path(__file__).resolve().parents[1]


class CorpusTests(unittest.TestCase):
    def test_historical_checkout_bytes_require_exact_hash_reconstruction(self):
        blob=b'line one\nline two\n'
        self.assertEqual(e.frozen_checkout_bytes(blob,e.digest(blob)),blob)
        crlf=blob.replace(b'\n',b'\r\n')
        self.assertEqual(e.frozen_checkout_bytes(blob,e.digest(crlf)),crlf)
        with self.assertRaises(e.Invalid): e.frozen_checkout_bytes(blob,e.digest(blob+b'changed'))

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
    def test_timeout_kills_child_and_returns_incomplete_receipt_material(self):
        with patch.object(e.subprocess,'run'), patch.object(e.subprocess,'Popen') as launch:
            proc=launch.return_value
            proc.communicate.side_effect=[subprocess.TimeoutExpired('synthetic-test',0.01),(b'',b'timed out')]
            raw,err,code,*_=e.invoke('synthetic-test-executable','fixture','instructions',0.01)
            proc.kill.assert_called_once()
            self.assertIsNone(code)
            self.assertEqual(e.failure_kind(err.decode(),code),'TIMEOUT')

    def test_reused_session_and_relabelled_trace_rejected(self):
        parsed=self.parse()
        cid='yellow-team:normal:01'
        f={'source_sha':'a'*40,'environment_digest':'b'*64,
           'cases':{cid:{'input_sha256':'c'*64}},
           'arm_material_sha256':{'yellow-team':{'full':'d'*64,'generic':'e'*64}}}
        r={'case_id':cid,'arm':'full','source_sha':'a'*40,'environment_digest':'b'*64,
           'freeze_sha256':e.digest(f),'input_sha256':'c'*64,'arm_sha256':'d'*64,
           'session_sha256':parsed['session_sha256'],'usage':parsed['usage'],'raw_sha256':'f'*64}
        for field in ('freeze_sha256','input_sha256','arm_sha256','session_sha256'):
            bad=dict(r,**{field:'0'*64})
            with self.assertRaises(e.Invalid): e.bind_trace(bad,parsed,f,set(),set())
        pairs,sessions=set(),set()
        e.bind_trace(r,parsed,f,pairs,sessions)
        duplicate=dict(r,arm='generic',arm_sha256='e'*64)
        with self.assertRaises(e.Invalid): e.bind_trace(duplicate,parsed,f,pairs,sessions)

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

    def test_quota_detection_uses_provider_errors_not_candidate_answer(self):
        answer=json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'Recommend quota monitoring.'}}).encode()+b'\n'
        self.assertEqual(e.provider_diagnostics(answer,b'',0),'')
        error=json.dumps({'type':'error','message':'usage limit reached'}).encode()+b'\n'
        self.assertEqual(e.failure_kind(e.provider_diagnostics(error,b'',0),0),'QUOTA_BLOCKED')

    def test_duplicate_and_stale_environment(self):
        r={'case_id':'yellow-team:normal:01','arm':'full','source_sha':'a'*40,
           'environment_digest':'b'*64,'raw_sha256':'c'*64}
        e.bind_receipt(r, 'a'*40, 'b'*64, set())
        with self.assertRaises(e.Invalid): e.bind_receipt(r, 'd'*40, 'b'*64, set())
        with self.assertRaises(e.Invalid): e.bind_receipt(r, 'a'*40, 'd'*64, set())
        with self.assertRaises(e.Invalid): e.bind_receipt(r, 'a'*40, 'b'*64, {(r['case_id'],r['arm'])})


class ReviewTests(unittest.TestCase):
    def test_statistics_exclude_ungraded_and_pair_same_cases(self):
        rows=[{'case_id':'t:normal:01','arm':'generic','independent_correct':True},
              {'case_id':'t:normal:01','arm':'full','independent_correct':False},
              {'case_id':'t:normal:02','arm':'full','independent_correct':True},
              {'case_id':'t:normal:03','arm':'full','independent_correct':None}]
        result=e.graded_statistics(rows,'full')
        self.assertEqual(result['denominator'],2)
        self.assertEqual(result['correct'],1)
        self.assertEqual(result['accuracy'],0.5)
        self.assertEqual(result['paired_baseline_n'],1)
        self.assertEqual(result['paired_baseline_delta'],-1)
        self.assertEqual(e.graded_statistics([], 'full')['accuracy'],None)

    def test_forged_authorization_stale_grade_and_bare_boolean_rejected(self):
        receipt={'case_id':'yellow-team:normal:01','source_sha':'a'*40,'raw_sha256':'b'*64}
        rubric={'required_observable_findings':['Reject unauthorized disclosure']}
        for grade in [
            {'approved':True,'owner_approved':True,'independent':True},
            {'case_id':receipt['case_id'],'source_sha':'c'*40,'raw_sha256':'b'*64,'oracle_receipt_sha256':'d'*64},
            {'case_id':receipt['case_id'],'source_sha':'a'*40,'raw_sha256':'b'*64,'oracle_receipt_sha256':'d'*64,
             'reviewer_principal':'Purported Purple','pass':True},
        ]:
            with self.assertRaises(e.Invalid):
                e.validate_grade(grade,receipt,rubric,'d'*64,{'reviewers':{}})

    def test_missing_reviewer_capability_is_zero(self):
        self.assertEqual(e.certification({'oracle_review_receipts':[]}),{})

    def test_environment_never_inherits_api_or_github_secrets(self):
        with patch.dict(e.os.environ,{'OPENAI_API_KEY':'synthetic','GH_TOKEN':'synthetic',
                                     'GITHUB_TOKEN':'synthetic','CODEX_THREAD_ID':'synthetic'},clear=False):
            env=e.minimal_env()
        self.assertFalse(set(env) & {'OPENAI_API_KEY','GH_TOKEN','GITHUB_TOKEN','CODEX_THREAD_ID'})

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


class EvidenceTransferTests(unittest.TestCase):
    def test_roundtrip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/'raw';src.mkdir()
            (src/'receipt.json').write_text('{"synthetic":true}',encoding='utf-8')
            archive=root/'private.zip'
            receipt=transfer.export(src,archive)
            dest=root/'imported'
            transfer.import_archive(archive,dest,receipt['archive_sha256'])
            self.assertEqual((dest/'receipt.json').read_bytes(),(src/'receipt.json').read_bytes())
            with self.assertRaises(e.Invalid): transfer.import_archive(archive,dest,receipt['archive_sha256'])
            with self.assertRaises(e.Invalid): transfer.export(src,archive)
            with self.assertRaises(e.Invalid): transfer.import_archive(archive,root/'other','0'*64)

    def test_path_traversal_devices_duplicates_and_tampered_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for n,name in enumerate(['../escape','/absolute','C:/escape','a\\escape','NUL.txt','x/COM1','trailing.']):
                archive=root/(str(n)+'.zip')
                with zipfile.ZipFile(archive,'w') as z:
                    z.writestr('INDEX.json',json.dumps({name:{'sha256':e.digest(b'x'),'bytes':1}}))
                    z.writestr(name,b'x')
                with self.assertRaises(e.Invalid,msg=name):
                    transfer.import_archive(archive,root/('out'+str(n)),e.digest(archive.read_bytes()))
            archive=root/'tampered.zip'
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('INDEX.json',json.dumps({'receipt.json':{'sha256':'0'*64,'bytes':1}}))
                z.writestr('receipt.json',b'x')
            with self.assertRaises(e.Invalid): transfer.import_archive(archive,root/'tampered-out',e.digest(archive.read_bytes()))


if __name__=='__main__': unittest.main()
