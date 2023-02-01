##############
# Providers
#############
provider "aws" {
  region = var.aws_region
}
# Provider for us-west-2 region
provider "aws" {
  region = "us-west-2"
  alias  = "uswest2"
}
# Provider for us-west-2 region
provider "aws" {
  region = "us-east-1"
  alias  = "useast1"
}
# Provider for us-west-2 region
provider "aws" {
  region = "eu-central-1"
  alias  = "eucentral1"
}