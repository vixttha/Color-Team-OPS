// Deterministic one-worker fencing model. Caller must commit using a real atomic provider CAS.
export function acquire(state,req){
  const deny=(reason)=>({ok:false,reason,state});
  if(!state||!Number.isSafeInteger(state.revision)||state.revision<0||!Number.isSafeInteger(state.fence)||state.fence<0)return deny('INVALID_STATE');
  if(!req||req.expectedRevision!==state.revision)return deny('STALE_CONCURRENT_WRITE');
  if(state.activeWorker!==null)return deny('WORKER_ALREADY_ACTIVE');
  if(req.headVerified!==true||req.ownerApproved!==true||!req.team||!req.workItemId)return deny('MISSING_TRUSTED_HEAD_DECISION');
  const next={...state,revision:state.revision+1,fence:state.fence+1,activeWorker:{team:req.team,workItemId:req.workItemId,fence:state.fence+1}};
  return {ok:true,state:next,lease:next.activeWorker,providerCasRequired:true};
}
export function release(state,req){
  const deny=(reason)=>({ok:false,reason,state});
  if(!state?.activeWorker||!req||req.expectedRevision!==state.revision)return deny('NO_ACTIVE_OR_STALE');
  if(req.fence!==state.activeWorker.fence||req.team!==state.activeWorker.team)return deny('FENCE_OR_TEAM_MISMATCH');
  return {ok:true,state:{...state,revision:state.revision+1,activeWorker:null},providerCasRequired:true};
}
