# ##########
# Subnets
# ##########

resource "aws_subnet" "private_subnets" {
  count = length(local.vpc_subnets)
  vpc_id = local.vpc_subnets[count.index]["vpc_id"]
  cidr_block = local.vpc_subnets[count.index]["subnet_cidr"]
  availability_zone = local.vpc_subnets[count.index]["subnet_az"]
  tags              =  merge(local.common_tags, map("Name", format("${local.subnet_name}0%s", local.vpc_subnets[count.index]["subnet_key"]+1)))
}
