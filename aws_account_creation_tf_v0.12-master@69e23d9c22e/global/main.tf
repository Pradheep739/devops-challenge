################################################################################
# Global Module

# IAM Module
# Creates all the standard roles and policies required in the account
# Creates and configures budget as per the account owner threshold amount.
# Send out an email to the account owner when 90% of the budget threshold is reached.
# Configures IAM password Policy 

# Common Modules
# Cleans up default vpcs and related resources in all regions
# Creates multiregion cloudtrail and logs into centralized buctet in SharedServices (Oregon).
# Creates CW alarms and metrics which is triggered during following cases
#         * If root user uses the account
#         * If Multiple unauthorized actions or logins attempted
#         * If there is a Management Console sign-in without MFA
#         * If changes are made to IAM policies
#         * If changes are made to CloudTrail
#         * If customer created CMKs get disabled or scheduled for deletion
#         * If changes are made to an S3 Bucket
#         * If changes are made to AWS Config

# Creates a Lambda function that triggers an alert when access key age of the user is expiring
#         * age_limit = 180 / age_warning = 150
# Creates a Lambda function that enforces kms encryption on unencrypted buckets
# Creates a Lambda function that enforces required tags

# Note: Looks for the values of the variables in the config.json at root folder
################################################################################

module "iam" {
  #source = "../../aws_modules_v0.12//global-iam"
  source       = "git::ssh://git@bitbucket.science.roche.com:7999/rsc-aws-tf/aws_modules_v0.12.git//global-iam"
  account_name = var.account_name
  account_env  = var.account_env

  owner                              = var.owner
  environment                        = var.environment
  businessunit                       = var.businessunit
  costcenter                         = var.costcenter
  wbs                                = var.wbs
  billing_limit_amount               = var.billing_limit_amount
  billing_subscriber_email_addresses = var.billing_subscriber_email_addresses
  billing_start_time                 = var.billing_start_time

  # Pre-set Value
  aws_region = "us-east-1"
}

module "common" {
  #source       = "../../aws_modules_v0.12//global-common"
  source       = "git::ssh://git@bitbucket.science.roche.com:7999/rsc-aws-tf/aws_modules_v0.12.git//global-common"
  account_name = var.account_name
  account_env  = var.account_env

  owner        = var.owner
  environment  = var.environment
  businessunit = var.businessunit
  costcenter   = var.costcenter
  wbs          = var.wbs
  lambda_role  = module.iam.lambda_role

  # Pre-set Value
  aws_region = "us-west-2"
}
