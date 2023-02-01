


data "aws_ec2_transit_gateway_vpc_attachment" "tgw_attach_use1" {
  count = length(var.vpcs["us-east-1"]) > 0 ? length(var.vpcs["us-east-1"]) : 0
  provider  = aws.useast1
  filter {
    name   = "vpc-id"
    values = [var.vpcs["us-east-1"][count.index]]
  }
}

resource "aws_ec2_transit_gateway_route_table_association" "reg_rt_association_use1" {
  count = length(var.vpcs["us-east-1"]) > 0 ? length(var.vpcs["us-east-1"]) : 0
  provider  = aws.useast1
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_use1[count.index].id
  transit_gateway_route_table_id = local.tgw_route_table["us-east-1"]
}

resource "aws_ec2_transit_gateway_route_table_propagation" "reg_rt_propagation_use1" {
  count = length(var.vpcs["us-east-1"]) > 0 ? length(var.vpcs["us-east-1"]) : 0
  provider  = aws.useast1
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_use1[count.index].id
  transit_gateway_route_table_id = local.tgw_route_table["us-east-1"]
}
resource "aws_ec2_transit_gateway_route_table_propagation" "reg_post_inspection_rt_propagation_use1" {
  count = length(var.vpcs["us-east-1"]) > 0 ? length(var.vpcs["us-east-1"]) : 0
  provider  = aws.useast1
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_use1[count.index].id
  transit_gateway_route_table_id = local.tgw_postinspection_routetable["us-east-1"]
}


# ##### us-west-2 ####

data "aws_ec2_transit_gateway_vpc_attachment" "tgw_attach_usw2" {
  count = length(var.vpcs["us-west-2"]) > 0 ? length(var.vpcs["us-west-2"]) : 0
  provider  = aws.uswest2
  filter {
    name   = "vpc-id"
    values = [var.vpcs["us-west-2"][count.index]]
  }
}

output "aws_ec2_transit_gateway_vpc_attachment_id" {
  value = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_usw2.*.id
}

resource "aws_ec2_transit_gateway_route_table_association" "reg_rt_association_usw2" {
  count = length(var.vpcs["us-west-2"]) > 0 ? length(var.vpcs["us-west-2"]) : 0
  provider  = aws.uswest2
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_usw2[count.index].id
  transit_gateway_route_table_id = local.tgw_route_table["us-west-2"]
}

resource "aws_ec2_transit_gateway_route_table_propagation" "reg_rt_propagation_usw2" {
  count = length(var.vpcs["us-west-2"]) > 0 ? length(var.vpcs["us-west-2"]) : 0
  provider  = aws.uswest2
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_usw2[count.index].id
  transit_gateway_route_table_id = local.tgw_route_table["us-west-2"]
}

resource "aws_ec2_transit_gateway_route_table_propagation" "reg_post_inspection_rt_propagation_usw2" {
  count = length(var.vpcs["us-west-2"]) > 0 ? length(var.vpcs["us-west-2"]) : 0
  provider  = aws.uswest2
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_usw2[count.index].id
  transit_gateway_route_table_id = local.tgw_postinspection_routetable["us-west-2"]
}



#### Eu-central-1 ####
data "aws_ec2_transit_gateway_vpc_attachment" "tgw_attach_euc1" {
  count = length(var.vpcs["eu-central-1"]) > 0 ? length(var.vpcs["eu-central-1"]) : 0
  provider  = aws.eucentral1
  filter {
    name   = "vpc-id"
    values = [var.vpcs["eu-central-1"][count.index]]
  }
}

resource "aws_ec2_transit_gateway_route_table_association" "reg_rt_association_euc1" {
  count = length(var.vpcs["eu-central-1"]) > 0 ? length(var.vpcs["eu-central-1"]) : 0
  provider  = aws.eucentral1
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_euc1[count.index].id
  transit_gateway_route_table_id = local.tgw_route_table["eu-central-1"]
}

resource "aws_ec2_transit_gateway_route_table_propagation" "reg_rt_propagation_euc1" {
  count = length(var.vpcs["eu-central-1"]) > 0 ? length(var.vpcs["eu-central-1"]) : 0
  provider  = aws.eucentral1
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_euc1[count.index].id
  transit_gateway_route_table_id = local.tgw_route_table["eu-central-1"]
}
resource "aws_ec2_transit_gateway_route_table_propagation" "reg_post_inspection_rt_propagation_euc1" {
  count = length(var.vpcs["eu-central-1"]) > 0 ? length(var.vpcs["eu-central-1"]) : 0
  provider  = aws.eucentral1
  transit_gateway_attachment_id  = data.aws_ec2_transit_gateway_vpc_attachment.tgw_attach_euc1[count.index].id
  transit_gateway_route_table_id = local.tgw_postinspection_routetable["eu-central-1"]
}
