"""Additive SOLO v2 candidate runner with truthful CLI-version receipts.

Derived from frozen solo_eval.candidate, which remains byte-for-byte unchanged.
The existing full-evaluation supervisor uses this ONLY for new candidates.
CLI-version drift is recorded in the receipt and must be separated at quality
analysis. No model/rubric/arm/context/permissions change is authorized.
"""
from __future__ import annotations

from devtools import cli_eval as e
from devtools import solo_eval as s
from devtools.solo_eval_candidate_recovery import observed_cli_version


def candidate(f,case,arm,exe):
    base=s.location(f)/'candidates'/e.digest(case['case_id']+'|'+arm)[:24]
    prompt=e.candidate_input(case);material=e.arm_material(e.ROOT,case['team_id'])[arm]
    e.require(e.digest(prompt)==f['cases'][case['case_id']]['input_sha256'],'CANDIDATE_INPUT_CHANGED')
    e.require(e.digest(material)==f['arm_material_sha256'][case['team_id']][arm],'CANDIDATE_ARM_CHANGED')
    for attempt in range(1,f['environment']['max_attempts_per_pair']+1):
        trial=base/str(attempt)
        if (trial/'receipt.json').is_file():
            r=e.load(trial/'receipt.json')
            if r['status']=='COMPLETED':
                parsed=s.verify_candidate(f,trial,set(),set())
                return r,parsed['response']
            if r['status']!='EXECUTION_BLOCKED':return r,None
            continue
        # Observe before creating attempt evidence: failed version probes write nothing.
        version = observed_cli_version(exe)
        trial.mkdir(parents=True, exist_ok=False)
        (trial/'input.json').write_text(prompt,encoding='utf-8')
        out,err,code,start,end,latency,isolated=e.invoke(exe,prompt,material,f['environment']['timeout_seconds'])
        (trial/'stdout.jsonl').write_bytes(out);(trial/'stderr.txt').write_bytes(err)
        r={'host':'CLI_TEST','evaluation_mode':'SOLO_DEVELOPER','case_id':case['case_id'],'arm':arm,'attempt':attempt,
           'source_sha':f['source_sha'],'functional_source_sha':e.MODEL_SOURCE,'environment_digest':f['environment_digest'],
           'freeze_sha256':e.digest(f),'input_sha256':e.digest(prompt),'arm_sha256':e.digest(material),
           'raw_sha256':e.digest(out),'stderr_sha256':e.digest(err),'started_at':start,'ended_at':end,
           'latency_seconds':latency,'exit_code':code,'cli_version':version,'model_requested':e.MODEL,
           'effort_requested':e.EFFORT,'model_observed':'NOT_EXPOSED_BY_JSONL','model_identity_provenance':'CLI_REQUEST_NOT_PROVIDER_ATTESTED',
           'status':e.failure_kind(e.provider_diagnostics(out,err,code),code),'metrics':e.ungraded(case)}
        response=None
        if not isolated:r['status']='INVALID_TRACE';r['reason']='CANDIDATE_SCRATCH_MUTATION'
        elif code==0 and r['status'] not in ('QUOTA_BLOCKED','RATE_LIMIT_BLOCKED'):
            try:
                parsed=e.parse_trace(out,code);response=parsed.pop('response');r.update(parsed)
                r['grading']='SOLO_DEVELOPER_UNGRADED'
                (trial/'response.txt').write_text(response,encoding='utf-8')
            except e.Invalid as exc:r['status']='INVALID_TRACE';r['reason']=str(exc)
        e.validate_observation(r);e.save_new(trial/'receipt.json',r)
        if r['status']=='COMPLETED':return r,response
        if r['status']!='EXECUTION_BLOCKED':return r,None
    return r,None

