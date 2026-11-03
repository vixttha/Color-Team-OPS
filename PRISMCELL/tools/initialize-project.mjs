/* Optional offline provisioning utility. No GitHub API requests or credentials. */
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {renderProject} from '../core/starter.mjs';
async function main(args){
  const flags={};
  for(let i=0;i<args.length;i+=2){
    if(!['--config','--out','--source-sha'].includes(args[i])||!args[i+1]||Object.hasOwn(flags,args[i]))throw Error('USAGE: --config project.json --out NEW_EMPTY_DIR --source-sha 40_HEX');
    flags[args[i]]=args[i+1];
  }
  if(Object.keys(flags).length!==3)throw Error('Missing --config, --out or --source-sha');
  const config=JSON.parse(await readFile(resolve(flags['--config']),'utf8'));
  const project=renderProject(config,flags['--source-sha']);
  const output=resolve(flags['--out']);
  // Exclusive first mkdir refuses an already-existing folder, so a dry run never overwrites existing work.
  await mkdir(output,{recursive:false});
  for(const workcell of project){
    for(const [file,content] of Object.entries(workcell.files).sort(([a],[b])=>a.localeCompare(b))){
      const target=join(output,workcell.team,file);
      await mkdir(dirname(target),{recursive:true});
      await writeFile(target,content,{flag:'wx'});
    }
  }
  await writeFile(join(output,'MANIFEST.json'),JSON.stringify({
    schema_version:'prismcell-bootstrap-manifest-0.0.1',
    project_id:config.project_id,repository:config.repository,source_sha:flags['--source-sha'],
    installed:false,provider_verified:false,teams:project.map(({team,branch,issue_url,files})=>({team,branch,issue_url,files:Object.keys(files).sort()}))
  },null,2)+'\n',{flag:'wx'});
  process.stdout.write('PRISMCELL_OFFLINE_CLEANROOM_BOOTSTRAP_READY '+output+'\n');
}
if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  main(process.argv.slice(2)).catch(e=>{process.stderr.write('BOOTSTRAP_DENIED '+e.message+'\n');process.exitCode=1});
}
export {main};
