locals{
  #gd_master_account_id = "077433217788"
  
  region_code = {
    us-west-2    = "USW2"
    us-east-1    = "USE1"
    eu-central-1 = "EUC1"
  }

  common_tags = {
    "Environment"   = var.environment
    "Owner"         = var.owner
    "BusinessUnit"  = var.businessunit
    "CostCenter"    = var.costcenter
    "WBS"           = var.wbs
  }

  kms_key_name  =   upper("KMS-${local.region_code[var.aws_region]}-${var.account_name}-${var.account_env}-01")
  config_role_name = upper("ROLE-${var.account_name}-${var.account_env}-AWSCFG")
  dlm_lifecycle_role_name = upper("ROLE-${var.account_name}-${var.account_env}-DLM-LIFECYCLE")
  infra_bucketname = lower(replace("s3${local.region_code[var.aws_region]}app${var.account_name}infra${var.account_env}001","-",""))
  log_bucketname = lower(replace("s3${local.region_code[var.aws_region]}app${var.account_name}logs${var.account_env}001","-",""))

  # Network Parameters

  vpc_subnets = flatten([
    for vpc_key, vpc in var.vpc_config : [
      for subnet_key, subnet in vpc.subnets : {
        vpc_key = vpc_key
        vpc_cidr = vpc.vpc_cidr
        secondary_cidr = vpc.secondary_cidr_blocks  
        subnet_key = subnet_key
        subnet_cidr = subnet.cidr_block
        vpc_id  = aws_vpc.vpc[vpc_key].id
        routetable_id  = aws_route_table.routetable[vpc_key].id
        subnet_az  = subnet.az
      }
     ]
  ])


  dhcp = {
    "us-west-2" = {
      dhcp_options_domain_name          = "aws.science.roche.com"
      dhcp_options_domain_name_servers  = ["10.158.10.113", "10.152.5.113"]
      dhcp_options_ntp_servers          = ["169.254.169.123"]
      dhcp_options_netbios_name_servers = ["10.158.10.113", "10.152.5.113"]
      dhcp_options_netbios_node_type    = "8"
    },
    "eu-central-1" = {
      dhcp_options_domain_name          = "aws.science.roche.com"
      dhcp_options_domain_name_servers  = ["10.158.10.113", "10.152.5.113"]
      dhcp_options_ntp_servers          = ["169.254.169.123"]
      dhcp_options_netbios_name_servers = ["10.158.10.113", "10.152.5.113"]
      dhcp_options_netbios_node_type    = "8"
    },
    "us-east-1" = {
      dhcp_options_domain_name          = "aws.science.roche.com"
      dhcp_options_domain_name_servers  = ["10.158.10.113", "10.152.5.113"]
      dhcp_options_ntp_servers          = ["169.254.169.123"]
      dhcp_options_netbios_name_servers = ["10.158.10.113", "10.152.5.113"]
      dhcp_options_netbios_node_type    = "8"
    }
  }

  tgw_id = {
    "us-west-2" = "tgw-08ac6c4ea44676be6"
    "eu-central-1" = "tgw-0cacc4d4bea21e576"
    "us-east-1" = "tgw-073edf7d31ad83111"
  }

  vpc_secondary_cidr = [
    for vpc_key, secondary_vpc in var.vpc_config:
      secondary_vpc if (secondary_vpc["secondary_cidr_blocks"] != "") 
  ]
  
  vpc_name          = upper("VPC-${local.region_code[var.aws_region]}-${var.account_name}-${var.account_env}")
  vpc_s3_endpoint   = upper("VPC-${local.region_code[var.aws_region]}-${var.account_name}-${var.account_env}-S3-ENDPOINT")
  routetable_name   = upper("RT-${local.region_code[var.aws_region]}-${var.account_name}-${var.account_env}")
  subnet_name       = upper("SUB-PRV-${local.region_code[var.aws_region]}-AZ")
  flowlog_role_name = upper("ROLE-${var.account_name}-${var.account_env}-AWSFLOWRW")
  flowlog-loggroup  = upper("flowlog-${var.account_name}-loggroup")
  windows_sg_name   = upper("SG-${local.region_code[var.aws_region]}-WIN-${var.account_env}")
  db_sg_name        = upper("SG-${local.region_code[var.aws_region]}-DB-${var.account_env}")
  webserver_sg_name = upper("SG-${local.region_code[var.aws_region]}-WEB-${var.account_env}")
  linux_sg_name     = upper("SG-${local.region_code[var.aws_region]}-LIN-${var.account_env}")
  dns_sg_name       = upper("SG-${local.region_code[var.aws_region]}-DNS-${var.account_env}")
}
