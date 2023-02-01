import boto3 
import utils 

def tag_ecr():
    ecr = boto3.client('ecr', region_name=utils.Account.region)
    
    #ECR Arns
    ecr_arns = get_ecr_respository_arns(ecr)
    
    #Filtered ECR Arns 
    filtered_ecr_arns = [] 
    
    #Filter and Tag ECR 
    for arn in ecr_arns: 
        ecr_updated = False 
        ecr_tags = ecr.list_tags_for_resource(resourceArn=arn)['tags']
        ecr_keys = [ecr_tag['Key'] for ecr_tag in ecr_tags]
        for default_tag in utils.default_tags:
            if default_tag['Key'] not in ecr_keys: 
                ecr.tag_resource(resourceArn=arn, tags=[default_tag])
                ecr_updated = True 
        if ecr_updated: 
            filtered_ecr_arns.append(arn)
    
    return filtered_ecr_arns 

def get_ecr_respository_arns(ecr):
    ecr_arns = [] 
    repository_response = ecr.describe_repositories()
    while 'nextToken' in repository_response.keys():
        ecr_arns += utils.extract_id(repository_response, 'repositories', 'repositoryArn')
        token = repository_response['nextToken']
        repository_response = ecr.describe_repositories(nextToken=token)
    ecr_arns += utils.extract_id(repository_response, 'repositories', 'repositoryArn')
    return ecr_arns