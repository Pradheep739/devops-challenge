{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "appstream:Get*",
                "autoscaling:Describe*",
                "cloudformation:DescribeStacks",
                "cloudformation:DescribeStackEvents",
                "cloudformation:DescribeStackResource",
                "cloudformation:DescribeStackResources",
                "cloudformation:GetTemplate",
                "cloudformation:List*",
                "cloudfront:Get*",
                "cloudfront:List*",
                "cloudtrail:DescribeTrails",
                "cloudtrail:GetTrailStatus",
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "config:Put*",
                "directconnect:Describe*",
                "dynamodb:GetItem",
                "dynamodb:BatchGetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:DescribeTable",
                "dynamodb:ListTables",
                "ec2:Describe*",
                "elasticache:Describe*",
                "elasticbeanstalk:Check*",
                "elasticbeanstalk:Describe*",
                "elasticbeanstalk:List*",
                "elasticbeanstalk:RequestEnvironmentInfo",
                "elasticbeanstalk:RetrieveEnvironmentInfo",
                "elasticloadbalancing:Describe*",
                "elastictranscoder:Read*",
                "elastictranscoder:List*",
                "iam:List*",
                "iam:Get*",
                "kinesis:Describe*",
                "kinesis:Get*",
                "kinesis:List*",
                "opsworks:Describe*",
                "opsworks:Get*",
                "route53:Get*",
                "route53:List*",
                "redshift:Describe*",
                "redshift:ViewQueriesInConsole",
                "rds:Describe*",
                "rds:ListTagsForResource",
                "s3:Get*",
                "s3:List*",
                "sdb:GetAttributes",
                "sdb:List*",
                "sdb:Select*",
                "ses:Get*",
                "ses:List*",
                "sns:Get*",
                "sns:List*",
                "sqs:GetQueueAttributes",
                "sqs:ListQueues",
                "sqs:ReceiveMessage",
                "storagegateway:List*",
                "storagegateway:Describe*",
                "trustedadvisor:Describe*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject*"
            ],
            "Resource": [
                "arn:aws:s3:::*/AWSLogs/${account_id}/*"
            ],
            "Condition": {
                "StringLike": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketAcl"
            ],
            "Resource": [
                "arn:aws:s3:::${account_id}"
            ]
        },
        {
            "Sid": "Stmt1511208185407",
            "Action": [
                "acm:DescribeCertificate",
                "acm:ListCertificates"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}