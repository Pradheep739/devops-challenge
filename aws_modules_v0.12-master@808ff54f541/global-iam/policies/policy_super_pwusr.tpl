{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "IAMAccess",
			"Effect": "Deny",
			"Action": [
				"iam:CreateUser",
				"iam:UpdateUser",
				"iam:DeleteUser",
				"iam:CreateGroup",
				"iam:UpdateGroup",
				"iam:DeleteGroup"
			],
			"Resource": "*"
		},
		{
			"Sid": "NetworkAccess",
			"Effect": "Deny",
			"Action": [
				"ec2:CreateInternetGateway",
				"ec2:DeleteInternetGateway",
				"ec2:AttachInternetGateway",
				"ec2:DetachInternetGateway"
			],
			"Resource": "*"
		},
		{
			"Sid": "DenyVPCCreation",
			"Effect": "Deny",
			"Action": [
				"ec2:CreateDefaultVpc",
				"ec2:CreateVpc"
			],
			"Resource": "*",
			"Condition": {
				"StringNotEquals": {
					"aws:RequestedRegion": [
						"us-west-2",
						"us-east-1",
						"eu-central-1"
					]
				}
			}
		},
		{
            "Sid": "S3Encryptionconfig",
            "Effect": "Deny",
            "Action": "s3:PutEncryptionConfiguration",
            "Resource": "*"
        },
		{
			"Sid": "LaunchingEC2withAMIsAndTags",
			"Effect": "Deny",
			"Action": "ec2:RunInstances",
			"Resource": "arn:aws:ec2:*::image/ami-*",
			"Condition": {
				"StringNotEquals": {
					"ec2:ResourceTag/HardenedAMI": "Yes"
				}
			}
		},
		{
            "Sid": "Guardduty",
            "Effect": "Deny",
            "Action": [
                 "guardduty:Delete*"
            ],
            "Resource": "*"
        },
		{
			"Sid": "AWSAdminAccess",
			"Effect": "Allow",
			"Action": "*",
			"Resource": "*"
		}
	]
}