###########################
# Deploy Lambda to enforce s3 encryption
###########################

# Create achive of lambda code
data "archive_file" "s3encrptionzip" {
  type        = "zip"
  source_file = "${path.module}/ensure_s3encryption.py"
  output_path = "${path.module}/ensure_s3encryption.zip"
}

# Deploy the Lambda code
resource "aws_lambda_function" "lambda_s3encryption" {
  function_name = "S3-EnforceEncryption"

  filename         = data.archive_file.s3encrptionzip.output_path
  source_code_hash = data.archive_file.s3encrptionzip.output_base64sha256
  timeout = "900"
  role = var.lambda_role
  handler = "ensure_s3encryption.lambda_handler"
  runtime = "python3.7"
  tags    = local.common_tags
  
  }

resource "aws_lambda_permission" "lambda_permission_s3encryption_use1" {
  statement_id  = "AllowExecutionFromSNSUSE1"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_s3encryption.function_name
  principal     = "sns.amazonaws.com"
  
  source_arn = local.sns_s3encryption_use1
}

resource "aws_lambda_permission" "lambda_permission_s3encryption_usw2" {
  statement_id  = "AllowExecutionFromSNSUSW2"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_s3encryption.function_name
  principal     = "sns.amazonaws.com"

  source_arn = local.sns_s3encryption_usw2
}

resource "aws_lambda_permission" "lambda_permission_s3encryption_euc1" {
  statement_id  = "AllowExecutionFromSNSEUC1"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_s3encryption.function_name
  principal     = "sns.amazonaws.com"

  source_arn = local.sns_s3encryption_euc1
}
