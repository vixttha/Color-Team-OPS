/* PrismCell v0.0.1 universal deterministic intake engine.
   Pure functions, NO network, credentials, filesystem, permissions or autonomous dispatch.
   Host must fetch trusted provider receipts and enforce identity, ACL and compare-and-swap itself. */
const SHA = /^[a-fA-F0-9]{40}$/;
const ID = /^IN-[A-Z][A-Z0-9_]{1,39}-[0-9]{8}-[0-9]{3,6}$/;
const TEAM = /^[A-Z][A-Z0-9_]{1,39}$/;
const REPO = /^[A-Za-z0-9-]+\/[A-Za-z0-9._-]+$/;
const BRANCH = /^(?!\/)(?!.*(?:\.\.|\/\/|@\{|\\|[\x00-\x1f]))[A-Za-z0-9._\/-]+$/;
const allowedTypes = new Set(['REQUEST','FINDING','REVIEW','CHALLENGE','RESPONSE','BLOCKER','FYI']);
const priorities = new Set(['P0','P1','P2','P3']);
const text = (v,max=2048) => typeof v === 'string' && v.trim().length>0 && v.length<=max;
const url = v => text(v,2048) && /^https:\/\/[^\s/?#]+(?:\/[^\s]*)?$/.test(v) && !/https:\/\/(?:[^/@]*@)/.test(v);
const equal = (a,b) => JSON.stringify(a) === JSON.stringify(b);
const PROJECT_ID = /^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$/;
const validBranch = b => text(b,120) && BRANCH.test(b) && !b.startsWith('-') && b!=='HEAD' &&
  b.split('/').every(s=>s.length>0 && !s.startsWith('.') && !s.endsWith('.') && !s.endsWith('.lock'));
const validTime = v => typeof v==='string' && v.length<=60 &&
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(v) && Number.isFinite(Date.parse(v));
const decisionActions = new Set(['ACKNOWLEDGE','DEFER','BLOCK','REJECT']);
const ledgerStatuses = new Set(['RECEIVED_FOR_REVIEW',...decisionActions]);
const validLedgerEntry = e => !!e && typeof e==='object' && !Array.isArray(e) && ID.test(e.message_id||'') &&
  Number.isSafeInteger(e.comment_id) && e.comment_id>0 && url(e.comment_url) &&
  text(e.actor_login,100) && validTime(e.created_at) && validTime(e.updated_at) &&
  (SHA.test(e.source_sha||'') || e.source_sha==='unknown') && ledgerStatuses.has(e.status) &&
  (e.decision_history===undefined || (Array.isArray(e.decision_history) &&
    e.decision_history.every((v,i)=>v&&typeof v==='object'&&decisionActions.has(v.action)&&text(v.reason,1000)&&Number.isSafeInteger(v.revision)&&v.revision>0&&(i===0 || v.revision>e.decision_history[i-1].revision)) &&
    (e.decision_history.length===0 ? e.status==='RECEIVED_FOR_REVIEW' : e.status===e.decision_history.at(-1).action)));
const validLedger = l => !!l && typeof l==='object' && !Array.isArray(l) && Number.isSafeInteger(l.revision) && l.revision>=0 &&
  Array.isArray(l.entries) && l.entries.every(validLedgerEntry) &&
  new Set(l.entries.map(x=>x.comment_id)).size===l.entries.length &&
  new Set(l.entries.map(x=>x.message_id)).size===l.entries.length;

export function validateConfig(config) {
  const e=[];
  if(!config || typeof config!=='object' || Array.isArray(config))return ['INVALID_CONFIG'];
  const fields=['schema_version','project_id','repository','repository_url','transport','teams'];
  if(fields.some(k=>!Object.hasOwn(config,k)) || Object.keys(config).some(k=>!fields.includes(k)))e.push('PROJECT_FIELDS');
  if(config.schema_version!=='prismcell-project-config-0.0.1' || config.transport!=='github-issues-manual')e.push('PROJECT_VERSION_OR_TRANSPORT');
  if(!PROJECT_ID.test(config.project_id||'') || !REPO.test(config.repository||'') || config.repository_url!=='https://github.com/'+config.repository)e.push('BAD_PROJECT');
  if(!config.teams || typeof config.teams!=='object' || Array.isArray(config.teams))return [...e,'MISSING_TEAMS'];
  const names=Object.keys(config.teams);
  if(names.length<1 || names.length>50)e.push('TEAM_COUNT');
  const branchNames=[],issueNumbers=[];
  for(const [team,home] of Object.entries(config.teams)) {
    if(!TEAM.test(team) || !home || typeof home!=='object' || Array.isArray(home)) {e.push('BAD_TEAM_'+team);continue;}
    const keys=['branch','issue_number','issue_url'];
    if(keys.some(k=>!Object.hasOwn(home,k)) || Object.keys(home).some(k=>!keys.includes(k)))e.push('BAD_TEAM_FIELDS_'+team);
    if(!validBranch(home.branch) || !Number.isSafeInteger(home.issue_number) || home.issue_number<1 || home.issue_url!==config.repository_url+'/issues/'+home.issue_number)e.push('BAD_TEAM_'+team);
    branchNames.push(home.branch);issueNumbers.push(home.issue_number);
  }
  if(new Set(branchNames).size!==branchNames.length || new Set(issueNumbers).size!==issueNumbers.length)e.push('DUPLICATE_LOCATOR');
  return [...new Set(e)];
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
  if(!text(m.message_id,64) || !ID.test(m.message_id))e.push('BAD_MESSAGE_ID');
  else if(typeof m.to_team==='string' && !m.message_id.startsWith('IN-'+m.to_team+'-'))e.push('MESSAGE_ID_RECIPIENT_MISMATCH');
  const from=TEAM.test(m.from_team||'') && Object.hasOwn(config.teams,m.from_team)?config.teams[m.from_team]:null;
  const to=TEAM.test(m.to_team||'') && Object.hasOwn(config.teams,m.to_team)?config.teams[m.to_team]:null;
  if(!from || m.from_branch!==from.branch || !text(m.from_branch,120))e.push('CLAIMED_SENDER_BRANCH_MISMATCH');
  if(!to)e.push('UNKNOWN_RECIPIENT');
  if(!allowedTypes.has(m.type) || !priorities.has(m.priority))e.push('BAD_CLASSIFICATION');
  if(m.status!=='POSTED')e.push('SENDER_DECISION_FORBIDDEN');
  if(!text(m.summary,2048) || !text(m.requested_action,2048) || !text(m.authority_scope,1024) || !text(m.source_ref,180))e.push('BAD_TEXT');
  if(m.source_sha!=='unknown' && !SHA.test(m.source_sha||''))e.push('BAD_SOURCE_SHA');
  if(!Array.isArray(m.evidence_links) || m.evidence_links.length>16 || new Set(m.evidence_links).size!==m.evidence_links.length || m.evidence_links.some(x=>!url(x)))e.push('BAD_LINKS');
  if(Object.keys(m).some(k=>![...keys,'issue_url'].includes(k)))e.push('EXTRA_FIELDS');
  if(m.issue_url!==undefined && (!text(m.issue_url,300) || !url(m.issue_url) || m.issue_url!==to?.issue_url))e.push('WRONG_TARGET_URL');
  return [...new Set(e)];
}
export function intake(config, ledger, receipt, opts={}) {
  const errors=validateConfig(config);
  if(errors.length)return {decision:'REJECT',errors,authorityGranted:false,roleAuthenticated:false};
  const parsed=parseEnvelope(receipt?.body);
  errors.push(...parsed.errors);
  const m=parsed.message;
  if(m)errors.push(...validateMessage(config,m));
  if(m && opts.expected_source_sha && m.source_sha!==opts.expected_source_sha)errors.push('STALE_SOURCE_SHA');
  const team=m && TEAM.test(m.to_team||'') && Object.hasOwn(config.teams,m.to_team) ? config.teams[m.to_team] : null;
  if(!receipt || receipt.provider!=='github' || !team || !text(receipt.issue_url,300) || receipt.issue_url!==team.issue_url || !Number.isSafeInteger(receipt.comment_id) || receipt.comment_id<1 || receipt.comment_url!==(team.issue_url+'#issuecomment-'+receipt.comment_id) || !text(receipt.actor_login,100) || !validTime(receipt.created_at) || !validTime(receipt.updated_at))errors.push('UNVERIFIED_PROVIDER_METADATA');
  if(receipt?.created_at!==receipt?.updated_at)errors.push('EDITED_COMMENT_REVIEW');
  if(!validLedger(ledger))errors.push('BAD_LEDGER');
  if(ledger && opts.expected_revision!==undefined && ledger.revision!==opts.expected_revision)errors.push('STALE_CONCURRENT_WRITE');
  if(validLedger(ledger) && ledger.entries.some(x=>x.comment_id===receipt?.comment_id || x.message_id===m?.message_id))errors.push('DUPLICATE_OR_REPLAY');
  if(!receipt?.body || receipt.body.length>12000)errors.push('OVERSIZED_BODY');
  // The host must compare provider-retrieved receipt to its own trusted API response.
  // No claim of role authentication even if transport author equals the repo owner.
  if(errors.length)return {decision:'REJECT',errors:[...new Set(errors)],authorityGranted:false,roleAuthenticated:false,ledger};
  const entry={message_id:m.message_id,comment_id:receipt.comment_id,comment_url:receipt.comment_url,actor_login:receipt.actor_login,created_at:receipt.created_at,updated_at:receipt.updated_at,source_sha:m.source_sha,status:'RECEIVED_FOR_REVIEW',decision_history:[],from_team_claim:m.from_team,to_team:m.to_team};
  return {decision:'RECEIVE_FOR_REVIEW',errors:[],authorityGranted:false,roleAuthenticated:false,ledger:{...ledger,revision:ledger.revision+1,entries:[...ledger.entries,entry]}};
}
export function decide(config,ledger,decision,expected_revision) {
  if(validateConfig(config).length || !validLedger(ledger) || ledger.revision!==expected_revision)return {ok:false,reason:'STALE_OR_INVALID',authorityGranted:false};
  if(!decision || !decisionActions.has(decision.action) || !text(decision.reason,1000) || !ID.test(decision.message_id||''))return {ok:false,reason:'INVALID_DECISION',authorityGranted:false};
  const idx=ledger.entries.findIndex(e=>e.message_id===decision.message_id);
  if(idx<0)return {ok:false,reason:'UNKNOWN_MESSAGE',authorityGranted:false};
  if(ledger.entries[idx].status!=='RECEIVED_FOR_REVIEW' || (ledger.entries[idx].decision_history?.length||0)!==0)return {ok:false,reason:'ALREADY_DECIDED',authorityGranted:false};
  const event={action:decision.action,reason:decision.reason,revision:ledger.revision+1};
  const next=ledger.entries.map((v,i)=>i===idx?{...v,status:decision.action,reason:decision.reason,decision_history:[...(v.decision_history||[]),event]}:v);
  return {ok:true,authorityGranted:false,ledger:{...ledger,revision:ledger.revision+1,entries:next}};
}
export function resume(checkpoint, latest) {
  if(!checkpoint || !Number.isSafeInteger(checkpoint.revision) || checkpoint.revision<0 ||
      !Array.isArray(checkpoint.processed_comment_ids||[]) ||
      (checkpoint.processed_comment_ids||[]).some(id=>!Number.isSafeInteger(id)||id<1) ||
      new Set(checkpoint.processed_comment_ids||[]).size!==(checkpoint.processed_comment_ids||[]).length ||
      !validLedger(latest))return {ok:false,reason:'INVALID_CHECKPOINT',authorityGranted:false};
  if(latest.revision<checkpoint.revision)return {ok:false,reason:'HISTORY_REGRESSION',authorityGranted:false};
  const ids=new Set(latest.entries.map(e=>e.comment_id));
  for(const id of checkpoint.processed_comment_ids||[])if(!ids.has(id))return {ok:false,reason:'HISTORY_LOSS',authorityGranted:false};
  return {ok:true,revision:latest.revision,pending:latest.entries.filter(e=>e.status==='RECEIVED_FOR_REVIEW'),authorityGranted:false};
}
export function migrateState(state,config,pinnedSha) {
  const e=validateConfig(config);
  if(e.length || !state || !TEAM.test(state.team||'') || !Object.hasOwn(config.teams,state.team) || state.home_branch!==config.teams[state.team].branch || state.release_authorized!==false || !SHA.test(pinnedSha||''))return {ok:false,errors:e.length?e:['INVALID_LEGACY_STATE']};
  const migrated={...state,template_revision:pinnedSha,core_policy_revision:'prismcell-core-0.0.1',migration:{status:'PINNED_WITH_HISTORY_PRESERVED',from_version:state.version,source:'PRISMCELL_WORKBENCH_OPTION_D'}};
  return {ok:true,state:migrated};
}
