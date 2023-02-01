##############
# CLOUDTRAIL
##############


# CloudWatch Log Group for Sending Cloudtrail Logs. 
# Would be retained in the log group for 90 days.

resource "aws_cloudwatch_log_group" "cloudtrail_loggroup" {
 name = local.cloudtrail-loggroup
 retention_in_days = 90
 tags = local.common_tags
}


# Cloudtrail Role
resource "aws_iam_role" "cloudtrail_role" {
  #provider = "aws.Account_assumeRole"
  name = local.cloudtrail_role_name
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
# Cloudtrail Role Policy Document
data "aws_iam_policy_document" "cloudtrail_iam_policydocument" {
  #provider = "aws.Account_assumeRole"
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    effect = "Allow"
    resources = [
      "${aws_cloudwatch_log_group.cloudtrail_loggroup.arn}:*"
    ]
  }
}
# Cloudtrail Policy
resource "aws_iam_policy" "cloudtrail_iam_policy" {
  #provider = "aws.Account_assumeRole"
  name   = local.cloudtrail_policy_name
  path   = "/"
  policy = data.aws_iam_policy_document.cloudtrail_iam_policydocument.json
}
# Cloudtrail Role Policy Attachement
resource "aws_iam_policy_attachment" "cloudtrail_role_policy_attach" {
  #provider = "aws.Account_assumeRole"
  name       = "cloudtrail-role-policy-attachment"
  roles      = [aws_iam_role.cloudtrail_role.name]
  policy_arn = aws_iam_policy.cloudtrail_iam_policy.arn
}

# Cloudtrail resource
resource "aws_cloudtrail" "cloudtrail" {
  #provider = "aws.Account_assumeRole"
  enable_log_file_validation    = true
  include_global_service_events = true
  is_multi_region_trail         = true
  #kms_key_id                    = aws_kms_key.cloudtrail_key.arn
  kms_key_id                   = local.ss_ctr_kms_key_arn
  name                          = local.cloudtrail_name
  s3_bucket_name                = local.cloudtrail_bucket

  # Send logs to CloudWatch Log group
  cloud_watch_logs_group_arn = "${aws_cloudwatch_log_group.cloudtrail_loggroup.arn}:*"
  cloud_watch_logs_role_arn  = aws_iam_role.cloudtrail_role.arn

  tags = local.common_tags
}
