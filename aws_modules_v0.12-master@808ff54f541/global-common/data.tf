

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "kms_policy" {
  statement {
    sid = "kms_key_policy"
    actions = ["kms:*"]
    resources = ["*"]
    principals {
      type = "AWS"
      identifiers = [data.aws_caller_identity.current.account_id]
    }
  }
}

# Policy document for config role
data "template_file" "aws_config_policy" {
  template = "${file("${path.module}/policies/policy_awsconfig.tpl")}"

  vars = {
    account_id = data.aws_caller_identity.current.account_id
  }

}