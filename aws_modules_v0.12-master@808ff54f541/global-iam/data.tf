
#### DATA SOURCES #####

# Get current account
data "aws_caller_identity" "current" {}

# Assume policy document for ADFS Roles
data "aws_iam_policy_document" "role-policy-document" {
  statement {
    actions = ["sts:AssumeRoleWithSAML"]
    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:saml-provider/ADFS"]
    }
    effect = "Allow"
    condition {
      test     = "StringEquals"
      variable = "SAML:aud"

      values = [
        "https://signin.aws.amazon.com/saml",
      ]
    }
  }
}

# Policy Documnet for Jenkins Custom policy
data "template_file" "aws_jenkins_policy" {
  template = file("${path.module}/policies/policy_jenkins.tpl")
}

# Policy Document for ADFS Power User Policy
data "template_file" "aws_pwusr_policy" {
  template = file("${path.module}/policies/policy_pwr_usr.tpl")

    vars = {
    account_id      = data.aws_caller_identity.current.account_id
  }
}

# Policy Document for ADFS Super Power User Policy
data "template_file" "aws_super_pwusr_policy" {
  template = file("${path.module}/policies/policy_super_pwusr.tpl")
}

# Policy Documnet for Lambda accesskeyage policy
data "template_file" "aws_lambda_accesskeyage_policy" {
  template = file("${path.module}/policies/policy_lambda_accesskeyage.tpl")
}

# Policy Documnet for Lambda autotag policy
data "template_file" "aws_lambda_autotag_policy" {
    template = file("${path.module}/policies/policy_lambda_autotag.tpl")
}
# Policy Documnet for Lambda s3 encryption policy
data "template_file" "aws_lambda_s3encryption_policy" {
    template = file("${path.module}/policies/policy_lambda_s3encryption.tpl")
}
