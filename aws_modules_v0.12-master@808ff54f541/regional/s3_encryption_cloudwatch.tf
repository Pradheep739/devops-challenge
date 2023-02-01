# # SNS to subscribe
# resource "aws_sns_topic" "s3encryption_snstopic" {
#   name         = local.s3encryption_sns_name
#   display_name = local.s3encryption_sns_name
# }

# resource "aws_sns_topic_subscription" "s3encryption_snstopic_subscription" {
#   topic_arn = aws_sns_topic.s3encryption_snstopic.arn
#   protocol  = "lambda"
#   endpoint  = local.lambda_s3encryption_arn
# }


# # SNS Access Policy

# resource "aws_sns_topic_policy" "s3encryption_topic_policy" {
#   arn = aws_sns_topic.s3encryption_snstopic.arn

#   policy = data.aws_iam_policy_document.s3encryption_topic_policy_template.json
# }

# data "aws_iam_policy_document" "s3encryption_topic_policy_template" {
#   policy_id = "__default_policy_ID"

#   statement {
#     actions = [
#       "SNS:Subscribe",
#       "SNS:SetTopicAttributes",
#       "SNS:RemovePermission",
#       "SNS:Receive",
#       "SNS:Publish",
#       "SNS:ListSubscriptionsByTopic",
#       "SNS:GetTopicAttributes",
#       "SNS:DeleteTopic",
#       "SNS:AddPermission",
#     ]

#     condition {
#       test     = "StringEquals"
#       variable = "AWS:SourceOwner"

#       values = [
#         data.aws_caller_identity.current.account_id
#       ]
#     }

#     effect = "Allow"

#     principals {
#       type        = "AWS"
#       identifiers = ["*"]
#     }

#     resources = [
#       aws_sns_topic.s3encryption_snstopic.arn
#     ]

#     sid = "__default_statement_ID"
#   }
#   statement {
#     actions = [
#       "SNS:Publish",
#     ]

#     resources = [
#       aws_sns_topic.s3encryption_snstopic.arn
#     ]

#     effect = "Allow"

#     principals {
#       type        = "Service"
#       identifiers = ["events.amazonaws.com"]
#     }
#     sid = "aws_cw_events"
#   }
# }
# # cloudwatch event  to trigger when a new s3 bucket created
# resource "aws_cloudwatch_event_rule" "s3encryption_cwrule" {
#   name        = local.cw_s3encryption_name
#   description = "Tag EC2 Instances with OS Type and Owner (Instance Creator) upon creation"

#   event_pattern = <<PATTERN
# {
#   "source": [
#     "aws.s3"
#   ],
#   "detail-type": [
#     "AWS API Call via CloudTrail"
#   ],
#   "detail": {
#     "eventSource": [
#       "s3.amazonaws.com"
#     ],
#     "eventName": [
#       "CreateBucket"
#     ]
#   }
# }
# PATTERN
# }
# resource "aws_cloudwatch_event_target" "s3encryption_cwtarget" {
#   rule      = aws_cloudwatch_event_rule.s3encryption_cwrule.name
#   target_id = "SendToSNS"
#   arn       = aws_sns_topic.s3encryption_snstopic.arn
# }





