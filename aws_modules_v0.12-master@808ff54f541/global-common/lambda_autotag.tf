#################
# autotag lambda
#################

data "archive_file" "zipautotag" {
  type        = "zip"
  source_dir = "${path.module}/AutoTag"
  output_path = "${path.module}/AutoTag.zip"
}

resource "aws_lambda_function" "lambda_autotag" {
  function_name = "Tag-EnforceResourceTagging"

  filename         = data.archive_file.zipautotag.output_path
  source_code_hash = data.archive_file.zipautotag.output_base64sha256

  role = var.lambda_role
  handler = "lambda_function.lambda_handler"
  runtime = "python3.7"
  timeout = "900"
  tags = local.common_tags
  environment {
    variables = {
      Owner = local.common_tags["Owner"]
      BusinessUnit = local.common_tags["BusinessUnit"]
      CostCenter = local.common_tags["CostCenter"]
      Environment = local.common_tags["Environment"]
      WBS = local.common_tags["WBS"]
    }
  }
}

# Lambda permission to allow external sources invoking the Lambda function e.g. SNS
resource "aws_lambda_permission" "lambda_permission_autotag_use1" {
  statement_id  = "AllowExecutionFromSNSUSE1"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_autotag.function_name
  principal     = "sns.amazonaws.com"
  
  source_arn = local.sns_autotag_use1
}

resource "aws_lambda_permission" "lambda_permission_autotag_usw2" {
  statement_id  = "AllowExecutionFromSNSUSW2"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_autotag.function_name
  principal     = "sns.amazonaws.com"
  
  source_arn = local.sns_autotag_usw2
}

resource "aws_lambda_permission" "lambda_permission_autotag_euc1" {
  statement_id  = "AllowExecutionFromSNSEUC1"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_autotag.function_name
  principal     = "sns.amazonaws.com"
  
  source_arn = local.sns_autotag_euc1
}
