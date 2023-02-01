{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AccessKeyAgeNotifyPermissions",
            "Effect": "Allow",
            "Action": [
                "iam:ListUsers",
                "iam:ListAccessKeys",
                "SNS:Publish"
            ],
            "Resource": "*"
        }
    ]
}