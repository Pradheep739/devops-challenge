################################################################################
# Pre-Requisites Module

# Terraform v0.12.24
# Creates the State file s3 bucket and policy
# Creates Dynamo db table for Locking
# Note: Looks for the values of the variables in the config.json at root folder
################################################################################

module "pre-req" {
  #source       = "../../aws_modules_v0.12//terraform-state"
  source       = "git::ssh://git@bitbucket.science.roche.com:7999/rsc-aws-tf/aws_modules_v0.12.git//terraform-state"
  bucket       = var.bucket
  owner        = var.owner
  environment  = var.environment
  businessunit = var.businessunit
  costcenter   = var.costcenter
  wbs          = var.wbs
}


