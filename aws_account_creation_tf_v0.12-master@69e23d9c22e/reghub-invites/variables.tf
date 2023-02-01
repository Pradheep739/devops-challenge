###########
# Variables
###########

variable "member_account_id" {
  description = "Provide the new account id"
}
variable "member_account_root_email" {
  description = "Provide the new account root email id"
}
variable "member_account_business_unit" {
  description = "Provide the new account business unit"
}
variable "vpcs" {
  description = "Update the json object with list of vpcs in each region"
}

