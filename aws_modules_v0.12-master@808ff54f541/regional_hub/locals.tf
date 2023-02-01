locals {
  reghub_account_id = "077433217788"

  ram_name = {
    "us-west-2"    = "RAM-TGW-USW2-REGHUB-PRD-02"
    "us-east-1"    = "RAM-TGW-USE1-REGHUB-PRD-02"
    "eu-central-1" = "RAM-TGW-EUC1-REGHUB-PRD-02"
  }

  guardduty_masterDetector_id = {
    "us-west-2"    = "f0b88ebe76f773161de16819c4b64338"
    "us-east-1"    = "bab88cae3ef23bf8ac9f05a0bcf7215e"
    "eu-central-1" = "00b88ec47c6f69ff71ae20d0456b9c07"
  }

  tgw_route_table = {
    "us-west-2"    = "tgw-rtb-0ab613b5e70725803"
    "us-east-1"    = "tgw-rtb-0f571ef148672e3e2"
    "eu-central-1" = "tgw-rtb-081c5d281681da71a"
  }
  
  tgw_postinspection_routetable =  {
    "us-west-2"    = "tgw-rtb-003c2fd65d5356803"
    "us-east-1"    = "tgw-rtb-0bff021737637f0cc"
    "eu-central-1" = "tgw-rtb-02bab48614808c71a"
  }
}
