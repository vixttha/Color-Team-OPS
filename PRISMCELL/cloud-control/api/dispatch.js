export default function handler(req,res){
  res.setHeader('Cache-Control','no-store');
  return res.status(403).json({status:'EXECUTION_DISABLED',reason:'NO_VERIFIED_HEAD_AUTHORIZATION_OR_SCOPED_RUNTIME_CREDENTIALS'});
}
