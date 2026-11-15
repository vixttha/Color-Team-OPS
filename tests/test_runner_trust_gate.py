"""Pure unit tests; no owner runner/host actions."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'devtools/runner_trust_gate/admission.py'
spec = importlib.util.spec_from_file_location('runner_gate_admission', MODULE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
NOW = dt.datetime(2026, 11, 14, 19, 0, tzinfo=dt.timezone.utc)

def environment():
    return {
        'GITHUB_REPOSITORY':'vixttha/Color-Team-OPS',
        'GITHUB_SHA':'a'*40,
        'GITHUB_WORKFLOW_REF':'vixttha/Color-Team-OPS/.github/workflows/v0.0.2-integration-native.yml@refs/heads/integration/v0.0.2-master-single-thread',
        'GITHUB_WORKFLOW_SHA':'b'*40,
        'GITHUB_JOB':'windows',
        'RUNNER_NAME':'color-team-ops-windows-01',
        'RUNNER_OS':'Windows',
        'RUNNER_ENVIRONMENT':'self-hosted',
        'GITHUB_RUN_ID':'42100000000',
        'GITHUB_RUN_ATTEMPT':'1',
    }

def approval(context=None):
    result = {'schema':1,'issued_at':'2026-11-14T18:59:00Z','expires_at':'2026-11-14T19:04:00Z'}
    result.update(context if context is not None else gate.context_from_env(environment()))
    return result

class GatePolicyTests(unittest.TestCase):
    def test_good_exact_approval(self):
        gate.permit_valid(approval(),gate.context_from_env(environment()),NOW)

    def test_all_fields_fail_closed(self):
        for field in gate._FIELDS:
            p = approval();p[field] = p[field]+'x'
            with self.subTest(field=field), self.assertRaises(gate.Denied):
                gate.permit_valid(p,gate.context_from_env(environment()),NOW)

    def test_missing_all_identity_fields_fail(self):
        for key in gate._FIELDS.values():
            e=environment();del e[key]
            with self.subTest(key=key), self.assertRaises(gate.Denied):
                gate.context_from_env(e)

    def test_denies_hosted_runner(self):
        e=environment();e['RUNNER_ENVIRONMENT']='github-hosted'
        with self.assertRaises(gate.Denied):gate.context_from_env(e)

    def test_denies_repository_change(self):
        e=environment();e['GITHUB_REPOSITORY']='other/private'
        with self.assertRaises(gate.Denied):gate.context_from_env(e)

    def test_denies_malformed_shas(self):
        for key in ('GITHUB_SHA','GITHUB_WORKFLOW_SHA'):
            e=environment();e[key]='anything'
            with self.subTest(key=key), self.assertRaises(gate.Denied):gate.context_from_env(e)

    def test_denies_invalid_job_and_runner(self):
        for key in ('GITHUB_JOB','RUNNER_NAME'):
            e=environment();e[key]='../../owner'
            with self.subTest(key=key), self.assertRaises(gate.Denied):gate.context_from_env(e)

    def test_denies_wrong_workflow_ref(self):
        e=environment();e['GITHUB_WORKFLOW_REF']='evil/file'
        with self.assertRaises(gate.Denied):gate.context_from_env(e)

    def test_denies_stale_and_future(self):
        for stamp in ('2026-11-14T19:05:00Z','2026-11-14T18:50:00Z'):
            p=approval()
            if stamp.endswith('05:00Z'):p['issued_at']=stamp;p['expires_at']='2026-11-14T19:09:00Z'
            else:p['issued_at']='2026-11-14T18:40:00Z';p['expires_at']=stamp
            with self.subTest(stamp=stamp), self.assertRaises(gate.Denied):gate.permit_valid(p,gate.context_from_env(environment()),NOW)

    def test_denies_excessive_window(self):
        p=approval();p['expires_at']='2026-11-14T19:20:00Z'
        with self.assertRaises(gate.Denied):gate.permit_valid(p,gate.context_from_env(environment()),NOW)

    def test_denies_extra_or_missing_properties(self):
        for change in ('extra','missing'):
            p=approval()
            if change=='extra':p['override']=True
            else:del p['workflow_sha']
            with self.subTest(change=change),self.assertRaises(gate.Denied):gate.permit_valid(p,gate.context_from_env(environment()),NOW)

    def test_denies_duplicate_keys(self):
        with self.assertRaises(gate.Denied):json.loads('{"schema":1,"schema":2}',object_pairs_hook=gate._unique_pairs)

    def test_denies_invalid_timestamp(self):
        p=approval();p['expires_at']='2026-11-14T19:04:00+01:00'
        with self.assertRaises(gate.Denied):gate.permit_valid(p,gate.context_from_env(environment()),NOW)

    def test_denies_boolean_schema(self):
        p=approval();p['schema']=True
        with self.assertRaises(gate.Denied):gate.permit_valid(p,gate.context_from_env(environment()),NOW)

    def test_approval_name_bounded(self):
        c=gate.context_from_env(environment())
        self.assertEqual(gate._approval_filename(c),'42100000000-1-windows-color-team-ops-windows-01.json')

if __name__=='__main__': unittest.main()