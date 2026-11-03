// PrismCell Workbench v0.0.1 — portable pure JS reference guard (not a permission issuer).
// Caller MUST supply genuine GitHub API metadata; any caller can fake args, so this NEVER authenticates a team principal.
const homes = {
  "YELLOW": "agent/YELLOW-TEAM-AGENT",
  "ORANGE": "agent/ORANGE-TEAM-AGENT",
  "GREEN": "agent/GREEN-TEAM-AGENT",
  "RED": "team/red-team-agent",
  "BLUE": "agents/blue-team-agent",
  "PURPLE": "agent/PURPLE-TEAM-AGENT",
  "WHITE": "agent/WHITE-TEAM-AGENT",
  "BLACK": "agent/BLACK-TEAM-AGENT",
  "GRAY": "agent/GRAY-CELL-AGENT"
};
const issues = {
  "YELLOW": 9,
  "ORANGE": 10,
  "GREEN": 11,
  "RED": 12,
  "BLUE": 13,
  "PURPLE": 14,
  "WHITE": 15,
  "BLACK": 16,
  "GRAY": 17
};
const fields = ["message_id","from_team","from_branch","to_team","type","priority","summary","source_ref","source_sha","evidence_links","requested_action","authority_scope","status"];
function strVal(x){return typeof x==="string"&&x.trim().length>0;}
function guardMessage(m,trusted,seen=[]){
const errors=[];const home=homes[m?.from_team],issue=issues[m?.to_team];
const str=(v,max=2048)=>typeof v==="string"&&v.length>0&&v.length<=max;
if(!m||typeof m!=="object"||Array.isArray(m))return {triage:false,roleAuthenticated:false,authorityGranted:false,errors:["BAD_MESSAGE"]};
for(const x of fields)if(!Object.hasOwn(m,x))errors.push("MISSING_"+x);
if(!str(m.message_id,64)||!/^IN-[A-Z]+-\d{8}-\d{3,6}$/.test(m.message_id))errors.push("BAD_ID");
if(!home||m.from_branch!==home)errors.push("CLAIMED_TEAM_BRANCH_MISMATCH");
if(!issue)errors.push("UNKNOWN_RECIPIENT");
if(m.status!=="POSTED")errors.push("SENDER_CANNOT_SET_DECISION");
if(!/^(?:[a-fA-F0-9]{40}|unknown)$/.test(m.source_sha||""))errors.push("BAD_SHA");
if(!str(m.summary)||!str(m.requested_action)||!str(m.authority_scope,1024)||!str(m.source_ref,180))errors.push("BAD_TEXT");
if(!["REQUEST","FINDING","REVIEW","CHALLENGE","RESPONSE","BLOCKER","FYI"].includes(m.type)||!["P0","P1","P2","P3"].includes(m.priority))errors.push("BAD_ENUM");
if(!Array.isArray(m.evidence_links)||m.evidence_links.length>16||m.evidence_links.some(x=>!str(x)||!x.startsWith("https://"))||new Set(m.evidence_links).size!==m.evidence_links.length)errors.push("BAD_EVIDENCE_URL");
if(!trusted||typeof trusted!=="object"||trusted.issue_number!==issue||trusted.issue_url!==`https://github.com/vixttha/Color-Team-OPS/issues/${issue}`||!Number.isSafeInteger(trusted.comment_id)||trusted.comment_id<1||!str(trusted.actor_login,100)||!str(trusted.created_at,100)||!str(trusted.updated_at,100)||!str(trusted.body,16000))errors.push("MISSING_TRUSTED_GITHUB_METADATA");
else{
if(trusted.created_at!==trusted.updated_at)errors.push("EDITED_COMMENT_REQUIRES_MANUAL_REVIEW");
if(!trusted.body.includes(`message_id: ${m.message_id}`)||!trusted.body.includes(`source_sha: ${m.source_sha}`))errors.push("COMMENT_BODY_MISMATCH");
if(seen.some(x=>x.message_id===m.message_id||x.comment_id===trusted.comment_id))errors.push("DUPLICATE_OR_REPLAY");
}
return {triage:errors.length===0,roleAuthenticated:false,authorityGranted:false,observedActor:trusted?.actor_login||null,errors};
}
function guardWorkItem(w){
const errors=[];if(!w||typeof w!=="object"||Array.isArray(w))return{valid:false,errors:["BAD_WORK_ITEM"]};
if(!strVal(w.id)||!strVal(w.title)||!["P0","P1","P2","P3"].includes(w.priority)||!Array.isArray(w.acceptance_criteria)||!w.acceptance_criteria.length)errors.push("BAD_BASE");
if(!["QUEUED","ACTIVE","IMPLEMENTED_UNVERIFIED","VALIDATED","AUDITED","ACCEPTED","BLOCKED","DEFERRED","REJECTED"].includes(w.status))errors.push("BAD_STATUS");
if(w.status==="ACCEPTED"){
if(!/^[a-fA-F0-9]{40}$/.test(w.source_sha||""))errors.push("MISSING_EXACT_SHA");
if(!["OBSERVED_SOURCE","EXECUTED_AT_SHA","VERIFIED_PROVIDER","RESEARCH_CITED"].includes(w.evidence_status))errors.push("EVIDENCE_NOT_ACCEPTABLE");
if(!Array.isArray(w.evidence_refs)||!w.evidence_refs.length||w.evidence_refs.some(x=>!strVal(x)||!x.startsWith("https://")))errors.push("MISSING_EVIDENCE");
if(!homes[w.assigned_team]||!strVal(w.assigned_role)||!strVal(w.scope)||!["LOW","MEDIUM","HIGH","CRITICAL"].includes(w.risk)||!Array.isArray(w.prerequisites))errors.push("MISSING_CONTRACT_FIELDS");
if(!w.budget||!Number.isInteger(w.budget.max_repairs)||w.budget.max_repairs<0||w.budget.max_repairs>2||!Number.isInteger(w.repair_count)||w.repair_count>w.budget.max_repairs||w.repair_count<0)errors.push("BAD_REPAIR_BUDGET");
if(w.validation?.result!=="PASS"||!strVal(w.validation?.evidence_ref)||w.internal_audit?.result!=="PASS"||!strVal(w.internal_audit?.evidence_ref))errors.push("VALIDATION_AUDIT_INCOMPLETE");
if(w.head_decision?.result!=="ACCEPT"||!strVal(w.head_decision?.decision_ref))errors.push("HEAD_NOT_ACCEPTED");
}
return {valid:errors.length===0,errors};
}
function guardState(s){
const errors=[];
if(!s||typeof s!=="object"||Array.isArray(s))return{valid:false,errors:["BAD_STATE"]};
if(s.schema_version!=="prismcell-state-0.0.1"||s.template!=="PrismCell Workbench"||s.version!=="0.0.1")errors.push("BAD_VERSION");
if(!homes[s.team]||s.home_branch!==homes[s.team])errors.push("TEAM_BRANCH_MISMATCH");
if(s.release_authorized!==false)errors.push("UNAUTHORIZED_RELEASE_STATE");
if(s.last_verified_product_sha!==null&&s.last_verified_product_sha!==undefined&&!/^[a-fA-F0-9]{40}$/.test(s.last_verified_product_sha))errors.push("BAD_SOURCE_SHA");
if(s.template_revision!==undefined&&!/^[a-fA-F0-9]{40}$/.test(s.template_revision))errors.push("BAD_TEMPLATE_REVISION");
return{valid:errors.length===0,errors};
}
export {guardMessage,guardWorkItem,guardState,homes,issues};
