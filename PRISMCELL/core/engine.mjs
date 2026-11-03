/* PrismCell v0.0.1 universal deterministic intake engine.
   Pure functions, NO network, credentials, filesystem, permissions or autonomous dispatch.
   Host must fetch trusted provider receipts and enforce identity, ACL and compare-and-swap itself. */
const SHA = /^[a-fA-F0-9]{40}$/;
const ID = /^[A-Z][A-Z0-9_-]{7,79}$/;
const allowedTypes = new Set(['REQUEST','FINDING','REVIEW','CHALLENGE','RESPONSE','BLOCKER','FYI']);
const priorities = new Set(['P0','P1','P2','P3']);
const text = (v,max=2048) => typeof v === 'string' && v.trim().length>0 && v.length<=max;
const url = v => text(v,2048) && /^https:\/\/[^\s/?#]+(?:\/[^\s]*)?$/.test(v) && !/https:\/\/(?:[^/@]*@)/.test(v);
const equal = (a,b) => JSON.stringify(a) === JSON.stringify(b);
export function validateConfig(config) {
  const e=[];
  if(!config || typeof config!=='object' || Array.isArray(config))return ['INVALID_CONFIG'];
  if(!text(config.project_id,100) || !text(config.repository,200) || !url(config.repository_url))e.push('BAD_PROJECT');
  if(!config.teams || typeof config.teams!=='object' || Array.isArray(config.teams))return [...e,'MISSING_TEAMS'];
  const names=Object.keys(config.teams);
  if(names.length<2 || names.length>50 || new Set(names).size!==names.length)e.push('TEAM_COUNT');
  for(const [team,home] of Object.entries(config.teams)) {
    if(!/^[A-Z][A-Z0-9_]{1,39}$/.test(team) || !home || !text(home.branch,200) || !url(home.issue_url) || !Number.isSafeInteger(home.issue_number) || home.issue_number<1)e.push('BAD_TEAM_'+team);
    if(home && url(home.issue_url) && !home.issue_url.startsWith(config.repository_url+'/issues/'))e.push('ISSUE_REPO_MISMATCH_'+team);
    if(home && home.issue_url!==(config.repository_url+'/issues/'+home.issue_number))e.push('ISSUE_NUMBER_MISMATCH_'+team);
  }
  const branches=Object.values(config.teams).map(v=>v?.branch), issues=Object.values(config.teams).map(v=>v?.issue_number);
  if(new Set(branches).size!==branches.length || new Set(issues).size!==issues.length)e.push('DUPLICATE_LOCATOR');
  return e;
}
export function parseEnvelope(body) {
  if(!text(body,12000))return {message:null,errors:['INVALID_BODY']};
  const clean=body.trim();
  const match=clean.match(/^```prismcell-json\n([\s\S]+)\n```$/);
  let m;
  try {m=JSON.parse(match?match[1]:clean);}catch{return {message:null,errors:['INVALID_JSON_ENVELOPE']};}
  if(!m || typeof m!=='object' || Array.isArray(m))return {message:null,errors:['INVALID_ENVELOPE_OBJECT']};
  return {message:m,errors:[]};
}
export function validateMessage(config,message) {
  const e=validateConfig(config);
  if(e.length)return e;
  const m=message;
  if(!m || typeof m!=='object' || Array.isArray(m))return ['BAD_MESSAGE'];
  const keys=['message_id','from_team','from_branch','to_team','type','priority','summary','source_ref','source_sha','evidence_links','requested_action','authority_scope','status'];
  if(keys.some(k=>!Object.hasOwn(m,k)))e.push('MISSING_FIELDS');
  if(!ID.test(m.message_id||''))e.push('BAD_MESSAGE_ID');
  if(!config.teams[m.from_team] || m.from_branch!==config.teams[m.from_team]?.branch)e.push('CLAIMED_SENDER_BRANCH_MISMATCH');
  if(!config.teams[m.to_team])e.push('UNKNOWN_RECIPIENT');
  if(!allowedTypes.has(m.type) || !priorities.has(m.priority))e.push('BAD_CLASSIFICATION');
  if(m.status!=='POSTED')e.push('SENDER_DECISION_FORBIDDEN');
  if(!text(m.summary) || !text(m.requested_action) || !text(m.authority_scope,1024) || !text(m.source_ref,200))e.push('BAD_TEXT');
  if(m.source_sha!=='unknown' && !SHA.test(m.source_sha||''))e.push('BAD_SOURCE_SHA');
  if(!Array.isArray(m.evidence_links) || m.evidence_links.length>16 || new Set(m.evidence_links).size!==m.evidence_links.length || m.evidence_links.some(x=>!url(x)))e.push('BAD_LINKS');
  if(Object.keys(m).some(k=>![...keys,'issue_url'].includes(k)))e.push('EXTRA_FIELDS');
  if(m.issue_url!==undefined && m.issue_url!==config.teams[m.to_team]?.issue_url)e.push('WRONG_TARGET_URL');
  return e;
}
export function intake(config, ledger, receipt, opts={}) {
  const errors=validateConfig(config);
  if(errors.length)return {decision:'REJECT',errors,authorityGranted:false,roleAuthenticated:false};
  const parsed=parseEnvelope(receipt?.body);
  errors.push(...parsed.errors);
  const m=parsed.message;
  if(m)errors.push(...validateMessage(config,m));
  const team=m && config.teams[m.to_team];
  if(!receipt || receipt.provider!=='github' || !team || receipt.issue_url!==team.issue_url || !Number.isSafeInteger(receipt.comment_id) || receipt.comment_id<1 || receipt.comment_url!==(team.issue_url+'#issuecomment-'+receipt.comment_id) || !text(receipt.actor_login,100) || !text(receipt.created_at,60) || !text(receipt.updated_at,60))errors.push('UNVERIFIED_PROVIDER_METADATA');
  if(receipt?.created_at!==receipt?.updated_at)errors.push('EDITED_COMMENT_REVIEW');
  if(!ledger || !Number.isSafeInteger(ledger.revision) || ledger.revision<0 || !Array.isArray(ledger.entries))errors.push('BAD_LEDGER');
  if(ledger && opts.expected_revision!==undefined && ledger.revision!==opts.expected_revision)errors.push('STALE_CONCURRENT_WRITE');
  if(ledger?.entries?.some(x=>x.comment_id===receipt?.comment_id || x.message_id===m?.message_id))errors.push('DUPLICATE_OR_REPLAY');
  if(!receipt?.body || receipt.body.length>12000)errors.push('OVERSIZED_BODY');
  // The host must compare provider-retrieved receipt to its own trusted API response.
  // No claim of role authentication even if transport author equals the repo owner.
  if(errors.length)return {decision:'REJECT',errors:[...new Set(errors)],authorityGranted:false,roleAuthenticated:false,ledger};
  const entry={message_id:m.message_id,comment_id:receipt.comment_id,comment_url:receipt.comment_url,actor_login:receipt.actor_login,created_at:receipt.created_at,updated_at:receipt.updated_at,source_sha:m.source_sha,status:'RECEIVED_FOR_REVIEW',from_team_claim:m.from_team,to_team:m.to_team};
  return {decision:'RECEIVE_FOR_REVIEW',errors:[],authorityGranted:false,roleAuthenticated:false,ledger:{...ledger,revision:ledger.revision+1,entries:[...ledger.entries,entry]}};
}
export function decide(config,ledger,decision,expected_revision) {
  if(validateConfig(config).length || !ledger || ledger.revision!==expected_revision || !Array.isArray(ledger.entries))return {ok:false,reason:'STALE_OR_INVALID'};
  if(!decision || !['ACKNOWLEDGE','DEFER','BLOCK','REJECT'].includes(decision.action) || !text(decision.reason,1000) || !text(decision.message_id,80))return {ok:false,reason:'INVALID_DECISION'};
  const idx=ledger.entries.findIndex(e=>e.message_id===decision.message_id);
  if(idx<0)return {ok:false,reason:'UNKNOWN_MESSAGE'};
  const next=ledger.entries.map((v,i)=>i===idx?{...v,status:decision.action,reason:decision.reason}:v);
  return {ok:true,authorityGranted:false,ledger:{...ledger,revision:ledger.revision+1,entries:next}};
}
export function resume(checkpoint, latest) {
  if(!checkpoint || !latest || !Number.isSafeInteger(checkpoint.revision) || !Number.isSafeInteger(latest.revision) || !Array.isArray(latest.entries))return {ok:false,reason:'INVALID_CHECKPOINT'};
  if(latest.revision<checkpoint.revision)return {ok:false,reason:'HISTORY_REGRESSION'};
  const ids=new Set();
  for(const e of latest.entries){if(ids.has(e.comment_id))return {ok:false,reason:'HISTORY_DUPLICATION'};ids.add(e.comment_id);}
  for(const id of checkpoint.processed_comment_ids||[])if(!ids.has(id))return {ok:false,reason:'HISTORY_LOSS'};
  return {ok:true,revision:latest.revision,pending:latest.entries.filter(e=>e.status==='RECEIVED_FOR_REVIEW'),authorityGranted:false};
}
export function migrateState(state,config,pinnedSha) {
  const e=validateConfig(config);
  if(e.length || !state || !config.teams[state.team] || state.home_branch!==config.teams[state.team].branch || state.release_authorized!==false || !SHA.test(pinnedSha||''))return {ok:false,errors:e.length?e:['INVALID_LEGACY_STATE']};
  const migrated={...state,template_revision:pinnedSha,core_policy_revision:'prismcell-core-0.0.1',migration:{status:'PINNED_WITH_HISTORY_PRESERVED',from_version:state.version,source:'PRISMCELL_WORKBENCH_OPTION_D'}};
  return {ok:true,state:migrated};
}
