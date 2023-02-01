import boto3
import utils 

def tag_cloudwatch():
    cloudwatch = boto3.client('cloudwatch', region_name=utils.Account.region)
    
    #CloudWatch Arns
    cloudwatch_arns = get_cloudwatch_alarm_arns(cloudwatch)
    
    #Filtered CloudWatch Arns 
    filtered_cloudwatch_arns = [] 
    
    #CloudWatch Tag
    for arn in cloudwatch_arns:
        cloudwatch_updated = False 
        cloudwatch_tags = cloudwatch.list_tags_for_resource(ResourceARN=arn)['Tags']
        cloudwatch_keys = [cloudwatch_tag['Key'] for cloudwatch_tag in cloudwatch_tags]
        for default_tag in utils.default_tags:
            if default_tag['Key'] not in cloudwatch_keys: 
                cloudwatch.tag_resource(ResourceARN=arn, Tags=[default_tag])
                cloudwatch_updated = True 
        if cloudwatch_updated:
            filtered_cloudwatch_arns.append(arn)
    
    return filtered_cloudwatch_arns

def get_cloudwatch_alarm_arns(cloudwatch):
    alarm_arns = [] 
    alarm_response = cloudwatch.describe_alarms()
    while 'NextToken' in alarm_response.keys():
        alarm_arns += utils.extract_id(alarm_response, 'MetricAlarms', 'AlarmArn')
        token = alarm_response['NextToken']
        alarm_response = cloudwatch.describe_alarms(NextToken=token)
    alarm_arns += utils.extract_id(alarm_response, 'MetricAlarms', 'AlarmArn')
    return alarm_arns
