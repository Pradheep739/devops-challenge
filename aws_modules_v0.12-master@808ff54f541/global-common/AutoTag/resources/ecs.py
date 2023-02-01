import boto3 
import utils 

def tag_ecs():
    ecs = boto3.client('ecs', region_name=utils.Account.region)
    
    #ECS Arns
    ecs_arns = get_ecs_arns(ecs)
    
    #Filtered ECS Arns 
    filtered_ecs_arns = [] 
    
    #Filter and Tag ECS 
    for arn in ecs_arns:
        ecs_updated = False 
        ecs_tags = ecs.list_tags_for_resource(resourceArn=arn)['tags']
        ecs_keys = [ecs_tag['key'] for ecs_tag in ecs_tags]
        for ecs_tag in utils.ecs_tags: 
            if ecs_tag['key'] not in ecs_keys: 
                ecs.tag_resource(resourceArn=arn, tags=[ecs_tag])
                ecs_updated = True 
        if ecs_updated: 
            filtered_ecs_arns.append(arn)
    
    return filtered_ecs_arns

def get_ecs_arns(ecs):
    cluster_arns = [] 
    task_arns = [] 
    service_arns = [] 
    task_definition_arns = [] 
    container_instance_arns = [] 
    
    cluster_response = ecs.list_clusters()
    while 'nextToken' in cluster_response.keys():
        cluster_arns += cluster_response['clusterArns']
        token = cluster_response['nextToken']
        cluster_response = ecs.list_clusters(nextToken=token)
    cluster_arns += cluster_response['clusterArns']
    
    for cluster_arn in cluster_arns:
        task_response = ecs.list_tasks(cluster=cluster_arn)
        while 'nextToken' in task_response.keys():
            task_arns += task_response['taskArns']
            token = task_response['nextToken']
            task_response = ecs.list_tasks(cluster=cluster_arn, nextToken=token)
        task_arns += task_response['taskArns']
        service_response = ecs.list_services(cluster=cluster_arn)
        while 'nextToken' in service_response.keys():
            service_arns += service_response['serviceArns']
            token = service_response['nextToken']
            service_response = ecs.list_services(cluster=cluster_arn, nextToken=token)
        service_arns += service_response['serviceArns']

        container_instance_response = ecs.list_container_instances(cluster=cluster_arn)
        while 'nextToken' in container_instance_response.keys():
            container_instance_arns += container_instance_response['containerInstanceArns']
            token = container_instance_response['nextToken']
            container_instance_response = ecs.list_container_instances(cluster=cluster_arn, nextToken=token)
        container_instance_arns += container_instance_response['containerInstanceArns']

    task_definition_response = ecs.list_task_definitions()
    while 'nextToken' in task_definition_response.keys():
        task_definition_arns += task_definition_response['taskDefinitionArns']
        token = task_definition_response['nextToken']
        task_definition_response = ecs.list_task_definitions(nextToken=token)
    task_definition_arns += task_definition_response['taskDefinitionArns']

    return cluster_arns + task_arns + service_arns + task_definition_arns + container_instance_arns