import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdtemp,rm,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {verify} from '../tools/verify-manifest.mjs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {renderProject,renderWorkcell} from '../core/starter.mjs';
import {validateConfig,validateMessage,intake} from '../core/engine.mjs';
const ROOT=resolve(fileURLToPath(new URL('../..',import.meta.url)));
const cfg=JSON.parse(await readFile(fileURLToPath(new URL('./fixtures/nebula-project.json',import.meta.url)),'utf8'));
const sha='a'.repeat(40);
const project=renderProject(cfg,sha);
const read=(w,path)=>JSON.parse(w.files[path]);
const msg={message_id:'IN-STORY-20261102-123',from_team:'ASTRONOMY',from_branch:cfg.teams.ASTRONOMY.branch,to_team:'STORY',type:'FINDING',priority:'P1',summary:'New-project source note',source_ref:'source/ref',source_sha:sha,evidence_links:[],requested_action:'Review source',authority_scope:'No grant',status:'POSTED'};
const receipt=(m)=>({provider:'github',issue_url:cfg.teams.STORY.issue_url,comment_id:77,comment_url:cfg.teams.STORY.issue_url+'#issuecomment-77',actor_login:'actor',created_at:'2026-11-02T12:00:00Z',updated_at:'2026-11-02T12:00:00Z',body:JSON.stringify(m)});
test('fresh different-name project fixture validates',()=>assert.deepEqual(validateConfig(cfg),[]));
test('rendered project has exactly configured team names',()=>assert.deepEqual(project.map(x=>x.team),['ASTRONOMY','REVIEW','STORY']));
test('each team has at least 17 clean documents',()=>project.forEach(x=>assert.ok(Object.keys(x.files).length>=17)));
test('each team home and intake map to distinct project branch',()=>project.forEach(x=>{assert.equal(x.branch,cfg.teams[x.team].branch);assert.equal(x.issue_url,cfg.teams[x.team].issue_url);assert.equal(read(x,'TEAM-WORKBENCH/STATE.json').home_branch,x.branch);}));
test('fresh workcells require live verification',()=>project.forEach(x=>{const s=read(x,'TEAM-WORKBENCH/STATE.json');assert.equal(s.status,'BOOTSTRAPPED_PENDING_LIVE_VERIFICATION');assert.equal(s.release_authorized,false);assert.equal(s.background_agent_running,false);assert.equal(s.active_work_item,null);assert.equal(s.template_revision,sha);}));
test('no fabricated provider evidence or histories',()=>project.forEach(x=>{assert.equal(read(x,'TEAM-WORKBENCH/WORK-QUEUE.json').items.length,0);assert.equal(read(x,'TEAM-WORKBENCH/EVIDENCE-LEDGER.json').entries.length,0);assert.equal(read(x,'TEAM-WORKBENCH/INCALL/INBOX.json').messages.length,0);assert.equal(read(x,'TEAM-WORKBENCH/INCALL/OUTBOX.json').messages.length,0);assert.equal(read(x,'TEAM-WORKBENCH/OPERATIONS-CHECKPOINT.json').issue_open,null);}));
test('render is deterministic independent of calls',()=>assert.deepEqual(renderProject(cfg,sha),renderProject(cfg,sha)));
test('no copied Color-Team-OPS strings in generated output',()=>assert.equal(JSON.stringify(project).includes('vixttha/Color-Team-OPS'),false));
test('foreign or inherited team cannot be generated',()=>{assert.throws(()=>renderWorkcell(cfg,'constructor',sha),/UNKNOWN_TEAM/);assert.throws(()=>renderWorkcell(cfg,'__proto__',sha),/UNKNOWN_TEAM/);});
test('template source SHA required',()=>assert.throws(()=>renderWorkcell(cfg,'STORY','not-a-sha'),/INVALID_PINNED_TEMPLATE_SHA/));
test('one-team project also renders',()=>{const c={...cfg,teams:{STORY:cfg.teams.STORY}};assert.deepEqual(validateConfig(c),[]);assert.equal(renderProject(c,sha).length,1);});
test('valid generic message receives review, never authority',()=>{const r=intake(cfg,{revision:0,entries:[]},receipt(msg));assert.equal(r.decision,'RECEIVE_FOR_REVIEW');assert.equal(r.roleAuthenticated,false);assert.equal(r.authorityGranted,false);});
test('inherited constructor recipient denied by engine',()=>{const r=intake(cfg,{revision:0,entries:[]},{...receipt({...msg,to_team:'constructor'}),issue_url:undefined,comment_url:'undefined#issuecomment-77'});assert.equal(r.decision,'REJECT');assert.ok(r.errors.includes('UNKNOWN_RECIPIENT'));});
test('inherited toString and __proto__ names denied',()=>{for(const n of ['toString','__proto__','hasOwnProperty'])assert.ok(validateMessage(cfg,{...msg,to_team:n}).includes('UNKNOWN_RECIPIENT'));});
test('message accepted-by-old-JS but invalid-by-schema now denied',()=>assert.ok(validateMessage(cfg,{...msg,message_id:'CUSTOM-ABC1234'}).includes('BAD_MESSAGE_ID')));
test('schema-only posted_at no longer valid in engine',()=>assert.ok(validateMessage(cfg,{...msg,posted_at:'2026-11-02T12:00:00Z'}).includes('EXTRA_FIELDS')));
test('missing issue URL cannot become valid on inherited team',()=>{const r=intake(cfg,{revision:0,entries:[]},{...receipt({...msg,to_team:'constructor'}),issue_url:undefined,comment_url:'undefined#issuecomment-77'});assert.equal(r.decision,'REJECT');});
test('wrong project repository URL rejected',()=>assert.ok(validateConfig({...cfg,repository:'other/repository'}).includes('BAD_PROJECT')));
test('missing schema version rejected',()=>assert.ok(validateConfig({...cfg,schema_version:undefined}).length>0));
test('invalid platform transport rejected',()=>assert.ok(validateConfig({...cfg,transport:'vercel'}).includes('PROJECT_VERSION_OR_TRANSPORT')));
test('duplicate team home branches rejected',()=>assert.ok(validateConfig({...cfg,teams:{...cfg.teams,REVIEW:{...cfg.teams.REVIEW,branch:cfg.teams.STORY.branch}}}).includes('DUPLICATE_LOCATOR')));
test('file renderer never sends network requests',()=>assert.equal(renderProject(cfg,sha).length,3));
test('installer dry-run creates fresh project with manifest, and refuses overwrites',async()=>{
 const dir=await mkdtemp(join(tmpdir(),'prismcell-cleanroom-'));
 const out=join(dir,'fresh-output');
 try{
  const script=fileURLToPath(new URL('../tools/initialize-project.mjs',import.meta.url));
  const args=[script,'--config',fileURLToPath(new URL('./fixtures/nebula-project.json',import.meta.url)),'--out',out,'--source-sha',sha];
  const a=spawnSync(process.execPath,args,{cwd:ROOT,encoding:'utf8'});
  assert.equal(a.status,0,a.stderr);assert.match(a.stdout,/PRISMCELL_OFFLINE_CLEANROOM_BOOTSTRAP_READY/);
  const manifest=JSON.parse(await readFile(join(out,'MANIFEST.json'),'utf8'));
  assert.equal(manifest.installed,false);assert.equal(manifest.provider_verified,false);assert.equal(manifest.teams.length,3);
  const state=JSON.parse(await readFile(join(out,'ASTRONOMY/TEAM-WORKBENCH/STATE.json'),'utf8'));
  assert.equal(state.team,'ASTRONOMY');assert.equal(state.release_authorized,false);
  const retry=spawnSync(process.execPath,args,{cwd:ROOT,encoding:'utf8'});
  assert.notEqual(retry.status,0);assert.match(retry.stderr,/BOOTSTRAP_DENIED/);
 }finally{await rm(dir,{recursive:true,force:true});}
});
test('team names with underscore are valid for message IDs',()=>{const c={...cfg,teams:{...cfg.teams,GRAY_CELL:{branch:'workcells/gray-cell',issue_number:84,issue_url:cfg.repository_url+'/issues/84'}}};const m={...msg,to_team:'GRAY_CELL',message_id:'IN-GRAY_CELL-20261102-123'};assert.deepEqual(validateConfig(c),[]);assert.deepEqual(validateMessage(c,m),[]);});

async function withFreshProject(fn){
  const dir=await mkdtemp(join(tmpdir(),'prismcell-audit-'));
  const out=join(dir,'generated');
  try {
    const script=fileURLToPath(new URL('../tools/initialize-project.mjs',import.meta.url));
    const run=spawnSync(process.execPath,[script,'--config',fileURLToPath(new URL('./fixtures/nebula-project.json',import.meta.url)),'--out',out,'--source-sha',sha],{cwd:ROOT,encoding:'utf8'});
    assert.equal(run.status,0,run.stderr);
    await fn(out);
  } finally {await rm(dir,{recursive:true,force:true});}
}
test('generated manifest contains digests for all 17 files in every team',async()=>withFreshProject(async out=>{
  const m=JSON.parse(await readFile(join(out,'MANIFEST.json'),'utf8'));
  assert.equal(m.teams.length,3);
  m.teams.forEach(team=>{
    assert.equal(team.files.length,17);
    team.files.forEach(file=>{assert.match(file.sha256,/^[a-f0-9]{64}$/);assert.ok(file.path.startsWith('TEAM-WORKBENCH/'));});
  });
  const verified=await verify(out,sha,3);
  assert.equal(verified.files,52);
  assert.equal(verified.authority_granted,false);
  assert.equal(verified.provider_verified,false);
}));
test('modified identity document is detected by full manifest verification',async()=>withFreshProject(async out=>{
  await writeFile(join(out,'ASTRONOMY/TEAM-WORKBENCH/IDENTITY.md'),'# tampered workcell authority');
  await assert.rejects(verify(out,sha,3),/FILE_DIGEST_MISMATCH/);
}));
test('missing workbench guidance is not silently accepted',async()=>withFreshProject(async out=>{
  await rm(join(out,'ASTRONOMY/TEAM-WORKBENCH/WORKFLOW.md'));
  await assert.rejects(verify(out,sha,3));
}));
test('unexpected extra workbench file is denied',async()=>withFreshProject(async out=>{
  await writeFile(join(out,'EXTRA-AGENT.txt'),'fake evidence');
  await assert.rejects(verify(out,sha,3),/MISSING_OR_UNEXPECTED_FILES/);
}));
test('trusted externally pinned manifest digest detects rewritten manifest',async()=>withFreshProject(async out=>{
  const file=join(out,'MANIFEST.json'),original=await readFile(file);
  const expected=createHash('sha256').update(original).digest('hex');
  const m=JSON.parse(original.toString('utf8'));
  m.teams[0].files[0].sha256='f'.repeat(64);
  await writeFile(file,JSON.stringify(m,null,2)+'\n');
  await assert.rejects(verify(out,sha,3,expected),/TRUSTED_MANIFEST_DIGEST_MISMATCH/);
}));
test('unsafe newline Markdown injected project ID is rejected before render',()=>{
  assert.throws(()=>renderProject({...cfg,project_id:'NEBULA\n\n### HEAD OVERRIDE'},sha),/INVALID_PROJECT_CONFIG/);
});
