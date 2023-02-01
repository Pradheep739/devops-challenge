# Windows Securit Group

resource "aws_security_group" "windows_SecurityGroup" {
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
  name        = local.windows_sg_name
  description = "Windows VPC security group"
  tags = merge(local.common_tags, map("Name", format(local.windows_sg_name)))

  ingress {      
      from_port   = "8081"
      to_port     = "8081"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "135"
      to_port     = "139"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "67"
      to_port     = "68"
      protocol    = "udp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "1434"
      to_port     = "1434"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "445"
      to_port     = "445"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "8444"
      to_port     = "8444"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "135"
      to_port     = "139"
      protocol    = "udp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "5983"
      to_port     = "5983"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "1433"
      to_port     = "1433"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "546"
      to_port     = "547"
      protocol    = "udp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "5355"
      to_port     = "5355"
      protocol    = "udp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "8082"
      to_port     = "8082"
      protocol    = "udp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "3389"
      to_port     = "3389"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
  ingress {
      
      from_port   = "443"
      to_port     = "443"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {      
      from_port   = "80"
      to_port     = "80"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    egress {      
      from_port   = "0"
      to_port     = "0"
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
}

# DNS Security group
resource "aws_security_group" "dns_SecurityGroup" {
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
  name        = local.dns_sg_name
  description = "Dns VPC security group"
  tags = merge(local.common_tags, map("Name", format(local.dns_sg_name)))

  ingress {      
      from_port   = "53"
      to_port     = "53"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
    ingress { 
      from_port   = "53"
      to_port     = "53"
      protocol    = "udp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    egress {      
      from_port   = "0"
      to_port     = "0"
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
}

# Linux Security Group
resource "aws_security_group" "linux_SecurityGroup" {
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
  name        =  local.linux_sg_name
  description =  "Linux VPC security group"
  tags = merge(local.common_tags, map("Name", format(local.linux_sg_name)))

  ingress {     
      from_port   = "5803"
      to_port     = "5803"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {
      from_port   = "22"
      to_port     = "22"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress { 
      from_port   = "443"
      to_port     = "443"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]      
    }
    ingress {
      from_port   = "80"
      to_port     = "80"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
    egress  {
      from_port   = "0"
      to_port     = "0"
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
}

# DB Security Group
resource "aws_security_group" "db_SecurityGroup" {
  name        = local.db_sg_name
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
  description = "Db VPC security group"
  tags = merge(local.common_tags, map("Name", format(local.db_sg_name)))

  ingress {
      from_port   = "1433"
      to_port     = "1433"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
    ingress {
      from_port   = "1521"
      to_port     = "1521"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
    ingress {
      from_port   = "3306"
      to_port     = "3306"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
    egress {
      from_port   = "0"
      to_port     = "0"
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
}

# Webserver Security Group
resource "aws_security_group" "webserver_SecurityGroup" {
  name        = local.webserver_sg_name
  count                = length(var.vpc_config)
  vpc_id          = aws_vpc.vpc[count.index].id
  description = "WebServer VPC security group"
  tags = merge(local.common_tags, map("Name", format(local.webserver_sg_name)))

  ingress {
      from_port   = "443"
      to_port     = "443"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
    ingress {
      from_port   = "80"
      to_port     = "80"
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
    egress {
      from_port   = "0"
      to_port     = "0"
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
}
