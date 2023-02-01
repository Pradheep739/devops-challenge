'''
EC2 Instance Tagging upon creation (Default Tags, Owner, and OSTYPE)
CloudWatch Events Rule should be configured as CloudTrail Event Pattern with 'RunInstances' action
Event variable contains EC2 instance id, username of instance owner, existing tags, and platform type 
'''

import boto3 
import utils 
import json 

def ec2_instance_tag(event):
    ec2 = boto3.client('ec2', region_name=utils.Account.region)
    
    try:
        event_message = event['Records'][0]['Sns']['Message']
        event_message_json = json.loads(event_message)
        ec2_instance_items = event_message_json['detail']['responseElements']['instancesSet']['items']
        
        #Get EC2 Instance Owner User Name 
        try: 
            user_name = event_message_json['detail']['userIdentity']['principalId']
            user_name = user_name.split(":",1)[1]
        except Exception as e: 
            print(e)
            user_name = 'root'
        
        for ec2_instance in ec2_instance_items:
            #Get EC2 Instance ID 
            ec2_instance_id = ec2_instance['instanceId']
            
            print('----------------------------')
            print(ec2_instance_id)
            
            #Get EC2 Instance OS Type and Existing Tag Keys 
            ec2_instance_platform_and_tagkeys = get_ec2_instance_platform_and_tagkeys(ec2, ec2_instance_id)
            ec2_instance_platform = ec2_instance_platform_and_tagkeys[0]
            ec2_instance_tagkeys = ec2_instance_platform_and_tagkeys[1]
            
            #EC2 Owner Tagging
            if 'Owner' not in ec2_instance_tagkeys: 
                owner_tag = {} 
                owner_tag['Key'] = 'InstanceOwner'
                owner_tag['Value'] = user_name 
                ec2.create_tags(Resources=[ec2_instance_id], Tags=[owner_tag])
            
            #EC2 OS Tagging
            if 'OSTYPE' not in ec2_instance_tagkeys:
                os_tag = {} 
                os_tag['Key'] = 'OSTYPE'
                os_tag['Value'] = ec2_instance_platform 
                ec2.create_tags(Resources=[ec2_instance_id], Tags=[os_tag])
            
            #EC2 Default Tagging 
            for default_tag in utils.default_tags:
                if default_tag['Key'] not in ec2_instance_tagkeys:
                    ec2.create_tags(Resources=[ec2_instance_id], Tags=[default_tag])
                    
    except Exception as e:
        print("Exception while tagging EC2 Instances during creation: " + str(e))
    
    return

def get_ec2_instance_platform_and_tagkeys(ec2, ec2_instance_id):
    
    ec2_instance_platform_and_tagkeys = []
    ec2_instance_response = ec2.describe_instances(Filters=[{'Name':'instance-id', 'Values':[ec2_instance_id]}])
    ec2_instance_info = ec2_instance_response['Reservations'][0]['Instances'][0]
    
    if 'Platform' in ec2_instance_info.keys():
        ec2_instance_platform = ec2_instance_info['Platform'].upper()
    else:
        ec2_instance_platform = 'LINUX'
    ec2_instance_platform_and_tagkeys.append(ec2_instance_platform)
    
    if 'Tags' in ec2_instance_info.keys():
        tags = ec2_instance_info['Tags']
        ec2_instance_keys = [tag['Key'] for tag in tags]
    else:
        ec2_instance_keys = [] 
    ec2_instance_platform_and_tagkeys.append(ec2_instance_keys)
    
    return ec2_instance_platform_and_tagkeys