############
# Variables
############

variable "aws_region" {}

variable "owner" {}
variable "environment" {}
variable "businessunit" {}
variable "costcenter" {}
variable "wbs" {}

variable "account_name" {
  default     = ""                                     
  description = "Enter the environment of the account."
}
variable "account_env" {
  default     = ""                                      
  description = "Enter the environment of the account."
}

variable "vpc_config" {}