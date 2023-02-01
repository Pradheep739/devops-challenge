#### LOCALS ####

locals {

  shared_services_account = "717063266043"

  common_tags = {
    "Environment"   = var.environment
    "Owner"         = var.owner
    "BusinessUnit"  = var.businessunit
    "CostCenter"    = var.costcenter
    "WBS"           = var.wbs
  }
  
  # jenkins_assume_role  = "arn:aws:iam::${var.account_id}:role/Role-Jenkins"
  admin_rolename           = upper("ROLE-${var.account_name}-${var.account_env}-AWSADM")
  ss_rolename              = upper("ROLE-${var.account_name}-${var.account_env}-SS-CROSSACCOUNT")
  pwrusr_rolename          = upper("ROLE-${var.account_name}-${var.account_env}-AWSPWUSR")
  pwusr_policyname         = upper("POLICY-${var.account_name}-${var.account_env}-AWSPWUSR")
  pwusr_policyname01       = upper("POLICY-${var.account_name}-${var.account_env}-AWSPWUSR-01")
  suppwusr_rolename        = upper("ROLE-${var.account_name}-${var.account_env}-AWSSUPPWUSR")
  suppwusr_policyname      = upper("POLICY-${var.account_name}-${var.account_env}-AWSSUPPWUSR")
  read_rolename            = upper("ROLE-${var.account_name}-${var.account_env}-AWSUSR")
  principals               = "arn:aws:iam::${var.account_id}:saml-provider/ADFS"
  dlm_lifecycle_role       = upper("ROLE-${var.account_name}-${var.account_env}-DLM-LIFECYCLE")
  dlm_lifecycle_policyname = upper("POLICY-${var.account_name}-${var.account_env}-DLM-LIFECYCLE")

  budget_name =  upper("Budget-${var.account_name}-${var.account_env}")
  

  # VPC FLowLog Role
  vpcflowlog_rolename   = upper("ROLE-${var.account_name}-${var.account_env}-AWSFLOWRW")
  vpcflowlog_policyname = upper("POLICY-${var.account_name}-${var.account_env}-AWSFLOWRW")

  # AWS Lambda Role
  lambda_accesskeyage_role_name = upper("ROLE-${var.account_name}-${var.account_env}-accesskeyage-AWSLAMBDA")
  lambda_autotag_role_name      = upper("ROLE-${var.account_name}-${var.account_env}-autotag-AWSLAMBDA")
  lambda_rolename               = upper("ROLE-${var.account_name}-${var.account_env}-AWSLAMBDA")
}

