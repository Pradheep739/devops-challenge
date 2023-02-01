'''
Lambda function will collect all users in account and publish SNS message to renew access keys that approach or exceed age_limit.
SNS message is published if access key is found with age greater than age_warning.
Message body includes username, access key, and access key age along with recommended action to update old access keys
SNS should be configured with an email subscription to receive message. 
SNS Topic ARN should be added as a Lambda environment variable with key: SNSTopicArn, value: [insert Topic ARN]
Account Name should also be added as a Lambda environment variable with key: AccountName, value: [insert Account Name]
'''

import json
import boto3 
import datetime
import time 
import os 
import sys

iam = boto3.client('iam')
sns = boto3.client('sns')
sts = boto3.client('sts')

#Get Account ID for reference
caller_identity_resp = sts.get_caller_identity()
account_id = caller_identity_resp['Account']
account_name = os.environ['AccountName']

#Enforce access key age limit of 180 days. Warn users 30 days beforehand 
age_limit = 180
age_warning = 150
    
if age_warning > age_limit: 
    print(f'Age warning: {age_warning}')
    print(f'Age limit: {age_limit}')
    print('Age warning must be less than age limit')
    sys.exit(1)

def lambda_handler(event, context):
    
    #Collect User Names
    usernames = get_user_names()
    
    #Collect All Users' Access Keys 
    user_accesskeys = get_user_accesskeys(usernames)
    
    print(user_accesskeys)
    
    #Get Message to Send to SNS Topic
    [old_account_found, message] = get_message(user_accesskeys)
    
    #Send Message to SNS if Access Key found with age that meets warning threshold
    if old_account_found:
        print('Access Keys found to be approaching or has exceeded age limit')
        send_message(message)
        print('------------------------------------------')
        print(message)
    else:
        print('No old access keys found. All access keys are under the 150 day age warning period. Access keys should be renewed after 180 days.')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
def get_user_names():
    usernames = []
    list_users_response = iam.list_users()
    is_truncated = list_users_response['IsTruncated']
    users = list_users_response['Users']
    while is_truncated:
        for user in users:
            usernames.append(user['UserName'])
        marker = list_users_response['Marker']
        list_users_response = iam.list_users(Marker=marker)
        is_truncated = list_users_response['IsTruncated']
    for user in users:
        usernames.append(user['UserName'])
    return usernames 

def get_user_accesskeys(usernames):
    '''
    user_accesskeys: Type dict 
    username: Type str 
    accesskey: Type str 
    age: Type int 
    {username1: [[accesskey1, age1], [accesskey2, age2], ...], username2: [[accesskey3, age3], [accesskey4, age4], ...]}
    '''
    user_accesskeys = {} 
    for username in usernames: 
        #Create Full List where all accesskey info resides
        accesskeys_info = [] 
        
        #Populate accesskey_info 
        list_access_keys_response = iam.list_access_keys(UserName=username)
        is_truncated = list_access_keys_response['IsTruncated']
        while is_truncated:
            #List of Metadata for each Access Key
            accesskey_metadata_list = list_access_keys_response['AccessKeyMetadata']
            for accesskey_metadata in accesskey_metadata_list:
                #Get Access Key Id
                accesskey = accesskey_metadata['AccessKeyId']
                
                #Get Age of Access Key
                accesskeydate = accesskey['CreateDate'].date()
                currentdate = datetime.datetime.now().date()
                delta = currentdate - accesskeydate
                accesskey_age = delta.days 
                
                #Form Pair 
                accesskey_age_pair = [accesskey, accesskey_age]
                
                #Add Pair to Full List 
                accesskeys_info.append(accesskey_age_pair)
            marker = list_access_keys_response['Marker']
            list_access_keys_response = iam.list_access_keys(UserName=username, Marker=marker)
            is_truncated = list_access_keys_response['IsTruncated']
        #List of Metadata for each Access Key
        accesskey_metadata_list = list_access_keys_response['AccessKeyMetadata']
        for accesskey_metadata in accesskey_metadata_list:
            #Get Access Key Id
            accesskey = accesskey_metadata['AccessKeyId']
                
            #Get Age of Access Key
            accesskeydate = accesskey_metadata['CreateDate'].date()
            currentdate = datetime.datetime.now().date()
            delta = currentdate - accesskeydate
            accesskey_age = delta.days 
                
            #Form Pair 
            accesskey_age_pair = [accesskey, accesskey_age]
                
            #Add Pair to Full List 
            accesskeys_info.append(accesskey_age_pair)
        
        #Form Key-Value Mapping of Username to Accesskey Info
        user_accesskeys[username] = accesskeys_info
    
    return user_accesskeys

def get_message(user_accesskeys):
    
    message = f'AWS access key renewal recommended for the following users in account name: {account_name} and account id: {account_id} if access key age approaches or exceeds {age_limit} days: \n'

    old_account_found = False
    for username in user_accesskeys.keys():
        accesskeys_info = user_accesskeys[username]
        for accesskey_age_pair in accesskeys_info: 
            access_key = accesskey_age_pair[0]
            age = accesskey_age_pair[1] 
            message += f'\nUsername: {username}\nAccess Key: {access_key}\nAge: {age} days \n'
            if age < age_warning:
                message += f'Security Warning: None\n'
            elif age_warning <= age < age_limit:
                old_account_found = True 
                difference = age_limit - age
                message += f'Security Warning: Access key age will reach {age_limit} days in {difference} days \n'
            else:
                old_account_found = True 
                message += f'Security Warning: Access key age exceeded {age_limit} days. Update to new access key \n'
            
    return [old_account_found, message]

def send_message(message):
    #Configure correct Topic ARN and subscription and add it as an environment variable to this lambda function 
    topic_arn = os.environ['SNSTopicArn']
    subject = f"AWS Account {account_id} IAM User Access Key Notification"
    sns.publish(TopicArn=topic_arn, Message=message, Subject=subject)
    