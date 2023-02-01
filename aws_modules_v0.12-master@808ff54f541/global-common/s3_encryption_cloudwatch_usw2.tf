# SNS to subscribe
resource "aws_sns_topic" "s3encryption_snstopic_usw2" {
  provider  = aws.uswest2
  name         = local.s3encryption_sns_name_usw2
  display_name = local.s3encryption_sns_name_usw2
  tags = merge(local.common_tags, map("Name", format(local.s3encryption_sns_name_usw2)))
}
resource "aws_sns_topic_subscription" "s3encryption_snstopic_subscription_usw2" {
  provider  = aws.uswest2
  topic_arn = aws_sns_topic.s3encryption_snstopic_usw2.arn
  protocol  = "lambda"
  #endpoint  = local.lambda_s3encryption_arn
  endpoint  = aws_lambda_function.lambda_s3encryption.arn
}

# SNS Access Policy
resource "aws_sns_topic_policy" "s3encryption_topic_policy_usw2" {
  provider  = aws.uswest2
  arn = aws_sns_topic.s3encryption_snstopic_usw2.arn
  policy = data.aws_iam_policy_document.s3encryption_topic_policy_template_usw2.json
}

data "aws_iam_policy_document" "s3encryption_topic_policy_template_usw2" {
  #provider  = aws.uswest2
  policy_id = "__default_policy_ID"
  statement {
    actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:RemovePermission",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:AddPermission",
    ]
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceOwner"
      values = [
        data.aws_caller_identity.current.account_id
      ]
    }
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    resources = [
      aws_sns_topic.s3encryption_snstopic_usw2.arn
    ]
    sid = "__default_statement_ID"
  }
  statement {
    actions = [
      "SNS:Publish",
    ]
    resources = [
      aws_sns_topic.s3encryption_snstopic_usw2.arn
    ]
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
    sid = "aws_cw_events"
  }
}

# cloudwatch event  to trigger when a new s3 bucket created
resource "aws_cloudwatch_event_rule" "s3encryption_cwrule_usw2" {
  provider  = aws.uswest2
  name        = local.cw_s3encryption_name_usw2
  description = "Tag EC2 Instances with OS Type and Owner (Instance Creator) upon creation"
  event_pattern = <<PATTERN
{
  "source": [
    "aws.s3"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "s3.amazonaws.com"
    ],
    "eventName": [
      "CreateBucket"
    ]
  }
}
PATTERN
}

resource "aws_cloudwatch_event_target" "s3encryption_cwtarget_usw2" {
  provider  = aws.uswest2
  rule      = aws_cloudwatch_event_rule.s3encryption_cwrule_usw2.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.s3encryption_snstopic_usw2.arn
}

