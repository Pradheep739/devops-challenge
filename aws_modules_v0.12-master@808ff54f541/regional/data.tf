##############
# Datasources
##############

data "aws_caller_identity" "current" {}

# KMS Key Policy
data "template_file" "kms_policy" {
  #template = file("../../aws_modules_tf12/kmskey/policies/kms-key-policy.json.tpl")
  template = file("${path.module}/policies/kms-key-policy.tpl")
  vars = {
    account_id = data.aws_caller_identity.current.account_id
  }
}

# S3 Infra Bucket Policy
data "template_file" "s3_infra_bucketpolicy" {
  template = file("${path.module}/policies/s3_infra_bucketpolicy.tpl")

  vars = {
    account_id      = data.aws_caller_identity.current.account_id
    bucket_name     = local.infra_bucketname
  }
}

# S3 Logs Bucket Poicy
data "template_file" "s3_log_bucketpolicy" {
  template = file("${path.module}/policies/s3_log_bucketpolicy.tpl")

  vars = {
    account_id  = data.aws_caller_identity.current.account_id
    bucket_name = local.log_bucketname
  }
}

# data "aws_iam_role" "config_role" {
#   name = local.config_role_name
# }

data "aws_iam_role" "dlm_lifecycle_role" {
  name = local.dlm_lifecycle_role_name
}

data "aws_iam_role" "flowlog_role" {
  name = local.flowlog_role_name
}

data "aws_kms_key" "kms_key_arn" {
  key_id = "alias/${local.kms_key_name}"
}