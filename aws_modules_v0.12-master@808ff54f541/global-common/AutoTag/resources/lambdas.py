import boto3 
import utils

def tag_lambdas():
    lambda_client = boto3.client('lambda', region_name=utils.Account.region)
    
    #Lambda Ids
    lambda_arns = get_lambda_function_arns(lambda_client)
    
    #Filtered Lambda Ids 
    filtered_lambda_arns = [] 
    
    #Filter and Tag Lambda 
    for arn in lambda_arns:
        lambda_updated = False 
        lambda_tags = lambda_client.list_tags(Resource=arn)['Tags']
        lambda_keys = list(lambda_tags.keys())
        for k,v in utils.lambda_tags.items():
            if k not in lambda_keys: 
                lambda_client.tag_resource(Resource=arn, Tags={k:v})
                lambda_updated = True 
        if lambda_updated: 
            filtered_lambda_arns.append(arn)
    
    return filtered_lambda_arns 

def get_lambda_function_arns(lambda_client):
    lambda_arns = [] 
    lambda_response = lambda_client.list_functions()
    while 'NextMarker' in lambda_response.keys():
        lambda_arns += utils.extract_id(lambda_response, 'Functions', 'FunctionArn')
        marker = lambda_response['NextMarker']
        lambda_response = lambda_client.list_functions(Marker=marker)
    lambda_arns += utils.extract_id(lambda_response, 'Functions', 'FunctionArn')
    return lambda_arns