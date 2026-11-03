"""Cross-language PrismCell project/message contract parity. Native optional dev test."""
import copy
import json
import subprocess
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent
SCHEMA=ROOT/'core'/'schemas'
def check(kind, record):
    schema=json.loads((SCHEMA/(kind+'.schema.json')).read_text(encoding='utf8'))
    return Draft202012Validator(schema).is_valid(record)
def js(config, messages):
    code="""import {validateConfig,validateMessage} from './PRISMCELL/core/engine.mjs';
let raw='';for await(const c of process.stdin)raw+=c;
const d=JSON.parse(raw);
console.log(JSON.stringify({project:validateConfig(d.config),messages:d.messages.map(x=>validateMessage(d.messageConfig??d.config,x))}));
"""
    p=subprocess.run(['node','--input-type=module','-e',code],cwd=REPO,input=json.dumps({'config':config,'messages':messages}),capture_output=True,text=True,timeout=30,check=True)
    return json.loads(p.stdout)
class ContractParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=json.loads((ROOT/'tests'/'fixtures'/'nebula-project.json').read_text(encoding='utf8'))
        cls.sha='a'*40
        cls.message={'message_id':'IN-STORY-20261102-123','from_team':'ASTRONOMY','from_branch':cls.cfg['teams']['ASTRONOMY']['branch'],
                     'to_team':'STORY','type':'FINDING','priority':'P1','summary':'Find a source mismatch','source_ref':'src/review',
                     'source_sha':cls.sha,'evidence_links':['https://example.com/evidence'],'requested_action':'Review the finding',
                     'authority_scope':'Read only','status':'POSTED'}
    def test_01_project_schema_and_runtime_parity(self):
        base=self.cfg
        records=[
            base, {**base,'teams':{'STORY':base['teams']['STORY']}},
            {**base,'project_id':' '},
            {**base,'schema_version':'bad'},
            {**base,'transport':'example-runtime'},
            {**base,'project_id':'Z'*101},
            {**base,'unexpected':'untrusted'},
            {**base,'teams':{}},
            {**base,'repository_url':'https://service.invalid/owner/repo'},
            {**base,'teams':{**base['teams'],'REVIEW':{**base['teams']['REVIEW'],'branch':'invalid..name'}}},
            {**base,'repository':'bad repository'}
        ]
        for n,c in enumerate(records):
            with self.subTest(fixture=n):
                j=js(c,[])
                self.assertEqual(check('project',c),not bool(j['project']),msg=f"project case {n}: {j['project']}")
    def test_02_message_schema_and_runtime_parity(self):
        m=self.message
        records=[
            m,{**m,'message_id':'CUSTOM-ABC1234'}, {**m,'message_id':'IN-STORY-20261102-12'},
            {**m,'to_team':'constructor'},{**m,'to_team':'toString'},
            {**m,'status':'ACCEPTED'},{k:v for k,v in m.items() if k!='status'},
            {**m,'posted_at':'2026-11-02T12:00:00Z'},
            {**m,'summary':'   '},{**m,'summary':'A'*2049},
            {**m,'source_ref':'b'*181},{**m,'from_branch':'b'*121},
            {**m,'priority':'P9'},{**m,'source_sha':'xyz'},
            {**m,'evidence_links':['http://no.example/test']},
            {**m,'evidence_links':['https://example.com/a','https://example.com/a']},
            {**m,'evidence_links':['https://bad@example.com/credential']},
            {**m,'evidence_links':[]},
            {**m,'issue_url':self.cfg['teams']['STORY']['issue_url']},
            {**m,'requested_action':' '},
            {**m,'authority_scope':' '}
        ]
        result=js(self.cfg,records)
        self.assertEqual(result['project'],[])
        for n,item in enumerate(records):
            with self.subTest(fixture=n):
                self.assertEqual(check('message',item),not bool(result['messages'][n]),msg=f"message case {n}: {result['messages'][n]}")
    def test_03_cross_field_gates_exceed_plain_json_schema(self):
        # Schema cannot compare repository_url to repository, branch to team's bound identity,
        # or issue_url to actual issue number without cross-document provider attestation.
        mismatched={**self.cfg,'repository':'another/different'}
        self.assertTrue(check('project',mismatched))
        self.assertIn('BAD_PROJECT',js(mismatched,[])['project'])
        wrong={**self.message,'from_branch':'agent/other'}
        self.assertTrue(check('message',wrong))
        self.assertIn('CLAIMED_SENDER_BRANCH_MISMATCH',js(self.cfg,[wrong])['messages'][0])
        incorrect={**self.message,'issue_url':self.cfg['teams']['REVIEW']['issue_url']}
        self.assertTrue(check('message',incorrect))
        self.assertIn('WRONG_TARGET_URL',js(self.cfg,[incorrect])['messages'][0])
    def test_04_repeated_issue_ids_disallowed_by_runtime(self):
        wrong=copy.deepcopy(self.cfg)
        wrong['teams']['REVIEW']['issue_number']=wrong['teams']['STORY']['issue_number']
        wrong['teams']['REVIEW']['issue_url']=wrong['teams']['STORY']['issue_url']
        self.assertTrue(check('project',wrong))
        self.assertIn('DUPLICATE_LOCATOR',js(wrong,[])['project'])
if __name__=='__main__':unittest.main()
