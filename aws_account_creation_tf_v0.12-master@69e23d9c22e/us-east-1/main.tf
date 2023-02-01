module "vpc" {
  #source       = "../../aws_modules_tf_v0.12//regional"
  source       = "git::ssh://git@bitbucket.science.roche.com:7999/rsc-aws-tf/aws_modules_v0.12.git//regional"
  account_name = var.account_name
  account_env  = var.account_env
  owner        = var.owner
  environment  = var.environment
  businessunit = var.businessunit
  costcenter   = var.costcenter
  wbs          = var.wbs
  vpc_config   = var.vpc-us-east-1
  aws_region   = var.aws_region
}