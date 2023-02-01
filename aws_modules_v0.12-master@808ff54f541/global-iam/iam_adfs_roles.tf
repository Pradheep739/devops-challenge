##############
# ADFS ROLES 
##############


# Adfs Admin Role
resource "aws_iam_role" "adm_role" {
  #provider = "aws-use1"
  name               = local.admin_rolename
  description        = "Role for the AWS Admins Access"
  assume_role_policy = data.aws_iam_policy_document.role-policy-document.json
  tags               = local.common_tags
}
# Adfs Admin Role Policy
resource "aws_iam_role_policy_attachment" "adm_policy-attach" {
  #provider = "aws-use1"
  role       = aws_iam_role.adm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
# ADFS Power User Role
resource "aws_iam_role" "pwuser_role" {
  #provider = "aws-use1"
  name               = local.pwrusr_rolename
  description        = "Role for the AWS Power User"
  assume_role_policy = data.aws_iam_policy_document.role-policy-document.json
  tags               = local.common_tags
}
# ADFS Power User Role Policy
resource "aws_iam_policy" "pwusr_role_policies" {
  #provider = "aws-use1"
  name        = local.pwusr_policyname
  description = "Policy for Power User"
  policy      = data.template_file.aws_pwusr_policy.rendered
}
# # ADFS Power User Role Policy01
# resource "aws_iam_policy" "pwusr_role_policies01" {
#   #provider = "aws-use1"
#   name        = local.pwusr_policyname01
#   description = "Policy for Power User 01"
#   policy      = data.template_file.aws_pwusr_policy01.rendered
# }
# ADFS Power User Role Policy Attachment
resource "aws_iam_role_policy_attachment" "pwusr_policy_attach" {
  #provider = "aws-use1"
  role       = aws_iam_role.pwuser_role.name
  policy_arn = aws_iam_policy.pwusr_role_policies.arn
}
# # ADFS Power User Role Policy Attachment 01
# resource "aws_iam_role_policy_attachment" "pwusr_policy_attach01" {
#   #provider = "aws-use1"
#   role       = aws_iam_role.pwuser_role.name
#   policy_arn = aws_iam_policy.pwusr_role_policies01.arn
# }
# ADFS Super Power User Role
resource "aws_iam_role" "suppwusr_role" {
  #provider = "aws-use1"
  name               = local.suppwusr_rolename
  description        = "Role for Super Power User"
  assume_role_policy = data.aws_iam_policy_document.role-policy-document.json
  tags               = local.common_tags
}
# ADFS Super Power User Role Policy
resource "aws_iam_policy" "suppwusr_role_policies" {
  #provider = "aws-use1"
  name        = local.suppwusr_policyname
  description = "Policy Super Power User"
  policy      = data.template_file.aws_super_pwusr_policy.rendered
}
# ADFS Super Power User Role Policy Attachment
resource "aws_iam_role_policy_attachment" "suppwusr_policy_attach" {
  #provider = "aws-use1"
  role       = aws_iam_role.suppwusr_role.name
  policy_arn = aws_iam_policy.suppwusr_role_policies.arn
}
# ADFS ReadOnly User Role
resource "aws_iam_role" "read_role" {
  #provider = "aws-use1"
  name               = local.read_rolename
  description        = "Role for the AWS User Access"
  assume_role_policy = data.aws_iam_policy_document.role-policy-document.json
  tags               = local.common_tags
}
# ADFS ReadOnly User Role Policy Attachement
resource "aws_iam_role_policy_attachment" "read-policy-attach" {
  #provider = "aws-use1"
  role       = aws_iam_role.read_role.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}