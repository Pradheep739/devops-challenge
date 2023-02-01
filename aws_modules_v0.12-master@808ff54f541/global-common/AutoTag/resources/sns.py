import boto3 
import utils 

def tag_sns():
    sns = boto3.client('sns', region_name=utils.Account.region)
    
    #SNS Arns
    sns_arns = get_sns_topic_arns(sns)
    
    #Filtered SNS Arns 
    filtered_sns_arns = [] 
    
    #SNS Tag
    for arn in sns_arns:
        sns_updated = False 
        sns_tags = sns.list_tags_for_resource(ResourceArn=arn)['Tags']
        sns_keys = [sns_tag['Key'] for sns_tag in sns_tags]
        for default_tag in utils.default_tags: 
            if default_tag['Key'] not in sns_keys: 
                sns.tag_resource(ResourceArn=arn, Tags=[default_tag])
                sns_updated = True 
        if sns_updated: 
            filtered_sns_arns.append(arn)
    
    return filtered_sns_arns 

def get_sns_topic_arns(sns):
    sns_arns = [] 
    sns_response = sns.list_topics()
    while 'NextToken' in sns_response.keys():
        sns_arns += utils.extract_id(sns_response, 'Topics', 'TopicArn')
        token = sns_response['NextToken']
        sns_response = sns.list_topics(NextToken=token)
    sns_arns += utils.extract_id(sns_response, 'Topics', 'TopicArn')
    return sns_arns 