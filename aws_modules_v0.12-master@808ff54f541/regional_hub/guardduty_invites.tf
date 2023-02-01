
##############################
# Guardduty invite meber 
##############################

# Send Guard duty invite to member account in US-WEST-2
resource "aws_guardduty_member" "member_invite_usw2" {
  provider           = aws.uswest2

  count = upper(var.member_account_business_unit) != "PHC" ? 1 : 0
  detector_id        = local.guardduty_masterDetector_id["us-west-2"]
  account_id         = var.member_account_id
  email              = var.member_account_root_email
  invite             = true
  invitation_message = "GuardDuty Invite - Please accept this invitation if you are expecting it."
}

# Send Guard duty invite to member account in US-EAST-1
resource "aws_guardduty_member" "member_invite_use1" {
  provider = aws.useast1
  count = upper(var.member_account_business_unit) != "PHC" ? 1 : 0
  detector_id        = local.guardduty_masterDetector_id["us-east-1"]
  account_id         = var.member_account_id
  email              = var.member_account_root_email
  invite             = true
  invitation_message = "GuardDuty Invite - Please accept this invitation if you are expecting it."
}

# Send Guard duty invite to member account in EU-CENTRAL-1
resource "aws_guardduty_member" "member_invite_euc1" {
  provider = aws.eucentral1
  count = upper(var.member_account_business_unit) != "PHC" ? 1 : 0
  detector_id        = local.guardduty_masterDetector_id["eu-central-1"]
  account_id         = var.member_account_id
  email              = var.member_account_root_email
  invite             = true
  invitation_message = "GuardDuty Invite - Please accept this invitation if you are expecting it."
}