# #############
# # AWS Config
# #############

# # AWS Config Recorder
# resource "aws_config_configuration_recorder" "config-record" {
#   name     = "default"
#   recording_group {
#     all_supported = "true"
#     include_global_resource_types = "true"
#   }
#   role_arn = data.aws_iam_role.config_role.arn
# }


# # AWS Config Recorder Status
# resource "aws_config_configuration_recorder_status" "configrecordstatus" {
#   name       = aws_config_configuration_recorder.config-record.name
#   is_enabled = true
#   depends_on = [aws_config_delivery_channel.config-del-channel]
# }

# # AWS Config Delivery Channel
# resource "aws_config_delivery_channel" "config-del-channel" {
#   name           = "default"
#   snapshot_delivery_properties {
#     delivery_frequency = "One_Hour"
#   }
#   s3_bucket_name = local.config_bucket[var.aws_region]
#   depends_on     = [aws_config_configuration_recorder.config-record]
# }