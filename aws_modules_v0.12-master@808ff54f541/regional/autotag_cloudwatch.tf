# # SNS to subscribe
# resource "aws_sns_topic" "autotag_snstopic" {
#   name         = local.autotag_sns_name
#   display_name = local.autotag_sns_name
#   tags = merge(local.common_tags, map("Name", format(local.autotag_sns_name)))
# }

# #SNS subscription to lambda
# resource "aws_sns_topic_subscription" "autotag_snstopic_subscription" {
#   topic_arn = aws_sns_topic.autotag_snstopic.arn
#   protocol  = "lambda"
#   endpoint  = local.lambda_autotag_arn
# }

# resource "aws_sns_topic_policy" "autotag_topic_policy" {
#   arn = aws_sns_topic.autotag_snstopic.arn

#   policy = data.aws_iam_policy_document.autotag_topic_policy_template.json
# }

# data "aws_iam_policy_document" "autotag_topic_policy_template" {
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
#       aws_sns_topic.autotag_snstopic.arn
#     ]

#     sid = "__default_statement_ID"
#   }
#   statement {
#     actions = [
#       "SNS:Publish",
#     ]

#     resources = [
#       aws_sns_topic.autotag_snstopic.arn
#     ]

#     effect = "Allow"

#     principals {
#       type        = "Service"
#       identifiers = ["events.amazonaws.com"]
#     }
#     sid = "aws_cw_events"
#   }
# }
# # cloudwatch event rule to trigger when a new ec2 created
# resource "aws_cloudwatch_event_rule" "ec2ownertag" {
#   name        = local.cw_ec2autotag_name
#   description = "Tag EC2 Instances with OS Type and Owner (Instance Creator) upon creation"

#   event_pattern = <<PATTERN
# {
#   "source": [
#     "aws.ec2"
#   ],
#   "detail-type": [
#     "AWS API Call via CloudTrail"
#   ],
#   "detail": {
#     "eventSource": [
#       "ec2.amazonaws.com"
#     ],
#     "eventName": [
#       "RunInstances"
#     ]
#   }
# }
# PATTERN
# }

# #Cloudwatch event rule target
# resource "aws_cloudwatch_event_target" "ec2ownertagsns" {
#   rule      = aws_cloudwatch_event_rule.ec2ownertag.name
#   target_id = "SendToSNS"
#   arn       = aws_sns_topic.autotag_snstopic.arn
# }

# # Cloudwatch event rule to run once a day for tagging default tags all possible resources
# resource "aws_cloudwatch_event_rule" "autotag" {
#   name        = local.cw_autotag_name
#   description = "Tag all listed resources with default tags , runs once a day"
#   schedule_expression = "rate(1 day)"
# }

# # Cloudwatch event rule target to trigger SNS to trigger lambda
# resource "aws_cloudwatch_event_target" "autotagsns" {
#   rule      = aws_cloudwatch_event_rule.autotag.name
#   target_id = "SendToSNS"
#   arn       = aws_sns_topic.autotag_snstopic.arn
# }



