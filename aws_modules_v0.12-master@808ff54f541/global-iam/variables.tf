
#### VARIABLES #####

variable "aws_region" {}
variable "account_id" {
  default     = ""
  description = "Enter the environment of the account."
}
variable "account_name" {
  default     = ""
  description = "Enter the environment of the account."
}
variable "account_env" {
  default     = ""
  description = "Enter the environment of the account."
}
variable "billing_limit_amount"{
  description = "Budget limit amount"
}
variable "billing_subscriber_email_addresses" {
  description = "Email address to send budget alerts to"
}
variable "billing_start_time"{
  description = "Start time for calculating the bill"
}
variable "owner" {}
variable "environment" {}
variable "businessunit" {}
variable "costcenter" {}
variable "wbs" {}