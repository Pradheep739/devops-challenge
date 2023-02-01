
############################################
# Cloudwatch alarams to support config rules
#############################################

resource "aws_cloudwatch_metric_alarm" "CwAlarm1" {
  alarm_name = "root_account_login"
  alarm_description = "A CloudWatch Alarm that triggers if a root user uses the account."
  metric_name = "RootUserEventCount"
  namespace = "CloudTrailMetrics"
  statistic = "Sum"
  period = "60"
  threshold = "1"
  evaluation_periods = "1"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions = [ aws_sns_topic.notifyops_snstopic.arn ]
  treat_missing_data = "notBreaching"
  tags = local.common_tags
}

resource "aws_cloudwatch_log_metric_filter" "MetricFilter1" {
  #log_group_name = var.cloudtrail_loggroup
  log_group_name = aws_cloudwatch_log_group.cloudtrail_loggroup.id
  pattern = "{ ($.userIdentity.type = \"Root\") && ($.userIdentity.invokedBy NOT EXISTS) && ($.eventType != \"AwsServiceEvent\") }"
  name = "RootUserEventCount"

  metric_transformation {
    name = "RootUserEventCount"
    value = "1"
    namespace = "CloudTrailMetrics"
  }
}

resource "aws_cloudwatch_metric_alarm" "CwAlarm2" {
  alarm_name = "unauthorized_api_calls"
  alarm_description = "A CloudWatch Alarm that triggers if Multiple unauthorized actions or logins attempted."
  metric_name = "UnauthorizedAttemptCount"
  namespace = "CloudTrailMetrics"
  statistic = "Sum"
  period = "60"
  threshold = "1"
  evaluation_periods = "1"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions = [ aws_sns_topic.notifyops_snstopic.arn ]
  treat_missing_data = "notBreaching"
  tags = local.common_tags
}

resource "aws_cloudwatch_log_metric_filter" "MetricFilter2" {
  
  #log_group_name = var.cloudtrail_loggroup
  log_group_name = aws_cloudwatch_log_group.cloudtrail_loggroup.id
  pattern = "{ ($.errorCode = \"*UnauthorizedOperation\") || ($.errorCode = \"AccessDenied*\") }"
  name = "UnauthorizedAttemptCount"

  metric_transformation {
    name = "UnauthorizedAttemptCount"
    value = "1"
    namespace = "CloudTrailMetrics"
  }

}

resource "aws_cloudwatch_metric_alarm" "CwAlarm3" {
  
  alarm_name = "no_mfa_console_logins"
  alarm_description = "A CloudWatch Alarm that triggers if there is a Management Console sign-in without MFA."
  metric_name = "ConsoleSigninWithoutMFA"
  namespace = "CloudTrailMetrics"
  statistic = "Sum"
  period = "60"
  threshold = "1"
  evaluation_periods = "1"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions = [ aws_sns_topic.notifyops_snstopic.arn ]
  treat_missing_data = "notBreaching"
  tags = local.common_tags
}

resource "aws_cloudwatch_log_metric_filter" "MetricFilter3" {
  #log_group_name = var.cloudtrail_loggroup
  log_group_name = aws_cloudwatch_log_group.cloudtrail_loggroup.id
  pattern = "{($.eventName = \"ConsoleLogin\") && ($.additionalEventData.MFAUsed != \"Yes\") && ($.responseElements.ConsoleLogin != \"Failure\") && ($.additionalEventData.SamlProviderArn NOT EXISTS) }"
  name = "ConsoleSigninWithoutMFA"

  metric_transformation {
    name = "ConsoleSigninWithoutMFA"
    value = "1"
    namespace = "CloudTrailMetrics"
  }

}


resource "aws_cloudwatch_metric_alarm" "CwAlarm4" {
  alarm_name = "iam_policy_changes"
  alarm_description = "A CloudWatch Alarm that triggers when changes are made to IAM policies. Events include IAM policy creation/deletion/update operations as well as attaching/detaching policies from IAM users, roles or groups."
  metric_name = "IAMPolicyEventCount"
  namespace = "CloudTrailMetrics"
  statistic = "Sum"
  period = "300"
  threshold = "1"
  evaluation_periods = "1"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions = [ aws_sns_topic.notifyops_snstopic.arn ]
  treat_missing_data = "notBreaching"
  tags = local.common_tags
}

resource "aws_cloudwatch_log_metric_filter" "MetricFilter4" {
  #log_group_name = var.cloudtrail_loggroup
  log_group_name = aws_cloudwatch_log_group.cloudtrail_loggroup.id
  pattern = "{($.eventName=DeleteGroupPolicy)||($.eventName=DeleteRolePolicy)||($.eventName=DeleteUserPolicy)||($.eventName=PutGroupPolicy)||($.eventName=PutRolePolicy)||($.eventName=PutUserPolicy)||($.eventName=CreatePolicy)||($.eventName=DeletePolicy)||($.eventName=CreatePolicyVersion)||($.eventName=DeletePolicyVersion)||($.eventName=AttachRolePolicy)||($.eventName=DetachRolePolicy)||($.eventName=AttachUserPolicy)||($.eventName=DetachUserPolicy)||($.eventName=AttachGroupPolicy)||($.eventName=DetachGroupPolicy)}"
  name = "IAMPolicyEventCount"

  metric_transformation {
    name = "IAMPolicyEventCount"
    value = "1"
    namespace = "CloudTrailMetrics"
  }

}

resource "aws_cloudwatch_metric_alarm" "CwAlarm5" {
  alarm_name = "cloudtrail_changes"
  alarm_description = "A CloudWatch Alarm that triggers when changes are made to CloudTrail."
  metric_name = "CloudTrailEventCount"
  namespace = "CloudTrailMetrics"
  statistic = "Sum"
  period = "300"
  threshold = "1"
  evaluation_periods = "1"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions = [ aws_sns_topic.notifyops_snstopic.arn ]
  treat_missing_data = "notBreaching"
  tags = local.common_tags
}

resource "aws_cloudwatch_log_metric_filter" "MetricFilter5" {
  #log_group_name = var.cloudtrail_loggroup
  log_group_name = aws_cloudwatch_log_group.cloudtrail_loggroup.id
  pattern = "{ ($.eventName = CreateTrail) || ($.eventName = UpdateTrail) || ($.eventName = DeleteTrail) || ($.eventName = StartLogging) || ($.eventName = StopLogging) }"
  name = "CloudTrailEventCount"

  metric_transformation {
    name = "CloudTrailEventCount"
    value = "1"
    namespace = "CloudTrailMetrics"
  }

}

resource "aws_cloudwatch_metric_alarm" "CwAlarm7" {
  alarm_name = "disabled_deleted_cmks"
  alarm_description = "A CloudWatch Alarm that triggers if customer created CMKs get disabled or scheduled for deletion."
  metric_name = "KMSCustomerKeyDeletion"
  namespace = "CloudTrailMetrics"
  statistic = "Sum"
  period = "60"
  threshold = "1"
  evaluation_periods = "1"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions = [ aws_sns_topic.notifyops_snstopic.arn ]
  treat_missing_data = "notBreaching"
  tags = local.common_tags
}

resource "aws_cloudwatch_log_metric_filter" "MetricFilter7" {
  #log_group_name = var.cloudtrail_loggroup
  log_group_name = aws_cloudwatch_log_group.cloudtrail_loggroup.id
  pattern = "{ ($.eventSource = kms.amazonaws.com) &&  (($.eventName=DisableKey) || ($.eventName=ScheduleKeyDeletion)) }"
  name = "KMSCustomerKeyDeletion"

  metric_transformation {
    name = "KMSCustomerKeyDeletion"
    value = "1"
    namespace = "CloudTrailMetrics"
  }

}

resource "aws_cloudwatch_metric_alarm" "CwAlarm8" {
  alarm_name = "s3_changes"
  alarm_description = "A CloudWatch Alarm that triggers when changes are made to an S3 Bucket."
  metric_name = "S3BucketActivityEventCount"
  namespace = "CloudTrailMetrics"
  statistic = "Sum"
  period = "300"
  threshold = "1"
  evaluation_periods = "1"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions = [ aws_sns_topic.notifyops_snstopic.arn ]
  treat_missing_data = "notBreaching"
  tags = local.common_tags
}

resource "aws_cloudwatch_log_metric_filter" "MetricFilter8" {
  #log_group_name = var.cloudtrail_loggroup
  log_group_name = aws_cloudwatch_log_group.cloudtrail_loggroup.id
  pattern = "{ ($.eventSource = s3.amazonaws.com) && (($.eventName = PutBucketAcl) || ($.eventName = PutBucketPolicy) || ($.eventName = PutBucketCors) || ($.eventName = PutBucketLifecycle) || ($.eventName = PutBucketReplication) || ($.eventName = DeleteBucketPolicy) || ($.eventName = DeleteBucketCors) || ($.eventName = DeleteBucketLifecycle) || ($.eventName = DeleteBucketReplication)) }"
  name = "S3BucketActivityEventCount"

  metric_transformation {
    name = "S3BucketActivityEventCount"
    value = "1"
    namespace = "CloudTrailMetrics"
  }

}

resource "aws_cloudwatch_metric_alarm" "CwAlarm9" {
  alarm_name = "config_changes"
  alarm_description = "A CloudWatch Alarm that triggers when changes are made to AWS Config."
  metric_name = "CloudTrailEventCount"
  namespace = "CloudTrailMetrics"
  statistic = "Sum"
  period = "300"
  threshold = "1"
  evaluation_periods = "1"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions = [ aws_sns_topic.notifyops_snstopic.arn ]
  treat_missing_data = "notBreaching"
  tags = local.common_tags
}

resource "aws_cloudwatch_log_metric_filter" "MetricFilter9" {
  #log_group_name = var.cloudtrail_loggroup
  log_group_name = aws_cloudwatch_log_group.cloudtrail_loggroup.id
  pattern = "{ ($.eventName = PutConfigurationRecorder) || ($.eventName = StopConfigurationRecorder) || ($.eventName = DeleteDeliveryChannel) || ($.eventName = PutDeliveryChannel) }"
  name = "ConfigEventCount"

  metric_transformation {
    name = "CloudTrailEventCount"
    value = "1"
    namespace = "CloudTrailMetrics"
  }

}



