#######################
# Backend Configuration
#######################
terraform {
  backend "s3" {
    bucket         = ""
    key            = "us-west-2/resources.tfstate"
    region         = "us-west-2"
    encrypt        = "true"
    dynamodb_table = "terraform_locks"
  }
}
