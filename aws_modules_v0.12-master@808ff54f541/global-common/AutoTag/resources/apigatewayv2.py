import boto3 
import utils 

def tag_apigatewayv2():
    apigatewayv2 = boto3.client('apigatewayv2', region_name=utils.Account.region)
    
    #API Ids 
    api_stage_map = get_api_stage_map(apigatewayv2)
    api_ids = list(api_stage_map.keys())
    
    #API Arns 
    api_arns = [apigatewayv2_get_api_arn(api_id) for api_id in api_ids]
    
    #Filtered API Arns 
    filtered_api_arns = [] 
    
    #Filtered Stage Arns 
    filtered_stage_arns = [] 
    
    #Filter and Tag APIs 
    for index in range(len(api_arns)):
        api_updated = False 
        api = apigatewayv2.get_api(ApiId=api_ids[index])
        api_tags = api['Tags']
        for k,v in utils.apigateway_tags.items():
            if k not in api_tags.keys():
                apigatewayv2.tag_resource(ResourceArn=api_arns[index], Tags={k:v})
                api_updated = True 
        if api_updated: 
            filtered_api_arns.append(api_arns[index])
    
    #Filter and Tag Stages 
    stage_arns = [] #Stage Arn List
    for api_id in api_ids: 
        stage_names_and_arns = api_stage_map[api_id]
        for stage_name_arn_pair in stage_names_and_arns: 
            stage_updated = False 
            stage_name = stage_name_arn_pair[0]
            stage_arn = stage_name_arn_pair[1] 
            stage_arns.append(stage_arn) #Collect Stage Arns
            stage = apigatewayv2.get_stage(ApiId=api_id, StageName=stage_name)
            stage_tags = stage['Tags']
            for k,v in utils.apigateway_tags.items():
                if k not in stage_tags.keys():
                    apigatewayv2.tag_resource(ResourceArn=stage_arn, Tags={k:v})
                    stage_updated = True 
            if stage_updated: 
                filtered_stage_arns.append(stage_arn)
                    
    return filtered_api_arns + filtered_stage_arns

def get_api_stage_map(apigatewayv2):
    api_stage_map = {}
    
    apigatewayv2_response = apigatewayv2.get_apis()
    while 'NextToken' in apigatewayv2_response.keys():
        apis = apigatewayv2_response['Items']
        for api in apis:
            api_id = api['ApiId']
            stage_response = apigatewayv2.get_stages(ApiId=api_id)
            stage_names_and_arns = []
            while 'NextToken' in stage_response.keys():
                stages = stage_response['Items']
                for stage in stages:
                    stage_name_arn_pair = [] 
                    stage_name_arn_pair.append(stage['StageName'])
                    stage_name_arn_pair.append(apigatewayv2_get_stage_arn(api_id, stage_name))
                    stage_names_and_arns.append(stage_name_arn_pair)
                api_stage_map[api_id] = stage_names_and_arns 
                token = stage_response['NextToken']
                stage_response = apigatewayv2.get_stages(ApiId=api_id, NextToken=token)
            stages = stage_response['Items']
            for stage in stages:
                stage_name_arn_pair = [] 
                stage_name_arn_pair.append(stage['StageName'])
                stage_name_arn_pair.append(apigatewayv2_get_stage_arn(api_id, stage_name))
                stage_names_and_arns.append(stage_name_arn_pair)
            api_stage_map[api_id] = stage_names_and_arns 
        token = apigatewayv2_response['NextToken']
        apigatewayv2_response = apigateway.get_apis(NextToken=token)
    apis = apigatewayv2_response['Items']
    for api in apis:
        api_id = api['ApiId']
        stage_response = apigatewayv2.get_stages(ApiId=api_id)
        stage_names_and_arns = []
        while 'NextToken' in stage_response.keys():
            stages = stage_response['Items']
            for stage in stages:
                stage_name_arn_pair = [] 
                stage_name_arn_pair.append(stage['StageName'])
                stage_name_arn_pair.append(apigatewayv2_get_stage_arn(api_id, stage_name))
                stage_names_and_arns.append(stage_name_arn_pair)
            api_stage_map[api_id] = stage_names_and_arns 
            token = stage_response['NextToken']
            stage_response = apigatewayv2.get_stages(ApiId=api_id, NextToken=token)
        stages = stage_response['Items']
        for stage in stages:
            stage_name_arn_pair = [] 
            stage_name = stage['StageName']
            stage_name_arn_pair.append(stage_name)
            stage_name_arn_pair.append(apigatewayv2_get_stage_arn(api_id, stage_name))
            stage_names_and_arns.append(stage_name_arn_pair)
        api_stage_map[api_id] = stage_names_and_arns 
        
    return api_stage_map

def apigatewayv2_get_api_arn(api_id):
    return f'arn:aws:apigateway:{utils.Account.region}::/apis/{api_id}'

def apigatewayv2_get_stage_arn(api_id, stage_name):
    return f'arn:aws:apigateway:{utils.Account.region}::/apis/{api_id}/stages/{stage_name}'

