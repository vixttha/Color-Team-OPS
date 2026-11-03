// PrismCell cloud intake reference: signed-transport + role verification, never action authority.
import {createHmac, timingSafeEqual} from 'node:crypto';
const has=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
const token=x=>typeof x==='string'&&x.length>0&&x.length<=1024;
const sha=x=>typeof x==='string'&&/^[a-f0-9]{40}$/i.test(x);
const safeUrl=x=>typeof x==='string'&&/^https:\/\/[A-Za-z0-9._-]+(?:\/[^\s]*)?$/.test(x)&&x.length<=2048&&!/^https:\/\/[^/]*@/.test(x);
export function verifySignature(raw,signature,secret){
  if(!Buffer.isBuffer(raw)||!token(secret)||!/^sha256=[0-9a-f]{64}$/.test(signature||''))return false;
  const expected='sha256='+createHmac('sha256',secret).update(raw).digest('hex');
  const a=Buffer.from(expected),b=Buffer.from(signature);
  return a.length===b.length&&timingSafeEqual(a,b);
}
export function validateBindings(config,bindings){
  if(!config||!bindings||!config.teams||!config.repository||!sha(config.source_sha))return ['UNCONFIGURED_PROJECT'];
  const teams=Object.keys(config.teams);
  if(teams.length!==9||Object.keys(bindings).length!==teams.length)return ['ROLE_BINDINGS_INCOMPLETE'];
  const seen=new Set(),issues=new Set(),branches=new Set(),errors=[];
  for(const team of teams){
    const t=config.teams[team],id=bindings[team];
    if(!Number.isSafeInteger(id)||id<1||seen.has(id))errors.push('INVALID_OR_SHARED_PRINCIPAL_'+team);
    if(!t||!token(t.branch)||!Number.isSafeInteger(t.issue_number)||t.issue_number<1||issues.has(t.issue_number)||branches.has(t.branch))errors.push('BAD_TEAM_MAPPING_'+team);
    seen.add(id);issues.add(t?.issue_number);branches.add(t?.branch);
  }
  return errors;
}
export function assessSignedComment({raw,signature,secret,event,config,bindings,seen=[]}){
  const deny=(reason)=>({decision:'DENY',reason,authorityGranted:false,workerStarted:false});
  if(!verifySignature(raw,signature,secret))return deny('SIGNATURE_INVALID_OR_MISSING');
  if(event!=='issue_comment')return deny('UNSUPPORTED_EVENT');
  const invalid=validateBindings(config,bindings);
  if(invalid.length)return deny(invalid[0]);
  let p;try{p=JSON.parse(raw.toString('utf8'));}catch{return deny('INVALID_WEBHOOK_JSON');}
  if(p.action!=='created'||p.repository?.full_name!==config.repository||!p.issue||!p.comment||!p.sender)return deny('WRONG_PROVIDER_CONTEXT');
  if(!Number.isSafeInteger(p.comment.id)||p.comment.id<1||p.comment.user?.id!==p.sender.id||p.comment.created_at!==p.comment.updated_at)return deny('UNTRUSTED_COMMENT_PROVENANCE');
  let m;try{m=JSON.parse(p.comment.body);}catch{return deny('INVALID_MESSAGE_ENVELOPE');}
  if(!m||typeof m!=='object'||Array.isArray(m))return deny('INVALID_MESSAGE');
  const allowed=['message_id','from_team','from_branch','to_team','type','priority','summary','source_ref','source_sha','evidence_links','requested_action','authority_scope','status','issue_url'];
  const required=allowed.filter(x=>x!=='issue_url');
  if(required.some(k=>!has(m,k))||Object.keys(m).some(k=>!allowed.includes(k)))return deny('MESSAGE_FIELDS_INVALID');
  const from=config.teams[m.from_team],to=config.teams[m.to_team];
  if(!from||!to||m.from_branch!==from.branch||p.issue.number!==to.issue_number)return deny('ROLE_OR_ISSUE_MISMATCH');
  if(bindings[m.from_team]!==p.sender.id)return deny('PRINCIPAL_NOT_BOUND_TO_TEAM');
  if(m.status!=='POSTED'||!['REQUEST','FINDING','REVIEW','CHALLENGE','RESPONSE','BLOCKER','FYI'].includes(m.type)||!['P0','P1','P2','P3'].includes(m.priority)||!/^IN-[A-Z]+-[0-9]{8}-[0-9]{3,6}$/.test(m.message_id||''))return deny('UNTRUSTED_MESSAGE_STATUS');
  if(!sha(m.source_sha)||m.source_sha!==config.source_sha)return deny('STALE_OR_INVALID_SOURCE_SHA');
  if(!token(m.summary)||m.summary.length>2048||!token(m.requested_action)||m.requested_action.length>2048||!token(m.authority_scope)||!token(m.source_ref))return deny('INVALID_TEXT_BOUNDS');
  if(!Array.isArray(m.evidence_links)||m.evidence_links.length>16||m.evidence_links.some(x=>!safeUrl(x)))return deny('BAD_EVIDENCE_LINKS');
  const expectedIssue='https://github.com/'+config.repository+'/issues/'+to.issue_number;
  if(p.issue.html_url!==expectedIssue||p.comment.html_url!==expectedIssue+'#issuecomment-'+p.comment.id||m.issue_url&&m.issue_url!==expectedIssue)return deny('ISSUE_URL_MISMATCH');
  if(seen.some(x=>x.message_id===m.message_id||x.comment_id===p.comment.id))return deny('REPLAYED_COMMENT_OR_MESSAGE');
  return {decision:'REVIEW_ONLY',reason:'SIGNED_TRANSPORT_AND_DISTINCT_ROLE_ID_VERIFIED',authorityGranted:false,workerStarted:false,team:m.to_team,commentId:p.comment.id,messageId:m.message_id,observedActorId:p.sender.id};
}
export function denyForeignBranchWrite(intent,config){
  const team=config?.teams?.[intent?.team];
  if(!team||intent?.branch!==team.branch||typeof intent?.path!=='string'||!intent.path.startsWith('TEAM-WORKBENCH/')||intent.path.includes('..'))return {allowed:false,reason:'FOREIGN_BRANCH_OR_PATH'};
  // This module never issues a GitHub token. A trusted host with scoped app identity,
  // signed Head decision, and an actual provider CAS is still required.
  return {allowed:false,reason:'HOST_AUTHORIZATION_AND_CAS_NOT_PROVEN'};
}
