import boto3 
import utils 

def tag_autoscaling():
    autoscaling = boto3.client('autoscaling', region_name=utils.Account.region)
    
    #Autoscaling Group Ids 
    autoscaling_names = get_autoscaling_names(autoscaling)

    #Filtered Group Ids 
    filtered_autoscaling_names = [] 
    
    #Autoscaling Group Tag
    for name in autoscaling_names:
        autoscaling_updated = False 
        autoscaling_tags = autoscaling.describe_tags(Filters=[{'Name': 'auto-scaling-group', 'Values': [name]}])['Tags']
        autoscaling_keys = [autoscaling_tag['Key'] for autoscaling_tag in autoscaling_tags]
        
        for default_tag in utils.default_tags:
            if default_tag['Key'] not in autoscaling_keys:
                update_autoscaling_tags = [
                    {
                        'ResourceId': name,
                        'ResourceType': 'auto-scaling-group',
                        'Key': default_tag['Key'],
                        'Value': default_tag['Value'],
                        'PropagateAtLaunch': True
                    }
                ]
                autoscaling.create_or_update_tags(Tags=update_autoscaling_tags)
                autoscaling_updated = True 
        if autoscaling_updated: 
            filtered_autoscaling_names.append(name)
    
    return filtered_autoscaling_names

def get_autoscaling_names(autoscaling):

    autoscaling_names = [] 
    autoscaling_response = autoscaling.describe_auto_scaling_groups()
    
    while 'NextToken' in autoscaling_response.keys():
        autoscaling_groups = autoscaling_response['AutoScalingGroups']
        for autoscaling_group in autoscaling_groups:
            autoscaling_names.append(autoscaling_group['AutoScalingGroupName']) 
        token = autoscaling_response['NextToken']
        autoscaling_response = autoscaling.describe_auto_scaling_groups(NextToken=token)
    autoscaling_groups = autoscaling_response['AutoScalingGroups']
    
    for autoscaling_group in autoscaling_groups:
        autoscaling_names.append(autoscaling_group['AutoScalingGroupName']) 
        
    return autoscaling_names
    