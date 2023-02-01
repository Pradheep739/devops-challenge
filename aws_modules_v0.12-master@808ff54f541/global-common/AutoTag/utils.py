'''
Default tags defined in correct format for various resource types.
Configure environment variables to contain tag key and tag value 
'Account' class contains region and account_id variables that other functions can call for obtaining ARN 
'''

import os 
    
#Get Default Tags from Environment Variables 
env_vars = {'Owner': os.getenv('Owner'), 'BusinessUnit': os.getenv('BusinessUnit'), 'CostCenter': os.getenv('CostCenter'), 'Environment': os.getenv('Environment'), 'WBS': os.getenv('WBS')}
env_keys = list(env_vars.keys()) #[key1, key2, ...]

#Resource Tagging Formats 
default_tags = [{'Key': key, 'Value': os.getenv(key)} for key in env_keys]
   
ecs_tags = [{'key': key, 'value': os.getenv(key)} for key in env_keys]
    
s3_tags = {'TagSet': default_tags}
 
eks_tags = glue_tags = kinesis_tags = lambda_tags = sqs_tags = apigateway_tags = env_vars
    
cloudfront_tags = {'Items': default_tags}
  
kms_tags = [{'TagKey': key, 'TagValue': os.getenv(key)} for key in env_keys]

#Account Attributes (region and ID)
class Account: 
    
    region = ''
    account_id = ''
    
    def update_account_id(accountID):
        Account.account_id = accountID
    
    def update_region(region):
        Account.region = region 

#Get IDs from boto3 client describe calls 
def extract_id(response, key1, key2):
    id_list = [] 
    resources = response[key1]
    for resource in resources:
        id_list.append(resource[key2])
    return id_list 
    