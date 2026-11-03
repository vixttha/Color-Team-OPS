// Execute with: node --test PRISMCELL/tests/guard.test.mjs (optional development host only).
import test from "node:test";
import assert from "node:assert/strict";
import {guardMessage,guardWorkItem,guardState,homes} from "../tools/guard.mjs";
const msg={
  "message_id": "IN-ORANGE-20261102-001",
  "from_team": "BLUE",
  "from_branch": "agents/blue-team-agent",
  "to_team": "ORANGE",
  "type": "FINDING",
  "priority": "P1",
  "summary": "Source schema status issue",
  "source_ref": "template/prismcell-workbench-v0.0.1",
  "source_sha": "62d43ef51d362cf064c367158a8d7fce207abd68",
  "evidence_links": [
    "https://github.com/vixttha/Color-Team-OPS/issues/10"
  ],
  "requested_action": "Review schema",
  "authority_scope": "Read only",
  "status": "POSTED"
};
const trusted={
  "issue_number": 10,
  "issue_url": "https://github.com/vixttha/Color-Team-OPS/issues/10",
  "comment_id": 6591670496,
  "actor_login": "vixttha",
  "created_at": "2026-11-03T00:02:21Z",
  "updated_at": "2026-11-03T00:02:21Z",
  "body": "message_id: IN-ORANGE-20261102-001\nsource_sha: 62d43ef51d362cf064c367158a8d7fce207abd68"
};
test("real shaped source message triages, never grants authority",()=>{const r=guardMessage(msg,trusted);assert.equal(r.triage,true);assert.equal(r.roleAuthenticated,false);assert.equal(r.authorityGranted,false);});
test("forged accepted rejected",()=>assert.equal(guardMessage({...msg,status:"ACCEPTED"},trusted).triage,false));
test("claimed wrong home rejected",()=>assert.equal(guardMessage({...msg,from_branch:homes.RED},trusted).triage,false));
test("wrong issue rejected",()=>assert.equal(guardMessage(msg,{...trusted,issue_number:9}).triage,false));
test("edited comment requires review",()=>assert.equal(guardMessage(msg,{...trusted,updated_at:"2026-11-03T01:00:00Z"}).triage,false));
test("duplicate id rejected",()=>assert.equal(guardMessage(msg,trusted,[{message_id:msg.message_id,comment_id:trusted.comment_id}]).triage,false));
test("missing provider metadata rejected",()=>assert.equal(guardMessage(msg,null).triage,false));
test("non-https evidence rejected",()=>assert.equal(guardMessage({...msg,evidence_links:["javascript:bad"]},trusted).triage,false));
test("draft work item allowed",()=>assert.equal(guardWorkItem({id:"BLU-W001",title:"Review",priority:"P1",status:"QUEUED",acceptance_criteria:["Verify"],evidence_status:"NOT_RUN"}).valid,true));
test("false ACCEPTED/NOT_RUN rejected",()=>assert.equal(guardWorkItem({id:"BLU-W001",title:"Review",priority:"P1",status:"ACCEPTED",acceptance_criteria:["Verify"],evidence_status:"NOT_RUN"}).valid,false));
test("invalid team/branch rejected",()=>assert.equal(guardState({schema_version:"prismcell-state-0.0.1",template:"PrismCell Workbench",version:"0.0.1",team:"GOLD",home_branch:"main",release_authorized:false,last_verified_product_sha:null}).valid,false));
test("release claim rejected",()=>assert.equal(guardState({schema_version:"prismcell-state-0.0.1",template:"PrismCell Workbench",version:"0.0.1",team:"BLUE",home_branch:homes.BLUE,release_authorized:true,last_verified_product_sha:null}).valid,false));
