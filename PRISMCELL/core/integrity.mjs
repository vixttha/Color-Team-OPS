/* Optional cloud Node adapter for evidence snapshots; digest detects change, not authorship.
   Host must fetch the raw provider data itself. Never treat self-declared receipts as proof. */
import {createHash} from 'node:crypto';
export function digestReceipt(receipt) {
  if(!receipt || typeof receipt.body!=='string' || typeof receipt.actor_login!=='string' || !Number.isSafeInteger(receipt.comment_id) || typeof receipt.updated_at!=='string')throw new TypeError('Invalid receipt');
  const snapshot=JSON.stringify([receipt.provider,receipt.issue_url,receipt.comment_url,receipt.comment_id,receipt.actor_login,receipt.created_at,receipt.updated_at,receipt.body]);
  return 'sha256:'+createHash('sha256').update(snapshot,'utf8').digest('hex');
}
export function verifyReceiptSnapshot(stored,observed) {
  if(!stored || typeof stored.digest!=='string' || typeof stored.comment_url!=='string' || !observed || stored.comment_url!==observed.comment_url)return {matches:false,reason:'MISSING_OR_WRONG_RECEIPT'};
  try {return digestReceipt(observed)===stored.digest?{matches:true,reason:'SAME_PROVIDER_READBACK_SNAPSHOT'}:{matches:false,reason:'PROVIDER_RECEIPT_CHANGED'};}
  catch {return {matches:false,reason:'INVALID_PROVIDER_RECEIPT'};}
}
