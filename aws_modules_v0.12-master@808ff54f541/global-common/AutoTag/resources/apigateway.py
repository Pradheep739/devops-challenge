import boto3 
import utils 

def tag_apigateway():
    apigateway = boto3.client('apigateway', region_name=utils.Account.region)
    
    #APIGateway Ids 
    api_key_ids = get_api_key_ids(apigateway)
    client_certificate_ids = get_client_certificate_ids(apigateway)
    domain_names = get_domain_names(apigateway)
    usage_plan_ids = get_usage_plan_ids(apigateway)
    vpc_link_ids = get_vpc_link_ids(apigateway)
    rest_api_id_and_stage_name_map = get_rest_api_ids_and_stage_names_arns(apigateway)
    rest_api_ids = list(rest_api_id_and_stage_name_map.keys())
    
    #APIGateway Arns 
    api_key_arns = [apigateway_get_api_key_arn(api_key_id) for api_key_id in api_key_ids]
    client_certificate_arns = [apigateway_get_client_certificate_arn(client_certificate_id) for client_certificate_id in client_certificate_ids]
    domain_name_arns = [apigateway_get_domain_name_arn(domain_name) for domain_name in domain_names]
    usage_plan_arns = [apigateway_get_usage_plan_arn(usage_plan_id) for usage_plan_id in usage_plan_ids]
    vpc_link_arns = [apigateway_get_vpc_link_arn(vpc_link_id) for vpc_link_id in vpc_link_ids]
    rest_api_arns = [apigateway_get_restapi_arn(rest_api_id) for rest_api_id in rest_api_ids]
    
    #Filtered APIGateway Arns 
    filtered_api_key_arns = [] 
    filtered_client_certificate_arns = [] 
    filtered_domain_name_arns = [] 
    filtered_usage_plan_arns = [] 
    filtered_vpc_link_arns = [] 
    filtered_rest_api_arns = []
    filtered_stage_arns = [] 
    
    #Filter and Tag API Keys 
    for index in range(len(api_key_arns)):
        api_key_updated = False 
        api_key = apigateway.get_api_key(apiKey=api_key_ids[index])
        api_key_tags = api_key['tags']
        for k,v in utils.apigateway_tags.items():
            if k not in api_key_tags.keys():
                apigateway.tag_resource(resourceArn=api_key_arns[index], tags={k:v})
                api_key_updated = True 
        if api_key_updated: 
            filtered_api_key_arns.append(api_key_arns[index])
    
    #Filter and Tag Client Certificates
    for index in range(len(client_certificate_arns)):
        client_certificate_updated = False 
        client_certificate = apigateway.get_client_certificate(clientCertificateId=client_certificate_ids[index])
        client_certificate_tags = client_certificate['tags']
        for k,v in utils.apigateway_tags.items():
            if k not in client_certificate_tags.keys():
                apigateway.tag_resource(resourceArn=client_certificate_arns[index], tags={k:v})
                client_certificate_updated = True 
        if client_certificate_updated: 
            filtered_client_certificate_arns.append(client_certificate_arns[index])
    
    #Filter and Tag Domain Names
    for index in range(len(domain_name_arns)):
        domain_name_updated = False 
        domain_name = apigateway.get_domain_name(domainName=domain_names[index])
        domain_name_tags = domain_name['tags']
        for k,v in utils.apigateway_tags.items():
            if k not in domain_name_tags.keys():
                apigateway.tag_resource(resourceArn=domain_name_arns[index], tags={k:v})
                domain_name_updated = True 
        if domain_name_updated:
            filtered_domain_name_arns.append(domain_name_arns[index])
    
    #Filter and Tag Usage Plans
    for index in range(len(usage_plan_arns)):
        usage_plan_updated = False 
        usage_plan = apigateway.get_usage_plan(usagePlanId=usage_plan_ids[index])
        usage_plan_tags = usage_plan['tags']
        for k,v in utils.apigateway_tags.items():
            if k not in usage_plan_tags.keys():
                apigateway.tag_resource(resourceArn=usage_plan_arns[index], tags={k:v})
                usage_plan_updated = True 
        if usage_plan_updated: 
            filtered_usage_plan_arns.append(usage_plan_arns[index])
    
    #Filter and Tag VPC Links
    for index in range(len(vpc_link_arns)):
        vpc_link_updated = False 
        vpc_link = apigateway.get_vpc_link(vpcLinkId=vpc_link_ids[index])
        vpc_link_tags = vpc_link['tags']
        for k,v in utils.apigateway_tags.items():
            if k not in vpc_link_tags.keys():
                apigateway.tag_resource(resourceArn=vpc_link_arns[index], tags={k:v})
                vpc_link_updated = True 
        if vpc_link_updated:
            filtered_vpc_link_arns.append(vpc_link_arns[index])
    
    #Filter and Tag Rest APIs
    for index in range(len(rest_api_arns)):
        rest_api_updated = False 
        rest_api = apigateway.get_rest_api(restApiId=rest_api_ids[index])
        rest_api_tags = rest_api['tags']
        for k,v in utils.apigateway_tags.items():
            if k not in rest_api_tags.keys():
                apigateway.tag_resource(resourceArn=rest_api_arns[index], tags={k:v})
                rest_api_updated = True 
        if rest_api_updated:
            filtered_rest_api_arns.append(rest_api_arns[index])
    
    #Filter and Tag Stages 
    stage_arns = [] 
    for rest_api_id in rest_api_ids:
        stage_names_and_arns = rest_api_id_and_stage_name_map[rest_api_id]
        for stage_name_arn_pair in stage_names_and_arns: 
            stage_updated = False 
            stage_name = stage_name_arn_pair[0]
            stage_arn = stage_name_arn_pair[1] 
            stage_arns.append(stage_arn)
            stage = apigateway.get_stage(restApiId=rest_api_id, stageName=stage_name)
            if 'tags' in stage.keys():
                stage_tags = stage['tags']
                for k,v in utils.apigateway_tags.items():
                    if k not in stage_tags.keys():
                        apigateway.tag_resource(resourceArn=stage_arn, tags={k:v})
                        stage_updated = True 
            else: 
                apigateway.tag_resource(resourceArn=stage_arn, tags=utils.apigateway_tags)
                stage_updated = True 
            if stage_updated: 
                filtered_stage_arns.append(stage_arn)
    
    return filtered_api_key_arns+filtered_client_certificate_arns+filtered_domain_name_arns+ \
        filtered_usage_plan_arns+filtered_vpc_link_arns+filtered_rest_api_arns+filtered_stage_arns

def get_api_key_ids(apigateway):
    api_key_ids = [] 
    
    api_key_response = apigateway.get_api_keys()
    while 'position' in api_key_response:
        api_keys = api_key_response['items']
        for api_key in api_keys:
            api_key_id = api_key['id']
            api_key_ids.append(api_key_id)
        position_token = api_key_response['position']
        api_key_response = apigateway.get_api_keys(position=position_token)
    api_keys = api_key_response['items']
    for api_key in api_keys:
        api_key_id = api_key['id']
        api_key_ids.append(api_key_id)
    
    return api_key_ids
    
def get_client_certificate_ids(apigateway):
    client_certificate_ids = [] 
    
    client_certificate_response = apigateway.get_client_certificates()
    while 'position' in client_certificate_response.keys():
        client_certificates = client_certificate_response['items']
        for client_certificate in client_certificates:
            client_certificate_id = client_certificate['clientCertificateId']
            client_certificate_ids.append(client_certificate_id)
        position_token = client_certificate_response['position']
        client_certificate_response = apigateway.get_client_certificates(position=position_token)
    client_certificates = client_certificate_response['items']
    for client_certificate in client_certificates:
        client_certificate_id = client_certificate['clientCertificateId']
        client_certificate_ids.append(client_certificate_id)
    
    return client_certificate_ids

def get_domain_names(apigateway):
    domain_names = [] 
    
    domain_name_response = apigateway.get_domain_names()
    while 'position' in domain_name_response.keys():
        domain_names = domain_name_response['items']
        for domain_name in domain_names:
            domainName = domain_name['domainName']
            domain_names.append(domainName)
        position_token = domain_name_response['position']
        domain_name_response = apigateway.get_domain_names(position=position_token)
    domain_names = domain_name_response['items']
    for domain_name in domain_names:
        domainName = domain_name['domainName']
        domain_names.append(domainName)

    return domain_names 

def get_usage_plan_ids(apigateway):
    usage_plan_ids = [] 
    
    usage_plan_response = apigateway.get_usage_plans()
    while 'position' in usage_plan_response.keys():
        usage_plans = usage_plan_response['items']
        for usage_plan in usage_plans:
            usage_plan_id = usage_plan['id']
            usage_plan_ids.append(usage_plan_id)
        position_token = usage_plan_response['position']
        usage_plan_response = apigateway.get_usage_plans(position=position_token)
    usage_plans = usage_plan_response['items']
    for usage_plan in usage_plans:
        usage_plan_id = usage_plan['id']
        usage_plan_ids.append(usage_plan_id)
        
    return usage_plan_ids 

def get_vpc_link_ids(apigateway):
    vpc_link_ids = [] 
    
    vpc_link_response = apigateway.get_vpc_links()
    while 'position' in vpc_link_response:
        vpc_links = vpc_link_response['items']
        for vpc_link in vpc_links:
            vpc_link_id = vpc_link['id']
            vpc_link_ids.append(vpc_link_id)
        position_token = vpc_link_response['position']
        vpc_link_response = apigateway.get_vpc_links(position=position_token)
    vpc_links = vpc_link_response['items']
    for vpc_link in vpc_links:
        vpc_link_id = vpc_link['id']
        vpc_link_ids.append(vpc_link_id)

    return vpc_link_ids 

def get_rest_api_ids_and_stage_names_arns(apigateway):
    
    rest_api_id_and_stage_name_map = {}
    
    apigateway_response = apigateway.get_rest_apis()
    while 'position' in apigateway_response.keys():
        apis = apigateway_response['items']
        for api in apis:
            rest_api_id = api['id']
            stage_response = apigateway.get_stages(restApiId=rest_api_id)
            stage_items = stage_response['item']
            stage_names_and_arns = [] 
            for stage in stage_items: 
                stage_name_arn_pair = [] 
                stage_name_arn_pair.append(stage['stageName'])
                stage_name_arn_pair.append(apigateway_get_stage_arn(rest_api_id, stage['stageName']))
                stage_names_and_arns.append(stage_name_arn_pair)
            rest_api_id_and_stage_name_map[rest_api_id] = stage_names_and_arns  
        position_token = apigateway_response['position']
        apigateway_response = apigateway.get_rest_apis(position=position_token)
    apis = apigateway_response['items']
    for api in apis:
        rest_api_id = api['id']
        stage_response = apigateway.get_stages(restApiId=rest_api_id)
        stage_items = stage_response['item']
        stage_names_and_arns = [] 
        for stage in stage_items: 
            stage_name_arn_pair = [] 
            stage_name_arn_pair.append(stage['stageName'])
            stage_name_arn_pair.append(apigateway_get_stage_arn(rest_api_id, stage['stageName']))
            stage_names_and_arns.append(stage_name_arn_pair)
        rest_api_id_and_stage_name_map[rest_api_id] = stage_names_and_arns  
    
    return rest_api_id_and_stage_name_map 
    
def apigateway_get_api_key_arn(api_key_id):
    return f'arn:aws:apigateway:{utils.Account.region}::/apikeys/{api_key_id}'

def apigateway_get_client_certificate_arn(client_certificate_id):
    return f'arn:aws:apigateway:{utils.Account.region}::/clientcertificates/{client_certificate_id}'

def apigateway_get_domain_name_arn(domain_name):
    return f'arn:aws:apigateway:{utils.Account.region}::/domainnames/{domain_name}'
    
def apigateway_get_restapi_arn(rest_api_id):
    return f'arn:aws:apigateway:{utils.Account.region}::/restapis/{rest_api_id}'
    
def apigateway_get_stage_arn(rest_api_id, stage_name):
    return f'arn:aws:apigateway:{utils.Account.region}::/restapis/{rest_api_id}/stages/{stage_name}'

def apigateway_get_usage_plan_arn(usage_plan_id):
    return f'arn:aws:apigateway:{utils.Account.region}::/usageplans/{usage_plan_id}'

def apigateway_get_vpc_link_arn(vpc_link_id):
    return f'arn:aws:apigateway:{utils.Account.region}::/vpclinks/{vpc_link_id}'
