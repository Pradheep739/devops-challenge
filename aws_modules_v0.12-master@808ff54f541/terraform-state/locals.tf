locals {
  common_tags = {
    "Environment"   = var.environment
    "Owner"         = var.owner
    "BusinessUnit"  = var.businessunit
    "CostCenter"    = var.costcenter
    "WBS"           = var.wbs
  }
}