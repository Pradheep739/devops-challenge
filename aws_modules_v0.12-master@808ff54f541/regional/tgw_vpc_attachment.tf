# ######################
# # TGW VPC Attachment
# ######################

resource "null_resource" "create-subscription" {
  provisioner "local-exec" {
    
    command = <<EOT
      invitationarn=($(aws ram get-resource-share-invitations --query "resourceShareInvitations[?status=='PENDING'].resourceShareInvitationArn" --region "${var.aws_region}" --output text))

      if test -n "$invitationarn"; then
        aws ram accept-resource-share-invitation --resource-share-invitation-arn $invitationarn --region "${var.aws_region}"
      fi
      
  EOT
  }
}

data "aws_subnet_ids" "subnets" {
  depends_on = [aws_vpc.vpc, aws_subnet.private_subnets]
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
}


#Attach the vpc to the transit gateway
resource "aws_ec2_transit_gateway_vpc_attachment" "private_subnet_tgw_attach" {
  depends_on = [aws_vpc.vpc, aws_subnet.private_subnets]
  count                = length(var.vpc_config)
  subnet_ids         = data.aws_subnet_ids.subnets[count.index].ids
  vpc_id          = aws_vpc.vpc[count.index].id
  transit_gateway_id = local.tgw_id[var.aws_region]
}

# Adding route for tgw to route table
resource "aws_route" "tgw_route" {
  depends_on = [aws_ec2_transit_gateway_vpc_attachment.private_subnet_tgw_attach]
  count                = length(var.vpc_config)
  route_table_id = aws_route_table.routetable[count.index].id
  destination_cidr_block = "0.0.0.0/0"
  transit_gateway_id = local.tgw_id[var.aws_region]
}
