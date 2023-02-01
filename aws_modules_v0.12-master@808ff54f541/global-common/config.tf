#############
# AWS Config
#############


# set up a role for the Configuration Recorder to use

resource "aws_iam_role" "config_role" {
  name = local.config_role_name

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "config.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
}
 

# config role Policy
resource "aws_iam_policy" "config-role-policies" {
  name        = local.config_policy_name
  description = "Policy for config role"
  policy      = data.template_file.aws_config_policy.rendered
}

resource "aws_iam_role_policy_attachment" "config_policy_attachment" {
  role       = aws_iam_role.config_role.name
  policy_arn = aws_iam_policy.config-role-policies.arn
}


# US-WEST-2
# AWS Config Recorder
resource "aws_config_configuration_recorder" "config-record_usw2" {
  provider = aws.uswest2
  name     = "default"
  recording_group {
    all_supported = "true"
    include_global_resource_types = "true"
  }
  role_arn = aws_iam_role.config_role.arn
}


# AWS Config Recorder Status
resource "aws_config_configuration_recorder_status" "configrecordstatus_usw2" {
  provider = aws.uswest2
  name       = aws_config_configuration_recorder.config-record_usw2.name
  is_enabled = true
  depends_on = [aws_config_delivery_channel.config-del-channel_usw2]
}

# AWS Config Delivery Channel
resource "aws_config_delivery_channel" "config-del-channel_usw2" {
  provider = aws.uswest2
  name           = "default"
  snapshot_delivery_properties {
    delivery_frequency = "One_Hour"
  }
  s3_bucket_name = local.config_bucket[var.aws_region]
  depends_on     = [aws_config_configuration_recorder.config-record_usw2]
}


# US-EAST-1
# AWS Config Recorder
resource "aws_config_configuration_recorder" "config-record_use1" {
  provider = aws.useast1
  name     = "default"
  recording_group {
    all_supported = "true"
    include_global_resource_types = "true"
  }
  role_arn = aws_iam_role.config_role.arn
}


# AWS Config Recorder Status
resource "aws_config_configuration_recorder_status" "configrecordstatus_use1" {
  provider = aws.useast1
  name       = aws_config_configuration_recorder.config-record_use1.name
  is_enabled = true
  depends_on = [aws_config_delivery_channel.config-del-channel_use1]
}

# AWS Config Delivery Channel
resource "aws_config_delivery_channel" "config-del-channel_use1" {
  provider = aws.useast1
  name           = "default"
  snapshot_delivery_properties {
    delivery_frequency = "One_Hour"
  }
  s3_bucket_name = local.config_bucket[var.aws_region]
  depends_on     = [aws_config_configuration_recorder.config-record_use1]
}


# EU-CENTRAL-1
# AWS Config Recorder
resource "aws_config_configuration_recorder" "config-record_euc1" {
  provider = aws.eucentral1
  name     = "default"
  recording_group {
    all_supported = "true"
    include_global_resource_types = "true"
  }
  role_arn = aws_iam_role.config_role.arn
}


# AWS Config Recorder Status
resource "aws_config_configuration_recorder_status" "configrecordstatus_euc1" {
  provider = aws.eucentral1
  name       = aws_config_configuration_recorder.config-record_euc1.name
  is_enabled = true
  depends_on = [aws_config_delivery_channel.config-del-channel_euc1]
}

# AWS Config Delivery Channel
resource "aws_config_delivery_channel" "config-del-channel_euc1" {
  provider = aws.eucentral1
  name           = "default"
  snapshot_delivery_properties {
    delivery_frequency = "One_Hour"
  }
  s3_bucket_name = local.config_bucket[var.aws_region]
  depends_on     = [aws_config_configuration_recorder.config-record_euc1]
}