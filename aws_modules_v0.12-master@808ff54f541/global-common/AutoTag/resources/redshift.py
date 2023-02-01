import boto3 
import utils 

def tag_redshift():
    redshift = boto3.client('redshift', region_name=utils.Account.region)
    
    #Redshift Arns
    redshift_arns = get_redshift_cluster_arns(redshift)

    redshift_arns += get_redshift_hsm_config_arns(redshift)

    redshift_arns += get_redshift_hsm_client_arns(redshift)

    redshift_arns += get_redshift_cluster_parameter_group_arns(redshift)

    redshift_arns += get_redshift_cluster_snapshot_arns(redshift)

    redshift_arns += get_redshift_cluster_subnet_group_arns(redshift)
    
    #Filtered Redshift Arns 
    filtered_redshift_arns = []
    
    #Redshift Tag
    for arn in redshift_arns:
        redshift_updated = False 
        redshift_tagged_resources = redshift.describe_tags(ResourceName=arn)['TaggedResources']
        redshift_keys = [redshift_tagged_resource['Tag']['Key'] for redshift_tagged_resource in redshift_tagged_resources]
        for default_tag in utils.default_tags: 
            if default_tag['Key'] not in redshift_keys: 
                redshift.create_tags(ResourceName=arn, Tags=[default_tag])
                redshift_updated = True 
        if redshift_updated: 
            filtered_redshift_arns.append(arn)
        print('----------------------')
    return filtered_redshift_arns

def get_redshift_cluster_arns(redshift):
    cluster_response = redshift.describe_clusters()
    redshift_names = [] 
    while 'Marker' in cluster_response.keys():
        redshift_names += utils.extract_id(cluster_response, 'Clusters', 'ClusterIdentifier')
        marker = cluster_response['Marker']
        cluster_response = redshift.describe_clusters(Marker=marker)
    redshift_names += utils.extract_id(cluster_response, 'Clusters', 'ClusterIdentifier')
    redshift_arns = [redshift_get_cluster_arn(name) for name in redshift_names]
    return redshift_arns

def get_redshift_cluster_parameter_group_arns(redshift): 
    parameter_group_names = [] 
    cluster_parameter_group_response = redshift.describe_cluster_parameter_groups()
    while 'Marker' in cluster_parameter_group_response.keys():
        parameter_group_names += utils.extract_id(cluster_parameter_group_response, 'ParameterGroups', 'ParameterGroupName')
        marker = cluster_parameter_group_response['Marker']
        cluster_parameter_group_response = redshift.describe_cluster_parameter_groups(Marker=marker)
    parameter_group_names += utils.extract_id(cluster_parameter_group_response, 'ParameterGroups', 'ParameterGroupName')
    redshift_arns = [redshift_get_cluster_parameter_group_arn(parameter_group_name) for parameter_group_name in parameter_group_names]
    return redshift_arns

def get_redshift_cluster_snapshot_arns(redshift):
    cluster_snapshot_arn_params_list = [] 
    cluster_snapshot_response = redshift.describe_cluster_snapshots()
    while 'Marker' in cluster_snapshot_response.keys():
        cluster_snapshots = cluster_snapshot_response['Snapshots']
        for cluster_snapshot in cluster_snapshots:
            cluster_snapshot_arn_params = {} 
            cluster_snapshot_arn_params['SnapshotIdentifier'] = cluster_snapshot['SnapshotIdentifier']
            cluster_snapshot_arn_params['ClusterIdentifier'] = cluster_snapshot['ClusterIdentifier']
            cluster_snapshot_arn_params_list.append(cluster_snapshot_arn_params)
        marker = cluster_snapshot_response['Marker']
        cluster_snapshot_response = redshift.describe_cluster_snapshots(Marker=marker)
    cluster_snapshots = cluster_snapshot_response['Snapshots']
    for cluster_snapshot in cluster_snapshots:
        cluster_snapshot_arn_params = {} 
        cluster_snapshot_arn_params['SnapshotIdentifier'] = cluster_snapshot['SnapshotIdentifier']
        cluster_snapshot_arn_params['ClusterIdentifier'] = cluster_snapshot['ClusterIdentifier']
        cluster_snapshot_arn_params_list.append(cluster_snapshot_arn_params)
    redshift_arns = [redshift_get_cluster_snapshot_arn(cluster_snapshot_arn_params) for cluster_snapshot_arn_params in cluster_snapshot_arn_params_list]
    return redshift_arns

def get_redshift_cluster_subnet_group_arns(redshift):
    cluster_subnet_group_names = []
    cluster_subnet_group_response = redshift.describe_cluster_subnet_groups()
    while 'Marker' in cluster_subnet_group_response.keys():
        cluster_subnet_group_names += utils.extract_id(cluster_subnet_group_response, 'ClusterSubnetGroups', 'ClusterSubnetGroupName')
        marker = cluster_subnet_group_response['Marker']
        cluster_subnet_group_response = redshift.describe_cluster_subnet_groups(Marker=marker)
    cluster_subnet_group_names += utils.extract_id(cluster_subnet_group_response, 'ClusterSubnetGroups', 'ClusterSubnetGroupName')
    redshift_arns = [redshift_get_cluster_subnet_group_arn(cluster_subnet_group_name) for cluster_subnet_group_name in cluster_subnet_group_names]
    return redshift_arns 

def get_redshift_hsm_client_arns(redshift): 
    hsm_client_response = redshift.describe_hsm_client_certificates()
    while 'Marker' in hsm_client_response.keys():
        hsm_client_ids = utils.extract_id(hsm_client_response, 'HsmClientCertificates', 'HsmClientCertificateIdentifier')
        marker = hsm_client_response['Marker']
        hsm_client_response = redshift.describe_hsm_client_certificates(Marker=marker)
    hsm_client_ids = utils.extract_id(hsm_client_response, 'HsmClientCertificates', 'HsmClientCertificateIdentifier')
    redshift_arns = [redshift_get_hsm_client_arn(hsm_client_id) for hsm_client_id in hsm_client_ids]
    return redshift_arns 

def get_redshift_hsm_config_arns(redshift):
    hsm_config_ids = [] 
    hsm_config_response = redshift.describe_hsm_configurations()
    while 'Marker' in hsm_config_response.keys():
        hsm_config_ids += utils.extract_id(hsm_config_response, 'HsmConfigurations', 'HsmConfigurationIdentifier')
        marker = hsm_config_response['Marker']
        hsm_config_response = redshift.describe_hsm_configurations(Marker=marker)
    hsm_config_ids += utils.extract_id(hsm_config_response, 'HsmConfigurations', 'HsmConfigurationIdentifier')
    redshift_arns = [redshift_get_hsm_config_arn(hsm_config_id) for hsm_config_id in hsm_config_ids]
    return redshift_arns 

def redshift_get_cluster_arn(cluster_name):
    return f'arn:aws:redshift:{utils.Account.region}:{utils.Account.account_id}:cluster:{cluster_name}'

def redshift_get_cluster_parameter_group_arn(cluster_parameter_group_name):
    return f'arn:aws:redshift:{utils.Account.region}:{utils.Account.account_id}:parametergroup:{cluster_parameter_group_name}'

def redshift_get_cluster_snapshot_arn(cluster_snapshot_arn_params):
    cluster_name = cluster_snapshot_arn_params['ClusterIdentifier']
    snapshot_name = cluster_snapshot_arn_params['SnapshotIdentifier']
    return f'arn:aws:redshift:{utils.Account.region}:{utils.Account.account_id}:snapshot:{cluster_name}/{snapshot_name}'

def redshift_get_cluster_subnet_group_arn(cluster_subnet_group_name):
    return f'arn:aws:redshift:{utils.Account.region}:{utils.Account.account_id}:subnetgroup:{cluster_subnet_group_name}'

def redshift_get_hsm_config_arn(hsm_config_id):
    return f'arn:aws:redshift:{utils.Account.region}:{utils.Account.account_id}:hsmconfiguration:{hsm_config_id}'

def redshift_get_hsm_client_arn(hsm_client_id):
    return f'arn:aws:redshift:{utils.Account.region}:{utils.Account.account_id}:hsmclientcertificate:{hsm_client_id}'

