
#######
# DHCP 
#######

# DHCP Options Set
resource "aws_vpc_dhcp_options" "dhcp" {
  domain_name          = local.dhcp[var.aws_region]["dhcp_options_domain_name"]
  domain_name_servers  = local.dhcp[var.aws_region]["dhcp_options_domain_name_servers"]
  ntp_servers          = local.dhcp[var.aws_region]["dhcp_options_ntp_servers"]
  netbios_name_servers = local.dhcp[var.aws_region]["dhcp_options_netbios_name_servers"]
  netbios_node_type    = local.dhcp[var.aws_region]["dhcp_options_netbios_node_type"]

  tags = merge(local.common_tags, map("Name", format("DHCP-%s", local.vpc_name)))

}

# DHCP Options Set Association
resource "aws_vpc_dhcp_options_association" "dhcpassociation" {
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
  dhcp_options_id = join(",", aws_vpc_dhcp_options.dhcp.*.id)
}
