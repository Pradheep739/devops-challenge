#######################
# Backend Configuration
#######################
terraform {
  backend "s3" {
    bucket         = ""
    key            = "global/global.tfstate"
    region         = "us-west-2"
    encrypt        = "true"
    dynamodb_table = "terraform_locks"
  }
}
