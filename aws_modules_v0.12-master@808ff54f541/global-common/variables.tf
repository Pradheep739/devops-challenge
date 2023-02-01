#### VARIABLES #####

variable "aws_region" {}

variable "account_name" {
  default     = ""
  description = "Enter the environment of the account."
}
variable "account_env" {
  default     = ""
}
variable "owner" {}
variable "environment" {}
variable "businessunit" {}
variable "costcenter" {}
variable "wbs" {}
variable "lambda_role" {}
