import {assessSignedComment} from '../src/security.mjs';
async function rawBody(req){
  const chunks=[];let size=0;
  for await(const ch of req){const b=Buffer.isBuffer(ch)?ch:Buffer.from(ch);size+=b.length;if(size>16384)throw Error('BODY_TOO_LARGE');chunks.push(b);}
  return Buffer.concat(chunks);
}
export default async function handler(req,res){
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='POST')return res.status(405).json({status:'METHOD_NOT_ALLOWED'});
  // No credential configured -> zero acceptance, no backend side effects.
  const secret=process.env.PRISMCELL_GITHUB_WEBHOOK_SECRET;
  const bindingsText=process.env.PRISMCELL_ROLE_BINDINGS;
  const configText=process.env.PRISMCELL_PROJECT_CONFIG;
  if(!secret||!bindingsText||!configText)return res.status(503).json({status:'LOCKED',reason:'AUTHENTICATED_PROVIDER_CONFIG_REQUIRED'});
  let raw;try{raw=await rawBody(req);}catch{return res.status(413).json({status:'REJECTED'});}
  let cfg,bindings;try{cfg=JSON.parse(configText);bindings=JSON.parse(bindingsText);}catch{return res.status(503).json({status:'LOCKED',reason:'SERVER_CONFIGURATION_INVALID'});}
  const result=assessSignedComment({raw,signature:req.headers['x-hub-signature-256'],secret,event:req.headers['x-github-event'],config:cfg,bindings,seen:[]});
  if(result.decision!=='REVIEW_ONLY')return res.status(403).json({status:'REJECTED',reason:result.reason});
  // Durable server-backed dedupe, authenticated Head lease and scoped credentials
  // MUST be deployed before a message may be ACKed or dispatched.
  return res.status(503).json({status:'LOCKED',reason:'DURABLE_CAS_AND_HEAD_EXECUTION_GATE_NOT_CONFIGURED'});
}
