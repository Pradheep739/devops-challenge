{
	"Version": "2008-10-17",
	"Statement": [{
			"Sid": "Stmt1459217170695",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::${account_id}:root"
			},
			"Action": "s3:PutObject",
			"Resource": "arn:aws:s3:::${bucket_name}/*"
		},
		{
			"Sid": "DenyHttp",
			"Effect": "Deny",
			"Principal": {
				"AWS": "*"
			},
			"Action": [
				"s3:GetObject",
				"s3:PutObject"
			],
			"Resource": "arn:aws:s3:::${bucket_name}/*",
			"Condition": {
				"Bool": {
					"aws:SecureTransport": "false"
				}
			}
		}
	]
}