locals{

  gd_master_account_id = "077433217788"

  region_code = {
    us-west-2    = "USW2"
    us-east-1    = "USE1"
    eu-central-1 = "EUC1"
  }


  config_bucket = {
    us-west-2    = "s3glousw2coresharedconfigprd001"
    us-east-1    = "s3glouse1coresharedconfigprd001"
    eu-central-1 = "s3gloeuc1coresharedconfigprd001"
  }
  
  common_tags = {
    "Environment"   = var.environment
    "Owner"         = var.owner
    "BusinessUnit"  = var.businessunit
    "CostCenter"    = var.costcenter
    "WBS"           = var.wbs
  }

  dg_ops_email     = "8k-roche-operations@8kmiles.com"
  cloudtrail_bucket = "s3glousw2coresharedcloudtrailprd001"
  ss_ctr_kms_key_arn = "arn:aws:kms:us-west-2:717063266043:key/9d34f7c5-3bbe-4f9f-88ec-d0741b273b95"

  cloudtrail_role_name = upper("ROLE-${var.account_name}-${var.account_env}-AWSCTR")
  cloudtrail_policy_name = upper("POLICY-${var.account_name}-${var.account_env}-AWSCTR")
  cloudtrail_name = upper("RSC-${var.account_name}-CLOUDTRIAL")
  cloudtrail-loggroup = upper("cloudtrail-${var.account_name}-loggroup")
  
  # AWS Config Role
  config_role_name = upper("ROLE-${var.account_name}-${var.account_env}-AWSCFG")
  config_policy_name = upper("POLICY-${var.account_name}-${var.account_env}-AWSCFG")

  notifyoperation_sns_name = upper("SNS-notify8kops-${var.account_name}-${var.account_env}-${local.region_code[var.aws_region]}-01")
  cw_accesskeyage_name  = upper("CW-IAMACCESSKEYAGE-${var.account_name}-${var.account_env}-${local.region_code[var.aws_region]}-01")

  sns_autotag_use1 = "arn:aws:sns:us-east-1:${data.aws_caller_identity.current.account_id}:SNS-AUTOTAG-${var.account_name}-${var.account_env}-USE1-01"
  sns_autotag_usw2 = "arn:aws:sns:us-west-2:${data.aws_caller_identity.current.account_id}:SNS-AUTOTAG-${var.account_name}-${var.account_env}-USW2-01"
  sns_autotag_euc1 = "arn:aws:sns:eu-central-1:${data.aws_caller_identity.current.account_id}:SNS-AUTOTAG-${var.account_name}-${var.account_env}-EUC1-01"

  sns_s3encryption_use1 = "arn:aws:sns:us-east-1:${data.aws_caller_identity.current.account_id}:SNS-S3ENCRYPTION-${var.account_name}-${var.account_env}-USE1-01"
  sns_s3encryption_usw2 = "arn:aws:sns:us-west-2:${data.aws_caller_identity.current.account_id}:SNS-S3ENCRYPTION-${var.account_name}-${var.account_env}-USW2-01"
  sns_s3encryption_euc1 = "arn:aws:sns:eu-central-1:${data.aws_caller_identity.current.account_id}:SNS-S3ENCRYPTION-${var.account_name}-${var.account_env}-EUC1-01"

  kms_key_name_use1  =   upper("KMS-USE1-${var.account_name}-${var.account_env}-01")
  kms_key_name_usw2  =   upper("KMS-USW2-${var.account_name}-${var.account_env}-01")
  kms_key_name_euc1  =   upper("KMS-EUC1-${var.account_name}-${var.account_env}-01")

  s3encryption_sns_name_use1     =  upper("SNS-s3encryption-${var.account_name}-${var.account_env}-USE1-01")
  cw_s3encryption_name_use1      =  upper("CW-s3encryption-${var.account_name}-${var.account_env}-USE1-01")

  s3encryption_sns_name_usw2     =  upper("SNS-s3encryption-${var.account_name}-${var.account_env}-USW2-01")
  cw_s3encryption_name_usw2      =  upper("CW-s3encryption-${var.account_name}-${var.account_env}-USW2-01")

  s3encryption_sns_name_euc1     =  upper("SNS-s3encryption-${var.account_name}-${var.account_env}-EUC1-01")
  cw_s3encryption_name_euc1      =  upper("CW-s3encryption-${var.account_name}-${var.account_env}-EUC1-01")

  autotag_sns_name_use1     =  upper("SNS-autotag-${var.account_name}-${var.account_env}-USE1-01")
  cw_ec2autotag_name_use1   =  upper("CW-EC2AUTOTAG-${var.account_name}-${var.account_env}-USE1-01")
  cw_autotag_name_use1      =  upper("CW-AUTOTAG-${var.account_name}-${var.account_env}-USE1-01")

  autotag_sns_name_usw2     =  upper("SNS-autotag-${var.account_name}-${var.account_env}-USW2-01")
  cw_ec2autotag_name_usw2   =  upper("CW-EC2AUTOTAG-${var.account_name}-${var.account_env}-USW2-01")
  cw_autotag_name_usw2      =  upper("CW-AUTOTAG-${var.account_name}-${var.account_env}-USW2-01")
  
  autotag_sns_name_euc1     =  upper("SNS-autotag-${var.account_name}-${var.account_env}-EUC1-01")
  cw_ec2autotag_name_euc1   =  upper("CW-EC2AUTOTAG-${var.account_name}-${var.account_env}-EUC1-01")
  cw_autotag_name_euc1      =  upper("CW-AUTOTAG-${var.account_name}-${var.account_env}-EUC1-01")
  
}
