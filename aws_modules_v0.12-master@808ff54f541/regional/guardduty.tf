# ##################################
# # guardduty enable and accept invitation
# ##################################

# resource "aws_guardduty_detector" "member" {
#   #finding_publishing_frequency = "FIFTEEN_MINUTES"
#   enable = true
# }

# resource "aws_guardduty_invite_accepter" "member" {
#   detector_id       = aws_guardduty_detector.member.id
#   master_account_id = local.gd_master_account_id
# }
