import json
import boto3
import os 
import sys 
import utils
import time 
from actions import eventpattern 
from actions import schedule 

'''
This Lambda function will be configured with CloudWatch Events Rule and Simple Notification Service 
to run multi-regional autotagging of resources with default tags at periodic intervals and 
tagging of EC2 instances with default tags, Owner, and OS Type upon creation. Pre-existing tags that 
satisfy default tag keys will not be affected. This function currently handles APIGateway, APIGatewayV2, 
AutoScalingGroups, CloudFront, CloudWatch, DynamoDB, EC2/VPC, ECR, ECS, EFS, EKS, ELB, ELBV2, Glue, Kinesis, 
KMS, Lambda, RDS, Redshift, S3, SNS, SQS, WAF, WAFV2. This function currently uses environment variables 
to access default tags (see utils.py)

AWS ARN List 
https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html
'''

def lambda_handler(event, context):
    start_time = time.time()
    
    #SNS event source 
    print(event['Records'][0]['EventSource'])
    print(event['Records'][0]['EventSubscriptionArn'])
    
    #Get region, account_id, and type of event dynamically 
    region = json.loads(event['Records'][0]['Sns']['Message'])['region']
    account_id = json.loads(event['Records'][0]['Sns']['Message'])['account']
    detail_type = json.loads(event['Records'][0]['Sns']['Message'])['detail-type']
    
    print(region)
    
    #Update region and account_id class variables in Utils Account class
    utils.Account.update_region(region)
    utils.Account.update_account_id(account_id)
    
    if detail_type == 'AWS API Call via CloudTrail':
        print('CloudTrail')
        eventpattern.ec2_instance_tag(event) 
    elif detail_type == 'Scheduled Event':
        print('Scheduled Event')
        schedule.tag_all()
    else:
        print('Unrecognized event type')
        return
    
    print('AutoTag Complete')
    print("--- %s seconds ---" % (time.time() - start_time))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    