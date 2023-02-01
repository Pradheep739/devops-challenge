############
# Variables
############

variable "bucket" {
  description = "Provide the state file bucket name"
}
variable "owner" {
  description = "Provide value of the Owner tag"
}
variable "environment" {
  description = "Provide value of the Environment tag"
}
variable "costcenter" {
  description = "Provide value of the CostCenter tag"
}
variable "businessunit" {
  description = "Provide value of the Business Unit tag"
}
variable "wbs" {
  description = "Provide value of the WBS tag"
}