# VPC flow log IAM ROLE
resource "aws_iam_role" "vpcflowlog_role" {
  #provider = "aws.Account_assumeRole"
  name               = upper(local.vpcflowlog_rolename)
  description        = "Role for VPC FLowlogs"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "vpc-flow-logs.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# IAM policy for vpc flow log
resource "aws_iam_policy" "vpcflowlog_role_policies" {
  #provider = "aws.Account_assumeRole"
  name        = local.vpcflowlog_policyname
  description = "Policy for VPC FlowLogs"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}
#policy = data.template_file.aws_vpcflowlog_policy.rendered


# Policy attachment to vpc flow log
resource "aws_iam_role_policy_attachment" "policy-attach" {
  #provider = "aws.Account_assumeRole"
  role       = aws_iam_role.vpcflowlog_role.id
  policy_arn = aws_iam_policy.vpcflowlog_role_policies.arn
}
