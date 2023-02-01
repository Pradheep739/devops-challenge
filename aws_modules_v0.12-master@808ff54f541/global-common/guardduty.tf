##################################
# guardduty enable and accept invitation
##################################

# US-WEST-2
#resource "aws_guardduty_detector" "member_usw2" {
  #count = upper(var.businessunit) != "PHC" ? 1 : 0
  #provider = aws.uswest2
  #enable = true
#}

#resource "aws_guardduty_invite_accepter" "member_usw2" {
  #count = upper(var.businessunit) != "PHC" ? 1 : 0
  #provider = aws.uswest2
  #detector_id       = join("", aws_guardduty_detector.member_usw2.*.id)
  #master_account_id = local.gd_master_account_id
#}


# US-EAST-1
#resource "aws_guardduty_detector" "member_use1" {
  #provider = aws.useast1
  #count = upper(var.businessunit) != "PHC" ? 1 : 0
  #enable = true
#}

#resource "aws_guardduty_invite_accepter" "member_use1" {
  #count = upper(var.businessunit) != "PHC" ? 1 : 0
  #provider = aws.useast1
  #detector_id       = join("", aws_guardduty_detector.member_use1.*.id)
  #master_account_id = local.gd_master_account_id
#}


# EU-CENTRAL-1
#resource "aws_guardduty_detector" "member_euc1" {
  #count = upper(var.businessunit) != "PHC" ? 1 : 0
  #provider = aws.eucentral1
  #enable = true
#}

#resource "aws_guardduty_invite_accepter" "member_euc1" {
  #count = upper(var.businessunit) != "PHC" ? 1 : 0
  #provider = aws.eucentral1
  #detector_id       = join("", aws_guardduty_detector.member_euc1.*.id)
  #master_account_id = local.gd_master_account_id
#}
