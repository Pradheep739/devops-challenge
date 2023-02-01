#########################
# Deploy Lambda to calculate IAM user access keyage 
##########################

# Create achive of lambda code
data "archive_file" "zip" {
  type        = "zip"
  source_file = "${path.module}/aws_accesskeyage_notify.py"
  output_path = "${path.module}/aws_accesskeyage_notify.zip"
}

# Deploy the Lambda code
resource "aws_lambda_function" "lambda_accesskeyage" {
  function_name = "IAM-CheckAccessKeyAgeExpiration"

  filename         = data.archive_file.zip.output_path
  source_code_hash = data.archive_file.zip.output_base64sha256

  role = var.lambda_role
  handler = "aws_accesskeyage_notify.lambda_handler"
  runtime = "python3.7"
  timeout = 600
  environment {
    variables = {
      SNSTopicArn = aws_sns_topic.notifyops_snstopic.arn
      AccountName = var.account_name
    }
  }
  tags    = local.common_tags
}

# SNS Topic Resource
resource "aws_sns_topic" "notifyops_snstopic" {
  name         = local.notifyoperation_sns_name
  display_name = local.notifyoperation_sns_name
  tags    = local.common_tags
}

#Subscribe to the SNS
resource "null_resource" "create-access_keyage_subscription" {
  provisioner "local-exec" {
    command = "aws sns subscribe --topic-arn ${aws_sns_topic.notifyops_snstopic.arn} --protocol email --notification-endpoint ${local.dg_ops_email} --region ${var.aws_region} "
  }
}

# Cloudwatch event rule to run once a day for tagging default tags all possible resources
resource "aws_cloudwatch_event_rule" "cwaccesskeyage" {
  name        = local.cw_accesskeyage_name
  description = "Check IAM users accesskeys IAM-CheckAccessKeyAgeExpiration , runs once a day"
  schedule_expression = "rate(1 day)"
}

# Cloudwatch event rule target to trigger SNS to trigger lambda
resource "aws_cloudwatch_event_target" "cwtargetaccesskeyage" {
  rule      = aws_cloudwatch_event_rule.cwaccesskeyage.name
  arn       = aws_lambda_function.lambda_accesskeyage.arn
}

# Lambda permission to allow external sources invoking the Lambda function e.g. CloudWatch Event
resource "aws_lambda_permission" "accesskeyage_allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_accesskeyage.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cwaccesskeyage.arn  
}
