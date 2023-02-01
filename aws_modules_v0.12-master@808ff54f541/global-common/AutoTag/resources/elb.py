import boto3
import utils 

def tag_elb():
    elb = boto3.client('elb', region_name=utils.Account.region)
    
    #ELB Ids 
    elb_ids = get_elb_load_balancer_names(elb)
    
    #Filtered ELB Ids 
    filtered_elb_ids = [] 
    
    #Filter and Tag ELB
    for name in elb_ids:
        elb_updated = False 
        elb_tags = elb.describe_tags(LoadBalancerNames=[name])['TagDescriptions'][0]['Tags']
        elb_keys = [elb_tag['Key'] for elb_tag in elb_tags]
        for default_tag in utils.default_tags:
            if default_tag['Key'] not in elb_keys: 
                elb.add_tags(LoadBalancerNames=[name], Tags=[default_tag])
                elb_updated = True 
        if elb_updated:
            filtered_elb_ids.append(name)
    
    return filtered_elb_ids

def tag_elbv2():
    elbv2 = boto3.client('elbv2', region_name=utils.Account.region)
    
    #ELBV2 Arns
    elbv2_load_balancer_arns = get_elbv2_load_balancer_arns(elbv2)
    elbv2_target_group_arns = get_elbv2_target_group_arns(elbv2)
    
    #Filtered ELBV2 Arns 
    filtered_elbv2_load_balancer_arns = [] 
    filtered_elbv2_target_group_arns = [] 
    
    #Filter and Tag ELBV2 Load Balancers
    for arn in elbv2_load_balancer_arns:
        load_balancer_updated = False 
        elbv2_load_balancer_tags = elbv2.describe_tags(ResourceArns=[arn])['TagDescriptions'][0]['Tags']
        elbv2_load_balancer_keys = [elbv2_load_balancer_tag['Key'] for elbv2_load_balancer_tag in elbv2_load_balancer_tags]
        for default_tag in utils.default_tags:
            if default_tag['Key'] not in elbv2_load_balancer_keys: 
                elbv2.add_tags(ResourceArns=[arn], Tags=[default_tag])
                load_balancer_updated = True 
        if load_balancer_updated: 
            filtered_elbv2_load_balancer_arns.append(arn)
    
    #Filter and Tag ELBV2 Target Groups 
    for arn in elbv2_target_group_arns:
        target_group_updated = False 
        elbv2_target_group_tags = elbv2.describe_tags(ResourceArns=[arn])['TagDescriptions'][0]['Tags']
        elbv2_target_group_keys = [elbv2_target_group_tag['Key'] for elbv2_target_group_tag in elbv2_target_group_tags]
        for default_tag in utils.default_tags:
            if default_tag['Key'] not in elbv2_target_group_keys: 
                elbv2.add_tags(ResourceArns=[arn], Tags=[default_tag])
                target_group_updated = True 
        if target_group_updated: 
            filtered_elbv2_target_group_arns.append(arn) 
    
    return filtered_elbv2_load_balancer_arns + filtered_elbv2_target_group_arns

def get_elb_load_balancer_names(elb):
    elb_ids = [] 
    lb_response = elb.describe_load_balancers()
    while 'NextMarker' in lb_response.keys():
        elb_ids += utils.extract_id(lb_response, 'LoadBalancerDescriptions', 'LoadBalancerName')
        marker = lb_response['NextMarker']
        lb_response = elb.describe_load_balancers(Marker=marker)
    elb_ids += utils.extract_id(lb_response, 'LoadBalancerDescriptions', 'LoadBalancerName')
    return elb_ids 

def get_elbv2_load_balancer_arns(elbv2):
    elbv2_ids = [] 
    lb2_response = elbv2.describe_load_balancers()
    while 'NextMarker' in lb2_response.keys():
        elbv2_ids += utils.extract_id(lb2_response, 'LoadBalancers', 'LoadBalancerArn')
        marker = lb2_response['NextMarker']
        lb2_response = elbv2.describe_load_balancers(Marker=marker)
    elbv2_ids += utils.extract_id(lb2_response, 'LoadBalancers', 'LoadBalancerArn')
    return elbv2_ids 

def get_elbv2_target_group_arns(elbv2):
    elbv2_ids = [] 
    target_group_response = elbv2.describe_target_groups()
    while 'NextMarker' in target_group_response.keys():
        elbv2_ids += utils.extract_id(target_group_response, 'TargetGroups', 'TargetGroupArn')
        marker = target_group_response['NextMarker']
        target_group_response = elbv2.describe_target_groups(Marker=marker)
    elbv2_ids += utils.extract_id(target_group_response, 'TargetGroups', 'TargetGroupArn')
    return elbv2_ids 