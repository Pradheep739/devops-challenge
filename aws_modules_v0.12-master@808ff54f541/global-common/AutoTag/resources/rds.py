import boto3 
import utils 

def tag_rds():
    rds = boto3.client('rds', region_name=utils.Account.region)
    
    #RDS Arns 
    rds_arns = get_rds_db_cluster_arns(rds)

    rds_arns += get_rds_db_cluster_snapshot_arns(rds)

    rds_arns += get_rds_db_cluster_parameter_group_arns(rds) 
    
    rds_arns += get_rds_db_instance_arns(rds)

    rds_arns += get_rds_db_parameter_group_arns(rds)

    rds_arns += get_rds_db_security_group_arns(rds)
    
    rds_arns += get_rds_db_snapshot_arns(rds)

    rds_arns += get_rds_db_subnet_group_arns(rds)

    rds_arns += get_rds_event_subcription_arns(rds)

    rds_arns += get_rds_option_group_arns(rds)

    rds_arns += get_rds_reserved_db_instance_arns(rds)
    
    #Filtered RDS Arns 
    filtered_rds_arns = [] 
    
    #RDS Tag
    for arn in rds_arns:
        rds_updated = False 
        rds_tags = rds.list_tags_for_resource(ResourceName=arn)['TagList']
        rds_keys = [rds_tag['Key'] for rds_tag in rds_tags]
        for default_tag in utils.default_tags: 
            if default_tag['Key'] not in rds_keys: 
                rds.add_tags_to_resource(ResourceName=arn, Tags=[default_tag])
                rds_updated = True 
        if rds_updated: 
            filtered_rds_arns.append(arn)
    
    return filtered_rds_arns

def get_rds_db_cluster_arns(rds): 
    rds_arns = [] 
    db_cluster_response = rds.describe_db_clusters()
    while 'Marker' in db_cluster_response.keys():
        rds_arns += utils.extract_id(db_cluster_response, 'DBClusters', 'DBClusterArn')
        marker = db_cluster_response['Marker']
        db_cluster_response = rds.describe_db_clusters(Marker=marker)
    rds_arns += utils.extract_id(db_cluster_response, 'DBClusters', 'DBClusterArn')
    return rds_arns

def get_rds_db_cluster_parameter_group_arns(rds): 
    rds_arns = [] 
    db_cluster_parameter_group_response = rds.describe_db_cluster_parameter_groups()
    while 'Marker' in db_cluster_parameter_group_response.keys():
        rds_arns += utils.extract_id(db_cluster_parameter_group_response, 'DBClusterParameterGroups', 'DBClusterParameterGroupArn')
        marker = db_cluster_parameter_group_response['Marker']
        db_cluster_parameter_group_response = rds.describe_db_cluster_parameter_groups(Marker=marker)
    rds_arns += utils.extract_id(db_cluster_parameter_group_response, 'DBClusterParameterGroups', 'DBClusterParameterGroupArn')
    return rds_arns

def get_rds_db_cluster_snapshot_arns(rds): 
    rds_arns = [] 
    db_cluster_snapshot_response = rds.describe_db_cluster_snapshots()
    while 'Marker' in db_cluster_snapshot_response.keys():
        rds_arns += utils.extract_id(db_cluster_snapshot_response, 'DBClusterSnapshots', 'DBClusterSnapshotArn')
        marker = db_cluster_snapshot_response['Marker']
        db_cluster_snapshot_response = rds.describe_db_cluster_snapshots(Marker=marker)
    rds_arns += utils.extract_id(db_cluster_snapshot_response, 'DBClusterSnapshots', 'DBClusterSnapshotArn')
    return rds_arns

def get_rds_db_instance_arns(rds):
    rds_arns = [] 
    db_instance_response = rds.describe_db_instances()
    while 'Marker' in db_instance_response.keys():
        rds_arns += utils.extract_id(db_instance_response, 'DBInstances', 'DBInstanceArn')
        marker = db_instance_response['Marker']
        db_instance_response = rds.describe_db_instances(Marker=marker)
    rds_arns += utils.extract_id(db_instance_response, 'DBInstances', 'DBInstanceArn')
    return rds_arns

def get_rds_db_parameter_group_arns(rds): 
    rds_arns = [] 
    db_parameter_group_response = rds.describe_db_parameter_groups()
    while 'Marker' in db_parameter_group_response.keys():
        rds_arns += utils.extract_id(db_parameter_group_response, 'DBParameterGroups', 'DBParameterGroupArn')
        marker = db_parameter_group_response['Marker']
        db_parameter_group_response = rds.describe_db_parameter_groups(Marker=marker)
    rds_arns += utils.extract_id(db_parameter_group_response, 'DBParameterGroups', 'DBParameterGroupArn')
    return rds_arns

def get_rds_db_security_group_arns(rds): 
    rds_arns = [] 
    db_security_group_response = rds.describe_db_security_groups()
    while 'Marker' in db_security_group_response.keys():
        rds_arns += utils.extract_id(db_security_group_response, 'DBSecurityGroups', 'DBSecurityGroupArn')
        marker = db_security_group_response['Marker']
        db_security_group_response = rds.describe_db_security_groups(Marker=marker)
    rds_arns += utils.extract_id(db_security_group_response, 'DBSecurityGroups', 'DBSecurityGroupArn')
    return rds_arns

def get_rds_db_snapshot_arns(rds):
    rds_arns = [] 
    db_snapshot_response = rds.describe_db_snapshots()
    while 'Marker' in db_snapshot_response.keys():
        rds_arns += utils.extract_id(db_snapshot_response, 'DBSnapshots', 'DBSnapshotArn')
        marker = db_snapshot_response['Marker']
        db_snapshot_response = rds.describe_db_snapshot(Marker=marker)
    rds_arns += utils.extract_id(db_snapshot_response, 'DBSnapshots', 'DBSnapshotArn')
    return rds_arns

def get_rds_db_subnet_group_arns(rds): 
    rds_arns = [] 
    db_subnet_group_response = rds.describe_db_subnet_groups()
    while 'Marker' in db_subnet_group_response.keys():
        rds_arns += utils.extract_id(db_subnet_group_response, 'DBSubnetGroups', 'DBSubnetGroupArn')
        marker = db_subnet_group_response['Marker']
        db_subnet_group_response = rds.describe_db_subnet_groups(Marker=marker)
    rds_arns += utils.extract_id(db_subnet_group_response, 'DBSubnetGroups', 'DBSubnetGroupArn')
    return rds_arns

def get_rds_event_subcription_arns(rds): 
    rds_arns = [] 
    event_subscription_response = rds.describe_event_subscriptions()
    while 'Marker' in event_subscription_response.keys():
        rds_arns += utils.extract_id(event_subscription_response, 'EventSubscriptionsList', 'EventSubscriptionArn')
        marker = event_subscription_response['Marker']
        event_subscription_response = rds.describe_event_subscriptions(Marker=marker)
    rds_arns += utils.extract_id(event_subscription_response, 'EventSubscriptionsList', 'EventSubscriptionArn')
    return rds_arns 

def get_rds_option_group_arns(rds): 
    rds_arns = [] 
    option_group_response = rds.describe_option_groups()
    while 'Marker' in option_group_response.keys():
        rds_arns += utils.extract_id(option_group_response, 'OptionGroupsList', 'OptionGroupArn')
        marker = option_group_response['Marker']
        option_group_response = rds.describe_option_groups(Marker=marker)
    rds_arns += utils.extract_id(option_group_response, 'OptionGroupsList', 'OptionGroupArn')
    return rds_arns 

def get_rds_reserved_db_instance_arns(rds): 
    rds_arns = [] 
    reserved_db_instance_response = rds.describe_reserved_db_instances()
    while 'Marker' in reserved_db_instance_response.keys():
        rds_arns += utils.extract_id(reserved_db_instance_response, 'ReservedDBInstances', 'ReservedDBInstanceArn')
        marker = reserved_db_instance_response['Marker']
        reserved_db_instance_response = rds.describe_reserved_db_instances(Marker=marker)
    rds_arns += utils.extract_id(reserved_db_instance_response, 'ReservedDBInstances', 'ReservedDBInstanceArn')
    return rds_arns 

