#### CROSS ACCOUNT ROLES ####
# Role with cross account relation with Shared Services Production Account

# SS Cross account Role
resource "aws_iam_role" "ss-cross-role" {
  #provider = "aws-use1"
  name               = local.ss_rolename
  description        = "Role for Cross Account Role for Shared Service"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "AWS" : "arn:aws:iam::${local.shared_services_account}:root"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# SS Cross account Role Policy attachements
resource "aws_iam_role_policy_attachment" "ec2fullacc-policy-attach" {
  #provider = "aws-use1"
  role       = aws_iam_role.ss-cross-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_role_policy_attachment" "vpcfullacc-policy-attach" {
  #provider = "aws-use1"
  role       = aws_iam_role.ss-cross-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
}

resource "aws_iam_role_policy_attachment" "tageditorreadonlyaccess-policy-attach" {
  #provider = "aws-use1"
  role       = aws_iam_role.ss-cross-role.name
  policy_arn = "arn:aws:iam::aws:policy/ResourceGroupsandTagEditorReadOnlyAccess"
}