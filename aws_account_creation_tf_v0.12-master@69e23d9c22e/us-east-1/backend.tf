#######################
# Backend Configuration
#######################
terraform {
  backend "s3" {
    bucket         = ""
    key            = "us-east-1/resources.tfstate"
    region         = "us-west-2"
    encrypt        = "true"
    dynamodb_table = "terraform_locks"
  }
}
