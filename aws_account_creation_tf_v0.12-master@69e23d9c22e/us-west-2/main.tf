################################################################################
# Regional Resources Module

# Creates infra and log buckets
# Creates KMS Keys with default policy ( Need to verify with Syam)
# Creates DLM Lifecycle policy for :
#         * All Instances with "Production" tag value for environment
#         * Daily backups
#         * Snapshots retained for 15 days
# Enables and configures AWS config and logs are sent to centralized buckets in Shared services for primary regions only.
# Creates Security Groups
#          * windows, dns , linux, db , webserver

# Creates SNS and required CW rules in three regions to trigger the S3 encforcer and Auto Tag Lambdas in Oregon.
# Creates Network resources
#          * Creates multiple VPCs w or w/o secondary cidr per region
#          * Creates subnets, route tables, s3 endpoinyt, dhcp optionset .
#          * Accepts resource share inviation sent from Reg hub and creates VPC attachment
# Guardduty invitation acceptance

# Note: Looks for the values of the variables in the config.json at root folder
################################################################################


module "vpc" {
  #source = "../../aws_modules_v0.12//regional"
  source       = "git::ssh://git@bitbucket.science.roche.com:7999/rsc-aws-tf/aws_modules_v0.12.git//regional"
  account_name = var.account_name
  account_env  = var.account_env
  owner        = var.owner
  environment  = var.environment
  businessunit = var.businessunit
  costcenter   = var.costcenter
  wbs          = var.wbs
  vpc_config   = var.vpc-us-west-2
  aws_region   = var.aws_region
}