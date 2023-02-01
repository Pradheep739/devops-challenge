import boto3
import utils 

def tag_eks():
    eks = boto3.client('eks', region_name=utils.Account.region)
    
    #EKS Arns
    try: 
        eks_arns = get_eks_cluster_arns(eks)
    except Exception as e:
        print(e)
        return []

    try: 
        eks_arns += get_eks_nodegroup_arns(eks)
    except Exception as e:
        print(e) 
        return []
    
    #Filtered EKS Arns
    filtered_eks_arns = [] 
    
    #Filter and Tag EKS 
    for arn in eks_arns:
        eks_updated = False 
        eks_tags = eks.list_tags_for_resource(resourceArn=arn)['tags']
        eks_keys = list(eks_tags.keys())
        for k,v in utils.eks_tags.items(): 
            if k not in eks_keys:
               eks.tag_resource(resourceArn=arn, tags={k:v})
               eks_updated = True 
        if eks_updated: 
            filtered_eks_arns.append(arn)
    
    return filtered_eks_arns

def get_eks_cluster_arns(eks):
    eks_arns = [] 
    cluster_names = [] 
    cluster_response = eks.list_clusters()
    while 'nextToken' in cluster_response.keys():
        cluster_names += cluster_response['clusters']
        token = cluster_response['nextToken']
        cluster_response = eks.list_clusters(nextToken=token)
    cluster_names += cluster_response['clusters']
    eks_arns = [eks_get_cluster_arn(cluster_name) for cluster_name in cluster_names]
    return eks_arns 

def get_eks_nodegroup_arns(eks):
    eks_arns = [] 
    cluster_names = [] 
    cluster_response = eks.list_clusters()
    while 'nextToken' in cluster_response.keys():
        cluster_names += cluster_response['clusters']
        token = cluster_response['nextToken']
        cluster_response = eks.list_clusters(nextToken=token)
    cluster_names += cluster_response['clusters']
    
    for cluster_name in cluster_names:
        nodegroup_response = eks.list_nodegroups(clusterName=cluster_name)
        while 'nextToken' in nodegroup_response.keys():
            nodegroup_names = nodegroup_response['nodegroups']
            for nodegroup_name in nodegroup_names:
                nodegroup_description = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
                eks_arns.append(nodegroup_description['nodegroup']['nodegroupArn'])
            token = nodegroup_response['nextToken']
            nodegroup_response = eks.list_nodegroups(clusterName=cluster_name, nextToken=token)
        nodegroup_names = nodegroup_response['nodegroups']
        for nodegroup_name in nodegroup_names:
            nodegroup_description = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
            eks_arns.append(nodegroup_description['nodegroup']['nodegroupArn'])
    
    return eks_arns

def eks_get_cluster_arn(cluster_name):
    return f'arn:aws:eks:{utils.Account.region}:{utils.Account.account_id}:cluster/{cluster_name}'