
##########################
# S3 StateFile Bucket
##########################
resource "aws_s3_bucket" "terraform_state" {
  bucket = var.bucket
  # Enable versioning so we can see the full revision history of our
  # state files
  versioning {
    enabled = true
  }
  # Enable server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
  policy      = data.template_file.aws_statefile_bucket_policy.rendered
  tags = local.common_tags
}

####################################
#     S3 StateFile Bucket Policy
####################################
data "aws_caller_identity" "current" {}

data "template_file" "aws_statefile_bucket_policy" {
  template = file("${path.module}/policies/s3_statefile_policy.tpl")

  vars = {
    account_id           = data.aws_caller_identity.current.account_id
    terraform_admin      = split("/", data.aws_caller_identity.current.arn)[1]
    statefile_bucketname = var.bucket
  }
}

####################################
# Dynamo Db Lock
####################################
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform_locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
  tags = local.common_tags
}
