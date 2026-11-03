export default function handler(req,res){
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='GET')return res.status(405).json({status:'METHOD_NOT_ALLOWED'});
  return res.status(200).json({service:'PrismCell Cloud Gate',status:'STAGING_LOCKED',write_enabled:false,autonomous_execution:false,independent_identity_certified:false});
}
