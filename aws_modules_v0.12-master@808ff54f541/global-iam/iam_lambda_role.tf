# Assume role policy for Lambda role
data "aws_iam_policy_document" "policy" {
  statement {
    sid    = ""
    effect = "Allow"

    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = local.lambda_rolename
  description        = "Role for Lambda"
  assume_role_policy = data.aws_iam_policy_document.policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Policy for Lambda autotag 
resource "aws_iam_policy" "lambda_autotagpolicies" {
  name        = "POLICY-LAMBDA-AUTOTAG"
  description = "Policy for Lambda autotag"
  policy      = data.template_file.aws_lambda_autotag_policy.rendered
}

# autotag Policy Attachement
resource "aws_iam_role_policy_attachment" "lambda_autotag_policyattach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_autotagpolicies.arn
}

# Policy for Lambda accesskeyage
resource "aws_iam_policy" "lambda_accesskeyagepolicies" {
  name        = "POLICY-LAMBDA-ACCESSKEYAGE"
  description = "Policy for Lambda accesskeyage"
  policy      = data.template_file.aws_lambda_accesskeyage_policy.rendered
}

# Lambda Role Policy Attachement for accessage
resource "aws_iam_role_policy_attachment" "lambda_accesskeyage_policyattach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_accesskeyagepolicies.arn
}
# Policy for Lambda s3 encryption
resource "aws_iam_policy" "lambda_s3encryptionpolicies" {
  name        = "POLICY-S3-ENCRYPTION"
  description = "Policy for Lambda accesskeyage"
  policy      = data.template_file.aws_lambda_s3encryption_policy.rendered
}

# Lambda Role Policy Attachement for s3encryption
resource "aws_iam_role_policy_attachment" "lambda_s3encryption_policyattach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_s3encryptionpolicies.arn
}
