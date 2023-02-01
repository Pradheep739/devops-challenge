#######################
# Networking Resources
#######################

# VPC Resource
resource "aws_vpc" "vpc" {
  count                = length(var.vpc_config)
  cidr_block           = var.vpc_config[count.index]["vpc_cidr"]
  instance_tenancy     = "default"
  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_classiclink   = false
  enable_classiclink_dns_support   = false
  assign_generated_ipv6_cidr_block  = false
  tags                 = merge(local.common_tags, map("Name", format("${local.vpc_name}-0%d", count.index+1)))    
}

data "aws_vpc" "selected" {
  depends_on = [aws_vpc.vpc]
  count           = length(local.vpc_secondary_cidr)
  cidr_block            = local.vpc_secondary_cidr[count.index]["vpc_cidr"]
}

# VPC Secondary CIDR
resource "aws_vpc_ipv4_cidr_block_association" "this" {
  count           = length(local.vpc_secondary_cidr)
  vpc_id          = data.aws_vpc.selected[count.index].id
  cidr_block      = local.vpc_secondary_cidr[count.index]["secondary_cidr_blocks"]
}

# VPC FlowLogs
resource "aws_flow_log" "vpc_flowlog" {
  count                = length(var.vpc_config)
  log_destination_type = "cloud-watch-logs"
  log_destination = aws_cloudwatch_log_group.vpc_flowlog_loggroup[count.index].arn
  iam_role_arn    =  data.aws_iam_role.flowlog_role.arn
  vpc_id          = aws_vpc.vpc[count.index].id
  traffic_type    = "ALL"
}
# VPC Flowlog Cloudwatch Log group
resource "aws_cloudwatch_log_group" "vpc_flowlog_loggroup" {
  count                = length(var.vpc_config)
  name = format("${local.flowlog-loggroup}-0%d", count.index+1)
}

# VPC S3 Endpoint
resource "aws_vpc_endpoint" "s3" {
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
  service_name = data.aws_vpc_endpoint_service.s3.service_name
  tags                 = merge(local.common_tags, map("Name", format("${local.vpc_s3_endpoint}-0%d", count.index+1))) 
}

data "aws_vpc_endpoint_service" "s3" {
  service = "s3"
  service_type = "Gateway"
}

# VPC S3 Endpoint Route Table Association
resource "aws_vpc_endpoint_route_table_association" "private_s3" {
  count                = length(var.vpc_config)
  vpc_endpoint_id = aws_vpc_endpoint.s3[count.index].id
  route_table_id  = aws_route_table.routetable[count.index].id
}