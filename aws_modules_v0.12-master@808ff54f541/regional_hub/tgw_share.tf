#################################
# Send Transitgateway resourrce share from Regional hub
#################################

# us-west-2
# Get the RegHub existing Resource Access Share
data "aws_ram_resource_share" "tgwramusw2" {
  provider       = aws.uswest2
  name           = local.ram_name["us-west-2"]
  resource_owner = "SELF"
}

# Update the RegHub RAM Principle with the New Account ID to send an Invitation
resource "aws_ram_principal_association" "update_ram_principleusw2" {
  provider           = aws.uswest2
  principal          = var.member_account_id
  resource_share_arn = data.aws_ram_resource_share.tgwramusw2.arn
}

#us-east-1
# Get the RegHub existing Resource Access Share
data "aws_ram_resource_share" "tgwramuse1" {
  provider       = aws.useast1
  name           = local.ram_name["us-east-1"]
  resource_owner = "SELF"
}

# Update the RegHub RAM Principle with the New Account ID to send an Invitation
resource "aws_ram_principal_association" "update_ram_principleuse1" {
  provider           = aws.useast1
  principal          = var.member_account_id
  resource_share_arn = data.aws_ram_resource_share.tgwramuse1.arn
}

# eu-central-1
# Get the RegHub existing Resource Access Share
data "aws_ram_resource_share" "tgwrameuc1" {
  provider       = aws.eucentral1
  name           = local.ram_name["eu-central-1"]
  resource_owner = "SELF"
}

# Update the RegHub RAM Principle with the New Account ID to send an Invitation
resource "aws_ram_principal_association" "update_ram_principleeuc1" {
  provider           = aws.eucentral1
  principal          = var.member_account_id
  resource_share_arn = data.aws_ram_resource_share.tgwrameuc1.arn
}
