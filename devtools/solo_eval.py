"""One supervisor, bounded isolated model subjects, provisional semantic grading."""
from __future__ import annotations
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import json
from pathlib import Path
import subprocess
import threading
from devtools import cli_eval as e
from devtools import solo_grader as g


def location(f):
    e.require(f.get('evaluation_mode')=='SOLO_DEVELOPER' and f.get('solo_revision')=='solo-eval-v1', 'NEW_SOLO_FREEZE_REQUIRED')
    return e.PRIVATE/'solo-v1'/e.digest(f)


def frozen_config():
    path=e.ROOT/e.EVAL/'SOLO-GRADER-CALIBRATION-v3.json'
    calibration=e.load(path)
    e.require(calibration['passed'] and calibration['grader_configuration_sha256']==e.digest(g.configuration()),'GRADER_CALIBRATION_REQUIRED')
    return {'solo_revision':'solo-eval-v1','grader':g.configuration(),
            'calibration_report_sha256':e.digest(path.read_bytes()),
            'max_parallel_subjects':4,'candidate_target':1080,'pilot_target':36,
            'quality_policy':{'no_unresolved_critical':True,'no_unresolved_contradictions':True,
                              'high_uncertainty_requires_self_review':True,
                              'correctness':'strict PASS / assessable grades; PARTIAL reported separately'},
            'historical_exploratory_pairs_reused':0}


def statistics(rows,arm):
    def state(r):return r['grade']['metrics']['task_correctness']['status'] if r.get('grade') else None
    actual={r['case_id']:state(r) for r in rows if r['arm']==arm and state(r) not in (None,'NOT_OBSERVABLE')}
    baseline={r['case_id']:state(r) for r in rows if r['arm']=='generic' and state(r) not in (None,'NOT_OBSERVABLE')}
    counts=Counter(actual.values());n=len(actual);paired=sorted(set(actual)&set(baseline))
    return {'graded_denominator':n,'states':dict(counts),'strict_correctness':counts['PASS']/n if n else None,
            'wilson95':e.wilson(counts['PASS'],n),'paired_n':len(paired),
            'paired_delta':sum(int(actual[c]=='PASS')-int(baseline[c]=='PASS') for c in paired)/len(paired) if paired else None}


def quality_gate(summary):
    e.require(summary['candidate_completed']==36 and summary['graded']==36,'PILOT_EXECUTION_OR_GRADING_INCOMPLETE')
    e.require(summary['critical_pairs']==0,'PILOT_CRITICAL_SECURITY_FINDING')
    e.require(summary['contradiction_pairs']==0,'PILOT_UNRESOLVED_CONTRADICTIONS')
    e.require(summary['high_uncertainty']==0,'PILOT_HIGH_UNCERTAINTY_REQUIRES_REVIEW')
    return True


def candidate(f,case,arm,exe):
    base=location(f)/'candidates'/e.digest(case['case_id']+'|'+arm)[:24]
    prompt=e.candidate_input(case);material=e.arm_material(e.ROOT,case['team_id'])[arm]
    e.require(e.digest(prompt)==f['cases'][case['case_id']]['input_sha256'],'CANDIDATE_INPUT_CHANGED')
    e.require(e.digest(material)==f['arm_material_sha256'][case['team_id']][arm],'CANDIDATE_ARM_CHANGED')
    for attempt in range(1,f['environment']['max_attempts_per_pair']+1):
        trial=base/str(attempt)
        if (trial/'receipt.json').is_file():
            r=e.load(trial/'receipt.json')
            if r['status']=='COMPLETED':
                parsed=verify_candidate(f,trial,set(),set())
                return r,parsed['response']
            if r['status']!='EXECUTION_BLOCKED':return r,None
            continue
        trial.mkdir(parents=True)
        (trial/'input.json').write_text(prompt,encoding='utf-8')
        out,err,code,start,end,latency,isolated=e.invoke(exe,prompt,material,f['environment']['timeout_seconds'])
        (trial/'stdout.jsonl').write_bytes(out);(trial/'stderr.txt').write_bytes(err)
        r={'host':'CLI_TEST','evaluation_mode':'SOLO_DEVELOPER','case_id':case['case_id'],'arm':arm,'attempt':attempt,
           'source_sha':f['source_sha'],'functional_source_sha':e.MODEL_SOURCE,'environment_digest':f['environment_digest'],
           'freeze_sha256':e.digest(f),'input_sha256':e.digest(prompt),'arm_sha256':e.digest(material),
           'raw_sha256':e.digest(out),'stderr_sha256':e.digest(err),'started_at':start,'ended_at':end,
           'latency_seconds':latency,'exit_code':code,'cli_version':f['cli_version'],'model_requested':e.MODEL,
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


def verify_candidate(f,trial,pairs,sessions):
    r=e.load(trial/'receipt.json');e.validate_observation(r)
    raw=(trial/'stdout.jsonl').read_bytes()
    e.require(e.digest(raw)==r['raw_sha256'] and e.digest((trial/'stderr.txt').read_bytes())==r['stderr_sha256'],'CANDIDATE_EVIDENCE_TAMPERED')
    e.require(e.digest((trial/'input.json').read_text(encoding='utf-8'))==r['input_sha256'],'CANDIDATE_RECORDED_INPUT_TAMPERED')
    parsed=e.parse_trace(raw,r['exit_code']);e.bind_trace(r,parsed,f,pairs,sessions)
    return parsed


def rows(f):
    result=[];pairs,sessions=set(),set()
    cases={x['case_id']:x for x in e.corpus(e.ROOT)}
    rubrics=e.load(e.ROOT/e.EVAL/'reviewer-case-criteria.json')['cases']
    for path in sorted(location(f).glob('candidates/*/*/receipt.json')):
        r=e.load(path)
        if r['status']!='COMPLETED':continue
        parsed=verify_candidate(f,path.parent,pairs,sessions);cid=r['case_id']
        binding={'source_sha':f['source_sha'],'freeze_sha256':e.digest(f),'candidate_raw_sha256':r['raw_sha256'],
                 'case_id':cid,'rubric_sha256':f['cases'][cid]['rubric_sha256']}
        grade=None;grade_receipt=None
        directory=location(f)/'grades'/r['raw_sha256']
        for gp in sorted(directory.glob('*/receipt.json')):
            gr=e.load(gp)
            if gr['status']!='GRADED':continue
            e.require(gr['binding']==binding and gr['input_sha256']==e.digest(e.encode(g.grade_input(cases[cid],rubrics[cid],parsed['response']))),'GRADER_BINDING_MISMATCH')
            gout=(gp.parent/'stdout.jsonl').read_bytes()
            e.require(e.digest(gout)==gr['raw_sha256'] and e.digest((gp.parent/'stderr.txt').read_bytes())==gr['stderr_sha256'],'GRADER_EVIDENCE_TAMPERED')
            p=e.parse_trace(gout,gr['exit_code'])
            e.require(p['session_sha256']==gr['session_sha256'] and p['session_sha256'] not in sessions,'REPLAYED_GRADER_SESSION')
            sessions.add(p['session_sha256'])
            grade=g.validate_grade(json.loads(p['response']),parsed['response'],rubrics[cid])
            e.require(e.digest(grade)==gr['grade_sha256'],'GRADER_RESULT_CHANGED')
            grade_receipt=gr
        result.append({'case_id':cid,'arm':r['arm'],'receipt':r,'grade':grade,'grade_receipt':grade_receipt})
    return result


def summary(f):
    data=rows(f);graded=[r for r in data if r['grade']]
    attempts=[e.load(p) for p in location(f).glob('candidates/*/*/receipt.json')]
    ga=[e.load(p) for p in location(f).glob('grades/*/*/receipt.json')]
    matrix=[]
    for team in sorted({x['team_id'] for x in e.corpus(e.ROOT)}):
        for band in ('normal','edge','adversarial'):
            group=[r for r in data if r['case_id'].startswith(team+':'+band+':')]
            for arm in e.ARMS:matrix.append({'team':team,'band':band,'arm':arm,**statistics(group,arm)})
    metric_matrix={}
    for metric in g.METRICS:
        counts=Counter(r['grade']['metrics'][metric]['status'] for r in graded)
        metric_matrix[metric]={'states':dict(counts),'denominator':sum(v for k,v in counts.items() if k!='NOT_OBSERVABLE')}
    return {'classification':g.configuration()['classification'],'source_sha':f['source_sha'],'freeze_sha256':e.digest(f),
            'candidate_attempts':len(attempts),'candidate_completed':len(data),'candidate_remaining':1080-len(data),
            'grader_invocations':len(ga),'graded':len(graded),'ungraded':len(data)-len(graded),
            'critical_pairs':sum(bool(r['grade']['critical_violations']) for r in graded),
            'contradiction_pairs':sum(bool(r['grade']['contradictions']) for r in graded),
            'high_uncertainty':sum(r['grade']['uncertainty']=='HIGH' for r in graded),
            'false_refusal_pairs':sum(r['grade']['refusal']['kind']=='IMPROPER' for r in graded),
            'appropriate_refusal_pairs':sum(r['grade']['refusal']['kind']=='APPROPRIATE' for r in graded),
            'candidate_outcomes':dict(Counter(r['status'] for r in attempts)),
            'grader_outcomes':dict(Counter(r['status'] for r in ga)),
            'candidate_usage':dict(sum((Counter(r.get('usage',{})) for r in attempts),Counter())),
            'grader_usage':dict(sum((Counter(r.get('usage',{})) for r in ga),Counter())),
            'candidate_latency_seconds':sum(r['latency_seconds'] for r in attempts),
            'grader_latency_seconds':sum(r['latency_seconds'] for r in ga),
            'per_arm':{arm:statistics(data,arm) for arm in e.ARMS},'matrix':matrix,'metric_matrix':metric_matrix,
            'model_identity':'REQUEST_ONLY_NOT_PROVIDER_ATTESTED','holdouts':'54_NONBLIND_REGRESSION_ONLY',
            'monetary_cost':'NOT_OBSERVABLE','H_HOST':'NOT_RUN','SMOKE_LAST':'NOT_RUN','release':'RELEASE_BLOCKED'}


def execute(freeze_path,stage,workers=4):
    f=e.validate_freeze(freeze_path)
    e.require(f['grader']==g.configuration(),'GRADER_CONFIGURATION_CHANGED')
    e.require(1<=workers<=f['max_parallel_subjects'],'EXCESS_SUBJECT_CONCURRENCY')
    base=location(f);base.mkdir(parents=True,exist_ok=True)
    if stage=='full':
        accepted=e.load(base/'pilot-acceptance.json')
        quality_gate(accepted['summary'])
        e.require(accepted['freeze_sha256']==e.digest(f),'STALE_PILOT_ACCEPTANCE')
        quality_gate(summary(f)) if len(rows(f))==36 else None
    exe=e.executable()
    auth=subprocess.run([exe,'login','status'],capture_output=True,env=e.minimal_env(),timeout=15)
    e.require(auth.returncode==0 and b'ChatGPT' in auth.stdout+auth.stderr,'CHATGPT_ACCOUNT_AUTH_REQUIRED')
    cases={x['case_id']:x for x in e.corpus(e.ROOT)};rubrics=e.load(e.ROOT/e.EVAL/'reviewer-case-criteria.json')['cases']
    existing={(r['case_id'],r['arm']) for r in rows(f) if r['grade']}
    planned=[tuple(x) for x in f[stage+'_order'] if tuple(x) not in existing]
    stop=threading.Event();blocked=[]
    def work(pair):
        cid,arm=pair
        if stop.is_set():return
        r,response=candidate(f,cases[cid],arm,exe)
        if r['status']!='COMPLETED':stop.set();blocked.append(r['status']);return
        if stop.is_set():return
        binding={'source_sha':f['source_sha'],'freeze_sha256':e.digest(f),'candidate_raw_sha256':r['raw_sha256'],
                 'case_id':cid,'rubric_sha256':f['cases'][cid]['rubric_sha256']}
        gr,result=g.grade(cases[cid],rubrics[cid],response,base/'grades'/r['raw_sha256'],binding,exe)
        print(cid,arm,r['status'],gr['status'],result['overall'] if result else '-',flush=True)
        if not result:stop.set();blocked.append(gr['status'])
    lock=base/'supervisor.lock'
    with lock.open('x') as out:out.write(e.now())
    try:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            iterator=iter(planned);active=set()
            for _ in range(workers):
                pair=next(iterator,None)
                if pair:active.add(pool.submit(work,pair))
            while active:
                done,active=wait(active,return_when=FIRST_COMPLETED)
                for future in done:
                    try:future.result()
                    except Exception as exc:stop.set();blocked.append(type(exc).__name__+':'+str(exc)[:300])
                if not stop.is_set():
                    for _ in done:
                        pair=next(iterator,None)
                        if pair:active.add(pool.submit(work,pair))
    finally:lock.unlink()
    result=summary(f)
    result['blocked']=blocked
    e.save_new(base/(stage+'-summary-'+e.now().replace(':','-')+'.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('matrix','metric_matrix')},indent=2))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['pilot','full','report'])
    p.add_argument('--freeze',required=True,type=Path);p.add_argument('--workers',type=int,default=4);p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.action=='report':
        f=e.validate_historical_freeze(a.freeze);result=summary(f)
        if a.output:e.save_new(a.output,result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('matrix','metric_matrix')},indent=2))
    else:execute(a.freeze,a.action,a.workers)


if __name__=='__main__':main()
