#####################################
# Custom Main Route Table and Routes
#####################################

# Custom Route Table
resource "aws_route_table" "routetable" {
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
  tags   = merge(local.common_tags, map("Name", format("${local.routetable_name}-0%d", count.index+1)))
}

#Custom Route Table Subnet Association with Dynamically created Subnets
resource "aws_route_table_association" "private_subnet_routetableassociation" {
  count = length(local.vpc_subnets)
  subnet_id         =  aws_subnet.private_subnets[count.index].id
  route_table_id = local.vpc_subnets[count.index]["routetable_id"]
}