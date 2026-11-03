/* Pure offline file-level check of a rendered workcell manifest, no provider calls. */
import {readFile} from 'node:fs/promises';
import {join} from 'node:path';
async function main([dir,sha,countRaw]){
  const expectedCount=countRaw?Number(countRaw):null;
  if(expectedCount!==null&&(!Number.isSafeInteger(expectedCount)||expectedCount<1||expectedCount>50))throw new Error('INVALID_TEAM_COUNT');
  if(!dir||!sha||!(/^[0-9a-fA-F]{40}$/).test(sha))throw new Error('MANIFEST_VALIDATION_ARGS');
  const m=JSON.parse(await readFile(join(dir,'MANIFEST.json'),'utf8'));
  if(m.schema_version!=='prismcell-bootstrap-manifest-0.0.1'||m.installed!==false||m.provider_verified!==false||m.source_sha!==sha||!Array.isArray(m.teams)||m.teams.length<1||m.teams.length>50||(expectedCount!==null&&m.teams.length!==expectedCount))throw Error('MANIFEST_CONTRACT_MISMATCH');
  const names=new Set();
  for(const team of m.teams){
    if(names.has(team.team)||!Array.isArray(team.files)||team.files.length<17)throw Error('MANIFEST_TEAM_OR_FILES');
    names.add(team.team);
    const state=JSON.parse(await readFile(join(dir,team.team,'TEAM-WORKBENCH/STATE.json'),'utf8'));
    const checkpoint=JSON.parse(await readFile(join(dir,team.team,'TEAM-WORKBENCH/OPERATIONS-CHECKPOINT.json'),'utf8'));
    if(state.team!==team.team||state.home_branch!==team.branch||state.template_revision!==sha||state.release_authorized!==false||state.status!=='BOOTSTRAPPED_PENDING_LIVE_VERIFICATION'||checkpoint.issue_open!==null||checkpoint.background_process!==false)throw Error('MANIFEST_STATE_NOT_SAFE');
  }
  process.stdout.write('PRISMCELL_OFFLINE_MANIFEST_VERIFIED '+sha+'\n');
}
main(process.argv.slice(2)).catch(e=>{process.stderr.write('MANIFEST_DENIED '+e.message+'\n');process.exitCode=1});
