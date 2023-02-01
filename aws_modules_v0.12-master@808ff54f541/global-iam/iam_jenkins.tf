#### JENKINS ROLE ####

# Jenkins Role
resource "aws_iam_role" "jenkins-role" {
  # provider = "aws-use1"
  name               = "ROLE-SHARED-JENKINS"
  description        = "Role for Jenkins"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com",
        "AWS" : "arn:aws:iam::${local.shared_services_account}:role/ROLE-SHARED-JENKINS"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# Jenkins Policy
resource "aws_iam_policy" "jenkins-role-policies" {
  #provider = "aws-use1"
  name        = "POLICY-SHARED-JENKINS"
  description = "Policy for Jenkins"
  policy      = data.template_file.aws_jenkins_policy.rendered
}

# Jenkins Role Policy Attachement
resource "aws_iam_role_policy_attachment" "jenkins-policy-attach" {
  #provider = "aws-use1"
  role       = aws_iam_role.jenkins-role.name
  policy_arn = aws_iam_policy.jenkins-role-policies.arn
}