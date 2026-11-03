"""Optional native Python Draft 2020-12 regression tests; jsonschema is a dev dependency only."""
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT = Path(__file__).resolve().parents[1] / 'core' / 'schemas'
SCHEMAS = {name: json.loads((ROOT / (name + '.schema.json')).read_text()) for name in ('message','state','work-item','project')}
SHA = 'a'*40
MESSAGE = {'message_id':'IN-BETA-20261102-123','from_team':'ALPHA','from_branch':'agent/alpha','to_team':'BETA','type':'FINDING','priority':'P1','summary':'Benign test','source_ref':'example/ref','source_sha':SHA,'evidence_links':['https://github.com/example/repo/issues/3'],'requested_action':'Review only','authority_scope':'No grant','status':'POSTED'}
STATE = {'schema_version':'prismcell-state-0.0.1','template':'PrismCell Workbench','version':'0.0.1','team':'ALPHA','home_branch':'agent/alpha','status':'BOOTSTRAPPED','active_work_item':None,'last_verified_product_sha':None,'last_session':None,'release_authorized':False}
WORK = {'id':'ITEM-01','title':'Review','priority':'P1','status':'QUEUED','acceptance_criteria':['Verify evidence'],'evidence_status':'NOT_RUN'}
REPO_URL = 'https://github.com/example/repo'
PROJECT = {'schema_version':'prismcell-project-config-0.0.1','project_id':'DEMO','repository':'example/repo','repository_url':REPO_URL,'transport':'github-issues-manual','teams':{'ALPHA':{'branch':'agent/alpha','issue_number':1,'issue_url':REPO_URL+'/issues/1'},'BETA':{'branch':'agent/beta','issue_number':2,'issue_url':REPO_URL+'/issues/2'}}}
def valid(name,record):return Draft202012Validator(SCHEMAS[name]).is_valid(record)
class UniversalSchemas(unittest.TestCase):
  def test_01_all_four_valid_draft202012(self):
    for name,schema in SCHEMAS.items():
      with self.subTest(name=name): Draft202012Validator.check_schema(schema)
  def test_02_regular_message(self):self.assertTrue(valid('message',MESSAGE))
  def test_03_sender_accepted_rejected(self):self.assertFalse(valid('message',{**MESSAGE,'status':'ACCEPTED'}))
  def test_04_unknown_extra_rejected(self):self.assertFalse(valid('message',{**MESSAGE,'owner_approved':True}))
  def test_05_malformed_sha_rejected(self):self.assertFalse(valid('message',{**MESSAGE,'source_sha':'abc'}))
  def test_06_non_https_link_rejected(self):self.assertFalse(valid('message',{**MESSAGE,'evidence_links':['javascript:bad']}))
  def test_07_generic_team_names_permitted(self):self.assertTrue(valid('state',STATE))
  def test_08_release_flag_true_rejected(self):self.assertFalse(valid('state',{**STATE,'release_authorized':True}))
  def test_09_state_invalid_sha_rejected(self):self.assertFalse(valid('state',{**STATE,'last_verified_product_sha':'invalid'}))
  def test_10_work_queued_unrun_valid(self):self.assertTrue(valid('work-item',WORK))
  def test_11_work_accepted_unrun_invalid(self):self.assertFalse(valid('work-item',{**WORK,'status':'ACCEPTED'}))
  def test_12_valid_accepted_work_with_evidence(self):
    accepted={**WORK,'status':'ACCEPTED','evidence_status':'EXECUTED_AT_SHA','source_sha':SHA,'assigned_team':'ALPHA','assigned_role':'Developer','scope':'Source review','risk':'LOW','prerequisites':[],'budget':{'max_repairs':2},'repair_count':0,'evidence_refs':['https://github.com/example/repo/commit/123'],'validation':{'result':'PASS','evidence_ref':'https://github.com/example/repo/issues/1'},'internal_audit':{'result':'PASS','evidence_ref':'https://github.com/example/repo/issues/1'},'head_decision':{'result':'ACCEPT','decision_ref':'https://github.com/example/repo/issues/1'}}
    self.assertTrue(valid('work-item',accepted))
  def test_13_project_config_valid(self):self.assertTrue(valid('project',PROJECT))
  def test_14_project_one_team_supported(self):self.assertTrue(valid('project',{**PROJECT,'teams':{'ALPHA':PROJECT['teams']['ALPHA']}}))
  def test_16_project_without_teams_rejected(self):self.assertFalse(valid('project',{**PROJECT,'teams':{}}))
  def test_17_project_whitespace_id_rejected(self):self.assertFalse(valid('project',{**PROJECT,'project_id':' '}))
  def test_15_project_wrong_issue_scheme_rejected(self):
    bad=json.loads(json.dumps(PROJECT));bad['teams']['ALPHA']['issue_url']='http://example.com'
    self.assertFalse(valid('project',bad))
if __name__=='__main__':unittest.main()
