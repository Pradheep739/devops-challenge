import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def put_bucket_encryption(kms_arn,aws_region,bucket_name,s3):
	logger.info("Running the encryption function")
	try:
		response = s3.put_bucket_encryption(
				Bucket=bucket_name,
				ServerSideEncryptionConfiguration={
						'Rules': [
								{
									'ApplyServerSideEncryptionByDefault': {
											'SSEAlgorithm': 'aws:kms',
											'KMSMasterKeyID': kms_arn
											}
									},
								]
						}
				)
		logger.info('Bucket {} in region {} is encrypted with kms_key {}'.format(bucket_name,aws_region,kms_arn))
		return response
	except Exception as e:
		logger.error('Error occurred when encrypting the bucket {} is {}'.format(bucket_name, e))
		return e


def get_kms(aws_region):
	try:
		kms_client = boto3.client('kms', region_name=aws_region)
		kms_response = kms_client.list_aliases()['Aliases']
		keys = [keys_ids['AliasName'] for keys_ids in kms_response]
		modified_keys = dict()
		for key_id in keys:
			key_response = kms_client.describe_key(KeyId=key_id)['KeyMetadata']
			if key_response['KeyManager'] == 'CUSTOMER' and key_response['KeyState'] == 'Enabled':
				modified_keys[key_response['KeyId']] = key_response['CreationDate']
		logger.info("returning the kms arn of the key")
		return sorted(modified_keys.items(), key=lambda x: x[1])[0][0]
	except Exception as e:
		logger.debug("The Error occurred when fetching Kms key is {}".format(e))


def check_bucket_encryption(aws_region,bucket_name,s3):
	logger.info("checking the bucket encryption")
	s3_response = s3.head_bucket(Bucket=bucket_name)
	if s3_response['ResponseMetadata']['HTTPStatusCode'] == 200:
		try:
			s3_encrypt = s3.get_bucket_encryption(Bucket=bucket_name)
			rules = s3_encrypt['ServerSideEncryptionConfiguration']['Rules']
			logger.info("Bucket: {}, Encryption: {".format(bucket_name, rules))
			logger.info("Bucket {} is already encrypted".format(bucket_name))
			return "The bucket {} is encrypted with the rules {}".format(bucket_name,rules)
		except Exception as e:
			logger.error("Error occurred when checking for the bucket encryption for {} is {}".format(bucket_name,e))
			if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
				logger.info("Bucket {} has no server side encryption enabled".format(bucket_name))
				logger.info("Encrypting the bucket with the kms key in the region {}".format(aws_region))
				logger.info("Getting the kms key arn for the region {}".format(aws_region))
				kms_arn = get_kms(aws_region)
				logger.info("Encrypting the bucket {} with the kms key {}".format(bucket_name,kms_arn))
				encrypting_bucket = put_bucket_encryption(kms_arn,aws_region,bucket_name,s3)
				logger.info(encrypting_bucket)
				if encrypting_bucket['ResponseMetadata']['HTTPStatusCode'] == 200:
					return "The bucket {}, in the region {} is encrypted with the kms key {}".format(bucket_name,aws_region,kms_arn)
				else:
					return "The Error occurred when encrypting the bucket {} with kms key {}".format(bucket_name,aws_region)
			else:
				return "Error occurred when finding for the bucket encryption is {}".format(e)


def lambda_handler(event,context):
	logger.info("starting the lambda function")
	s3_client = boto3.client('s3')
	message = event['Records'][0]['Sns']['Message']
	modified_message = json.loads(message)
	aws_region = modified_message['detail']['awsRegion']
	try:
		logger.info("Getting the newly created bucket name")
		if 'bucketName' in modified_message['detail']['requestParameters']:
			bucket_name = modified_message['detail']['requestParameters']['bucketName']
			logger.info("the bucket {} is newly created in region {}".format(bucket_name, aws_region))
			bucket_encryption = check_bucket_encryption(aws_region,bucket_name,s3_client)
			logger.info(bucket_encryption)
		else:
			logger.error("The bucket name is not present in the response event {}".format(modified_message))
	except Exception as e:
		logger.debug("UnExpected Error occurred when running the code".format(e))
