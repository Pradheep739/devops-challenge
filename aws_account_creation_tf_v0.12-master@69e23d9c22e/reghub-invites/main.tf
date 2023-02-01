################################################################################
# Regional Hub Module

# Needs to be run after assuming the Reg Hub Terraform Admin Role.
# Creates Resource access share of TGW for all three primary regions.
# Sends out GuardDuty invite for the member accounts ( Bound to change - Commented out now)

# Same module can be re run for attaching the tgw route table association and propagration once
# new account is onbiarded .

# Note: Looks for the values of the variables in the reghub-config.json at root folder
################################################################################



module "reghub-tgw-share" {
  #source = "../../aws_modules_v0.12//regional_hub"
  source                       = "git::ssh://git@bitbucket.science.roche.com:7999/rsc-aws-tf/aws_modules_v0.12.git//regional_hub"
  member_account_id            = var.member_account_id
  member_account_root_email    = var.member_account_root_email
  member_account_business_unit = var.member_account_business_unit
  vpcs                         = var.vpcs
}