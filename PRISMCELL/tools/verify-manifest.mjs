/* PrismCell v0.0.1 offline full manifest integrity and safe-state checker.
 * Compares EVERY generated file to per-file SHA256 and rejects missing/extra/symlinked files.
 * An untrusted manifest can be rewritten with its files; pin manifest digest in a trusted host
 * for authenticity. A local hash is NOT a GitHub signature or proof of owner approval. */
import {readFile,readdir,lstat} from 'node:fs/promises';
import {join,relative,sep} from 'node:path';
import {createHash} from 'node:crypto';
import {REQUIRED_WORKCELL_FILES} from '../core/starter.mjs';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const fail=reason=>{throw new Error(reason);};
const same=(a,b)=>a.length===b.length && a.every((x,i)=>x===b[i]);
async function enumerate(root,dir=root) {
  const result=[];
  for(const de of await readdir(dir,{withFileTypes:true})){
    const path=join(dir,de.name), info=await lstat(path);
    if(info.isSymbolicLink())fail('SYMLINK_FORBIDDEN');
    if(info.isDirectory())result.push(...await enumerate(root,path));
    else if(info.isFile())result.push(relative(root,path).split(sep).join('/'));
    else fail('UNSUPPORTED_FILESYSTEM_NODE');
  }
  return result;
}
export async function verify(dir,sha,countRaw,expectedManifestDigest){
  const expectedCount=countRaw===undefined?null:Number(countRaw);
  if(expectedCount!==null&&(!Number.isSafeInteger(expectedCount)||expectedCount<1||expectedCount>50))fail('INVALID_TEAM_COUNT');
  if(!dir||typeof sha!=='string'||!(/^[0-9a-fA-F]{40}$/).test(sha))fail('MANIFEST_VALIDATION_ARGS');
  const root=await lstat(dir);if(!root.isDirectory()||root.isSymbolicLink())fail('INVALID_ROOT_FOLDER');
  const manifestBytes=await readFile(join(dir,'MANIFEST.json'));
  if(expectedManifestDigest!==undefined && (!/^[0-9a-f]{64}$/.test(expectedManifestDigest)||hash(manifestBytes)!==expectedManifestDigest))fail('TRUSTED_MANIFEST_DIGEST_MISMATCH');
  const m=JSON.parse(manifestBytes.toString('utf8'));
  if(!m||m.schema_version!=='prismcell-bootstrap-manifest-0.0.1'||m.installed!==false||m.provider_verified!==false||
     m.source_sha!==sha||!Array.isArray(m.teams)||m.teams.length<1||m.teams.length>50||
     (expectedCount!==null&&m.teams.length!==expectedCount))fail('MANIFEST_CONTRACT_MISMATCH');
  const names=new Set(),expected=new Set(['MANIFEST.json']);
  for(const team of m.teams) {
    if(!team||typeof team!=='object'||typeof team.team!=='string'||!/^[A-Z][A-Z0-9_]{1,39}$/.test(team.team)||
       names.has(team.team)||typeof team.branch!=='string'||typeof team.issue_url!=='string'||
       !Array.isArray(team.files)||team.files.length!==REQUIRED_WORKCELL_FILES.length)fail('MANIFEST_TEAM_OR_FILES');
    names.add(team.team);
    const actualPaths=[];
    for(const record of team.files){
      if(!record||typeof record.path!=='string'||!REQUIRED_WORKCELL_FILES.includes(record.path)||
         typeof record.sha256!=='string'||!/^[a-f0-9]{64}$/.test(record.sha256)||
         actualPaths.includes(record.path))fail('MANIFEST_FILE_RECORD');
      actualPaths.push(record.path);
      const rel=team.team+'/'+record.path;
      if(expected.has(rel))fail('DUPLICATE_FILE');
      expected.add(rel);
      const bytes=await readFile(join(dir,team.team,record.path));
      if(hash(bytes)!==record.sha256)fail('FILE_DIGEST_MISMATCH_'+rel);
    }
    if(!same(actualPaths.sort(),REQUIRED_WORKCELL_FILES))fail('INCOMPLETE_WORKCELL');
    const read=async p=>JSON.parse(await readFile(join(dir,team.team,p),'utf8'));
    const [state,checkpoint,queue,inbox,outbox,evidence]=await Promise.all([
      'TEAM-WORKBENCH/STATE.json','TEAM-WORKBENCH/OPERATIONS-CHECKPOINT.json',
      'TEAM-WORKBENCH/WORK-QUEUE.json','TEAM-WORKBENCH/INCALL/INBOX.json',
      'TEAM-WORKBENCH/INCALL/OUTBOX.json','TEAM-WORKBENCH/EVIDENCE-LEDGER.json'
    ].map(read));
    if(state.team!==team.team||state.home_branch!==team.branch||state.incall_issue!==team.issue_url||
       state.template_revision!==sha||state.release_authorized!==false||state.status!=='BOOTSTRAPPED_PENDING_LIVE_VERIFICATION'||
       state.background_agent_running!==false||state.active_work_item!==null||checkpoint.issue_open!==null||
       checkpoint.background_process!==false||checkpoint.home_branch!==team.branch||checkpoint.template_revision!==sha||
       !Array.isArray(queue.items)||queue.items.length!==0||
       !Array.isArray(inbox.messages)||inbox.messages.length!==0||
       !Array.isArray(outbox.messages)||outbox.messages.length!==0||
       !Array.isArray(evidence.entries)||evidence.entries.length!==0)fail('WORKCELL_PRE_ACTIVATION_STATE_INVALID');
  }
  const actual=await enumerate(dir);
  if(!same(actual.sort(),[...expected].sort()))fail('MISSING_OR_UNEXPECTED_FILES');
  return {ok:true,teams:names.size,files:expected.size,source_sha:sha,manifest_digest:hash(manifestBytes),
    provider_verified:false,authority_granted:false};
}
async function main(args){
  const [dir,sha,countRaw,expectedManifestDigest]=args;
  const result=await verify(dir,sha,countRaw,expectedManifestDigest);
  process.stdout.write('PRISMCELL_OFFLINE_MANIFEST_VERIFIED '+result.source_sha+' '+result.files+' files; provider UNVERIFIED\n');
}
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  main(process.argv.slice(2)).catch(e=>{process.stderr.write('MANIFEST_DENIED '+e.message+'\n');process.exitCode=1});
}
