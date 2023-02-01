############
# KMS Keys
############
# US-WEST-2
resource "aws_kms_alias" "alias_usw2" {
  provider = aws.uswest2
  name          = "alias/${local.kms_key_name_usw2}"
  target_key_id = aws_kms_key.key_usw2.key_id
}
resource "aws_kms_key" "key_usw2" {
  #policy = data.template_file.kms_policy.rendered
  provider = aws.uswest2
  policy = data.aws_iam_policy_document.kms_policy.json
  enable_key_rotation = true
  tags = merge(local.common_tags, map("Name", format(local.kms_key_name_usw2)))
}

# US-EAST-1
resource "aws_kms_alias" "alias_use1" {
  provider = aws.useast1
  name          = "alias/${local.kms_key_name_use1}"
  target_key_id = aws_kms_key.key_use1.key_id
}
resource "aws_kms_key" "key_use1" {
  #policy = data.template_file.kms_policy.rendered
  provider = aws.useast1
  policy = data.aws_iam_policy_document.kms_policy.json
  enable_key_rotation = true
  tags = merge(local.common_tags, map("Name", format(local.kms_key_name_use1)))
}

# EU-CENTRAL-1
resource "aws_kms_alias" "alias_euc1" {
  provider = aws.eucentral1
  name          = "alias/${local.kms_key_name_euc1}"
  target_key_id = aws_kms_key.key_euc1.key_id
}
resource "aws_kms_key" "key_euc1" {
  #policy = data.template_file.kms_policy.rendered
  provider = aws.eucentral1
  policy = data.aws_iam_policy_document.kms_policy.json
  enable_key_rotation = true
  tags = merge(local.common_tags, map("Name", format(local.kms_key_name_euc1)))
}