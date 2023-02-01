import boto3
import utils 

def tag_ec2():
    ec2 = boto3.client('ec2', region_name=utils.Account.region)
    
    #EC2 Ids
    ec2_ids = get_ec2_ami_ids(ec2)

    ec2_ids += get_ec2_capacity_reservation_ids(ec2) 

    ec2_ids += get_ec2_client_vpn_endpoint_ids(ec2) 

    ec2_ids += get_ec2_customer_gateway_ids(ec2) 

    ec2_ids += get_ec2_dedicated_host_ids(ec2)

    ec2_ids += get_ec2_dedicated_host_reservation_ids(ec2)

    ec2_ids += get_ec2_dhcp_option_ids(ec2)

    ec2_ids += get_ec2_egress_only_internet_gateway_ids(ec2)

    ec2_ids += get_ec2_eip_ids(ec2)

    ec2_ids += get_ec2_eni_ids(ec2)

    ec2_ids += get_ec2_fleet_ids(ec2)
    
    ec2_instance_ids_and_platforms = get_ec2_instance_ids_and_platforms(ec2)

    ec2_ids += get_ec2_internet_gateway_ids(ec2)

    #ec2_ids += get_ec2_key_pair_ids(ec2)
    
    ec2_ids += get_ec2_launch_template_ids(ec2)

    ec2_ids += get_ec2_local_gateway_ids(ec2)

    ec2_ids += get_ec2_local_gateway_route_table_ids(ec2)

    ec2_ids += get_ec2_local_gateway_virtual_interface_ids(ec2)

    ec2_ids += get_ec2_local_gateway_virtual_interface_group_ids(ec2)

    ec2_ids += get_ec2_local_gateway_route_table_virtual_interface_group_association_ids(ec2)

    ec2_ids += get_ec2_local_gateway_route_table_vpc_association_ids(ec2)

    ec2_ids += get_ec2_nacl_ids(ec2)

    ec2_ids += get_ec2_nat_gateway_ids(ec2)

    #ec2_ids += get_ec2_placement_group_ids(ec2)

    ec2_ids += get_ec2_reserved_instance_ids(ec2) 

    ec2_ids += get_ec2_route_table_ids(ec2) 

    ec2_ids += get_ec2_security_group_ids(ec2)

    ec2_ids += get_ec2_snapshot_ids(ec2)

    ec2_ids += get_ec2_spot_instance_request_ids(ec2)

    ec2_ids += get_ec2_subnet_ids(ec2)

    ec2_ids += get_ec2_traffic_mirror_filter_ids(ec2)

    ec2_ids += get_ec2_traffic_mirror_session_ids(ec2)

    ec2_ids += get_ec2_traffic_mirror_target_ids(ec2)

    ec2_ids += get_ec2_transit_gateway_ids(ec2)

    ec2_ids += get_ec2_transit_gateway_attachment_ids(ec2)

    #ec2_ids += get_ec2_transit_gateway_multicast_domain_ids(ec2)

    ec2_ids += get_ec2_transit_gateway_route_table_ids(ec2)

    ec2_ids += get_ec2_volume_ids(ec2)

    ec2_ids += get_ec2_vpc_ids(ec2)  

    ec2_ids += get_ec2_vpc_endpoint_ids(ec2)

    ec2_ids += get_ec2_vpc_endpoint_service_ids(ec2)

    ec2_ids += get_ec2_vpc_peering_connections(ec2)

    ec2_ids += get_ec2_vpn_connection_ids(ec2) 

    ec2_ids += get_ec2_vpn_gateway_ids(ec2) 
    
    #Filtered EC2 Ids 
    filtered_ec2_ids = [] 
    filtered_ec2_instance_ids = [] 
    
    #Filter and Tag EC2 
    for ec2_id in ec2_ids:
        ec2_updated = False 
        ec2_tags = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [ec2_id]}])['Tags']
        ec2_keys = [ec2_tag['Key'] for ec2_tag in ec2_tags]
        for default_tag in utils.default_tags: 
            if default_tag['Key'] not in ec2_keys: 
                try:
                    ec2.create_tags(Resources=[ec2_id], Tags=[default_tag])
                    ec2_updated = True
                except Exception as e:
                    print(e)
        if ec2_updated: 
            filtered_ec2_ids.append(ec2_id)
    
    #EC2 Instance Tag
    try: 
        for ec2_instance_id_and_platform in ec2_instance_ids_and_platforms:
            ec2_instance_updated = False 
            ec2_instance_id = ec2_instance_id_and_platform[0]
            ec2_instance_platform = ec2_instance_id_and_platform[1]
            ec2_instance_tags = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [ec2_instance_id]}])['Tags']
            ec2_instance_keys = [ec2_instance_tag['Key'] for ec2_instance_tag in ec2_instance_tags]
            for default_tag in utils.default_tags: 
                if default_tag['Key'] not in ec2_instance_keys: 
                    ec2.create_tags(Resources=[ec2_instance_id], Tags=[default_tag])
                    ec2_instance_updated = True 
            #EC2 Owner Tagging
            if 'Owner' not in ec2_instance_keys:
                owner_tag = {} 
                owner_tag['Key'] = 'InstanceOwner'
                owner_tag['Value'] = 'root'
                ec2.create_tags(Resources=[ec2_instance_id], Tags=[owner_tag])
                ec2_instance_updated = True 
            #EC2 OS Tagging
            if 'OSTYPE' not in ec2_instance_keys:
                os_tag = {} 
                os_tag['Key'] = 'OSTYPE'
                os_tag['Value'] = ec2_instance_platform
                ec2.create_tags(Resources=[ec2_instance_id], Tags=[os_tag])
                ec2_instance_updated = True 
            if ec2_instance_updated: 
                filtered_ec2_instance_ids.append(ec2_instance_id)
    except Exception as e:
        print("Exception while tagging EC2 Instances during creation: " + str(e))
    
    return filtered_ec2_instance_ids + filtered_ec2_ids 

def get_ec2_ami_ids(ec2):
    ec2_ids = [] 
    images_response = ec2.describe_images(Owners=['self'])
    ec2_ids += utils.extract_id(images_response, 'Images', 'ImageId')
    return ec2_ids 

def get_ec2_capacity_reservation_ids(ec2):
    ec2_ids = [] 
    capacity_reservations_response = ec2.describe_capacity_reservations()
    while 'NextToken' in capacity_reservations_response.keys():
        ec2_ids += utils.extract_id(capacity_reservations_response, 'CapacityReservations', 'CapacityReservationId')
        token = capacity_reservations_response['NextToken']
        capacity_reservations_response = ec2.describe_capacity_reservations(NextToken=token)
    ec2_ids += utils.extract_id(capacity_reservations_response, 'CapacityReservations', 'CapacityReservationId')
    return ec2_ids 

def get_ec2_client_vpn_endpoint_ids(ec2):
    ec2_ids = [] 
    client_vpn_endpoint_response = ec2.describe_client_vpn_endpoints()
    while 'NextToken' in client_vpn_endpoint_response.keys():
        ec2_ids += utils.extract_id(client_vpn_endpoint_response, 'ClientVpnEndpoints', 'ClientVpnEndpointId')
        token = client_vpn_endpoint_response['NextToken']
        client_vpn_endpoint_response = ec2.describe_client_vpn_endpoints(NextToken=token)
    ec2_ids += utils.extract_id(client_vpn_endpoint_response, 'ClientVpnEndpoints', 'ClientVpnEndpointId')
    return ec2_ids

def get_ec2_customer_gateway_ids(ec2):
    ec2_ids = [] 
    customer_gateway_response = ec2.describe_customer_gateways()
    ec2_ids += utils.extract_id(customer_gateway_response, 'CustomerGateways', 'CustomerGatewayId')
    return ec2_ids 

def get_ec2_dedicated_host_ids(ec2):
    ec2_ids = [] 
    host_response = ec2.describe_hosts()
    while 'NextToken' in host_response.keys():
        ec2_ids += utils.extract_id(host_response, 'Hosts', 'HostId')
        token = host_response['NextToken']
        host_response = ec2.describe_hosts(NextToken=token)
    ec2_ids += utils.extract_id(host_response, 'Hosts', 'HostId')
    return ec2_ids 

def get_ec2_dedicated_host_reservation_ids(ec2):
    ec2_ids = [] 
    host_reservation_response = ec2.describe_host_reservations()
    while 'NextToken' in host_reservation_response.keys():
        ec2_ids += utils.extract_id(host_reservation_response, 'HostReservationSet', 'HostReservationId')
        token = host_reservation_response['NextToken']
        host_reservation_response = ec2.describe_host_reservations(NextToken=token)
    ec2_ids += utils.extract_id(host_reservation_response, 'HostReservationSet', 'HostReservationId')
    return ec2_ids 

def get_ec2_dhcp_option_ids(ec2):
    ec2_ids = [] 
    dhcp_options_response = ec2.describe_dhcp_options(MaxResults=1000)
    while 'NextToken' in dhcp_options_response.keys():
        ec2_ids += utils.extract_id(dhcp_options_response, 'DhcpOptions', 'DhcpOptionsId')
        token = dhcp_options_response['NextToken']
        dhcp_options_response = ec2.describe_dhcp_options(NextToken=token)
    ec2_ids += utils.extract_id(dhcp_options_response, 'DhcpOptions', 'DhcpOptionsId')
    return ec2_ids 

def get_ec2_egress_only_internet_gateway_ids(ec2):
    ec2_ids = []
    egress_only_internet_gateway_response = ec2.describe_egress_only_internet_gateways()
    while 'NextToken' in egress_only_internet_gateway_response.keys():
        ec2_ids += utils.extract_id(egress_only_internet_gateway_response, 'EgressOnlyInternetGateways', 'EgressOnlyInternetGatewayId')
        token = egress_only_internet_gateway_response['NextToken']
        egress_only_internet_gateway_response = ec2.describe_egress_only_internet_gateways(NextToken=token)
    ec2_ids += utils.extract_id(egress_only_internet_gateway_response, 'EgressOnlyInternetGateways', 'EgressOnlyInternetGatewayId')
    return ec2_ids 

def get_ec2_eip_ids(ec2):
    ec2_ids = [] 
    eip_response = ec2.describe_addresses()
    ec2_ids += utils.extract_id(eip_response, 'Addresses', 'AllocationId')
    return ec2_ids 

def get_ec2_eni_ids(ec2):
    ec2_ids = [] 
    eni_response = ec2.describe_network_interfaces()
    while 'NextToken' in eni_response.keys():
        ec2_ids += utils.extract_id(eni_response, 'NetworkInterfaces', 'NetworkInterfaceId')
        token = eni_response['NextToken']
        eni_response = ec2.describe_network_interfaces(NextToken=token)
    ec2_ids += utils.extract_id(eni_response, 'NetworkInterfaces', 'NetworkInterfaceId')
    return ec2_ids 

def get_ec2_fleet_ids(ec2):
    ec2_ids = [] 
    fleet_response = ec2.describe_fleets()
    while 'NextToken' in fleet_response.keys():
        ec2_ids += utils.extract_id(fleet_response, 'Fleets', 'FleetId')
        token = fleet_response['NextToken']
        fleet_response = ec2.describe_fleets(NextToken=token)
    ec2_ids += utils.extract_id(fleet_response, 'Fleets', 'FleetId')
    return ec2_ids 

def get_ec2_instance_ids_and_platforms(ec2):
    ec2_ids = [] 
    instances_response = ec2.describe_instances()
    instance_reservations = instances_response['Reservations']
    while 'NextToken' in instances_response.keys():
        for reservation in instance_reservations:
            instances = reservation['Instances']
            for instance in instances:
                instance_id_and_platform = []
                instance_id_and_platform.append(instance['InstanceId'])
                if 'Platform' in instance.keys():
                    instance_id_and_platform.append(instance['Platform'].upper())
                else:
                    instance_id_and_platform.append('LINUX')
                ec2_ids.append(instance_id_and_platform)
        token = instances_response['NextToken']
        instances_response = ec2.describe_instances(NextToken=token)
        instance_reservations = instances_response['Reservations']
    
    for reservation in instance_reservations:
        instances = reservation['Instances']
        for instance in instances:
            instance_id_and_platform = []
            instance_id_and_platform.append(instance['InstanceId'])
            if 'Platform' in instance.keys():
                instance_id_and_platform.append(instance['Platform'].upper())
            else:
                instance_id_and_platform.append('LINUX')
            ec2_ids.append(instance_id_and_platform)
    return ec2_ids 

def get_ec2_internet_gateway_ids(ec2):
    ec2_ids = [] 
    igw_response = ec2.describe_internet_gateways()
    while 'NextToken' in igw_response.keys():
        ec2_ids += utils.extract_id(igw_response, 'InternetGateways', 'InternetGatewayId')
        token = igw_response['NextToken']
        igw_response = ec2.describe_internet_gateways(NextToken=token)
    ec2_ids += utils.extract_id(igw_response, 'InternetGateways', 'InternetGatewayId')
    return ec2_ids 

def get_ec2_key_pair_ids(ec2):
    ec2_ids = [] 
    key_pair_response = ec2.describe_key_pairs()
    ec2_ids += utils.extract_id(key_pair_response, 'KeyPairs', 'KeyName')
    return ec2_ids 

def get_ec2_launch_template_ids(ec2):
    ec2_ids = [] 
    launch_templates_response = ec2.describe_launch_templates()
    while 'NextToken' in launch_templates_response.keys():
        ec2_ids += utils.extract_id(launch_templates_response, 'LaunchTemplates', 'LaunchTemplateId')
        token = launch_templates_response['NextToken']
        launch_templates_response = ec2.describe_launch_templates(NextToken=token)
    ec2_ids += utils.extract_id(launch_templates_response, 'LaunchTemplates', 'LaunchTemplateId')
    return ec2_ids 

def get_ec2_local_gateway_ids(ec2):
    ec2_ids = [] 
    local_gateway_response = ec2.describe_local_gateways()
    while 'NextToken' in local_gateway_response.keys():
        ec2_ids += utils.extract_id(local_gateway_response, 'LocalGateways', 'LocalGatewayId')
        token = local_gateway_response['NextToken']
        local_gateway_response = ec2.describe_local_gateways(NextToken=token)
    ec2_ids += utils.extract_id(local_gateway_response, 'LocalGateways', 'LocalGatewayId')
    return ec2_ids 

def get_ec2_local_gateway_route_table_ids(ec2):
    ec2_ids = [] 
    local_gateway_route_table_response = ec2.describe_local_gateway_route_tables()
    while 'NextToken' in local_gateway_route_table_response.keys():
        ec2_ids += utils.extract_id(local_gateway_route_table_response, 'LocalGatewayRouteTables', 'LocalGatewayRouteTableId')
        token = local_gateway_route_table_response['NextToken']
        local_gateway_route_table_response = ec2.describe_local_gateway_route_tables(NextToken=token)
    ec2_ids += utils.extract_id(local_gateway_route_table_response, 'LocalGatewayRouteTables', 'LocalGatewayRouteTableId')
    return ec2_ids 

def get_ec2_local_gateway_virtual_interface_ids(ec2):
    ec2_ids = [] 
    local_gateway_virtual_interface_response = ec2.describe_local_gateway_virtual_interfaces()
    while 'NextToken' in local_gateway_virtual_interface_response.keys():
        ec2_ids += utils.extract_id(local_gateway_virtual_interface_response, 'LocalGatewayVirtualInterfaces', 'LocalGatewayVirtualInterfaceId')
        token = local_gateway_virtual_interface_response['NextToken']
        local_gateway_virtual_interface_response = ec2.describe_local_gateway_virtual_interfaces(NextToken=token)
    ec2_ids += utils.extract_id(local_gateway_virtual_interface_response, 'LocalGatewayVirtualInterfaces', 'LocalGatewayVirtualInterfaceId')
    return ec2_ids 

def get_ec2_local_gateway_virtual_interface_group_ids(ec2):
    ec2_ids = [] 
    local_gateway_virtual_interface_group_response = ec2.describe_local_gateway_virtual_interface_groups()
    while 'NextToken' in local_gateway_virtual_interface_group_response.keys():
        ec2_ids += utils.extract_id(local_gateway_virtual_interface_group_response, 'LocalGatewayVirtualInterfaceGroups', 'LocalGatewayVirtualInterfaceGroupId')
        token = local_gateway_virtual_interface_group_response['NextToken']
        local_gateway_virtual_interface_group_response = ec2.describe_local_gateway_virtual_interface_groups(NextToken=token)
    ec2_ids += utils.extract_id(local_gateway_virtual_interface_group_response, 'LocalGatewayVirtualInterfaceGroups', 'LocalGatewayVirtualInterfaceGroupId')
    return ec2_ids 

def get_ec2_local_gateway_route_table_virtual_interface_group_association_ids(ec2):
    ec2_ids = [] 
    local_gateway_route_table_virtual_interface_group_association_response = ec2.describe_local_gateway_route_table_virtual_interface_group_associations()
    while 'NextToken' in local_gateway_route_table_virtual_interface_group_association_response.keys():
        ec2_ids += utils.extract_id(local_gateway_route_table_virtual_interface_group_association_response, 'LocalGatewayRouteTableVirtualInterfaceGroupAssociations', 'LocalGatewayRouteTableVirtualInterfaceGroupAssociationId')
        token = local_gateway_route_table_virtual_interface_group_association_response['NextToken']
        local_gateway_route_table_virtual_interface_group_association_response = ec2.describe_local_gateway_route_table_virtual_interface_group_associations(NextToken=token)
    ec2_ids += utils.extract_id(local_gateway_route_table_virtual_interface_group_association_response, 'LocalGatewayRouteTableVirtualInterfaceGroupAssociations', 'LocalGatewayRouteTableVirtualInterfaceGroupAssociationId')
    return ec2_ids 

def get_ec2_local_gateway_route_table_vpc_association_ids(ec2):
    ec2_ids = [] 
    local_gateway_route_table_vpc_association_response = ec2.describe_local_gateway_route_table_vpc_associations()
    while 'NextToken' in local_gateway_route_table_vpc_association_response.keys():
        ec2_ids += utils.extract_id(local_gateway_route_table_vpc_association_response, 'LocalGatewayRouteTableVpcAssociations', 'LocalGatewayRouteTableVpcAssociationId')
        token = local_gateway_route_table_vpc_association_response['NextToken']
        local_gateway_route_table_vpc_association_response = ec2.describe_local_gateway_route_table_vpc_associations(NextToken=token)
    ec2_ids += utils.extract_id(local_gateway_route_table_vpc_association_response, 'LocalGatewayRouteTableVpcAssociations', 'LocalGatewayRouteTableVpcAssociationId')
    return ec2_ids 

def get_ec2_nacl_ids(ec2):
    ec2_ids = [] 
    nacl_response = ec2.describe_network_acls()
    while 'NextToken' in nacl_response.keys():
        ec2_ids += utils.extract_id(nacl_response, 'NetworkAcls', 'NetworkAclId')
        token = nacl_response['NextToken']
        nacl_response = ec2.describe_network_acls(NextToken=token)
    ec2_ids += utils.extract_id(nacl_response, 'NetworkAcls', 'NetworkAclId')
    return ec2_ids 

def get_ec2_nat_gateway_ids(ec2):
    ec2_ids = [] 
    nat_response = ec2.describe_nat_gateways()
    while 'NextToken' in nat_response.keys():
        ec2_ids += utils.extract_id(nat_response, 'NatGateways', 'NatGatewayId')
        token = nat_response['NextToken']
        nat_response = ec2.describe_nat_gateways(NextToken=token)
    ec2_ids += utils.extract_id(nat_response, 'NatGateways', 'NatGatewayId')
    return ec2_ids 

def get_ec2_placement_group_ids(ec2):
    ec2_ids = [] 
    placement_group_response = ec2.describe_placement_groups()
    ec2_ids += utils.extract_id(placement_group_response, 'PlacementGroups', 'GroupId')
    return ec2_ids 

def get_ec2_reserved_instance_ids(ec2):
    ec2_ids = [] 
    reserved_instances_response = ec2.describe_reserved_instances()
    ec2_ids += utils.extract_id(reserved_instances_response, 'ReservedInstances', 'ReservedInstancesId')
    return ec2_ids 

def get_ec2_route_table_ids(ec2):
    ec2_ids = [] 
    route_table_response = ec2.describe_route_tables()
    while 'NextToken' in route_table_response.keys():
        ec2_ids += utils.extract_id(route_table_response, 'RouteTables', 'RouteTableId')
        token = route_table_response['NextToken']
        route_table_response = ec2.describe_route_tables(NextToken=token)
    ec2_ids += utils.extract_id(route_table_response, 'RouteTables', 'RouteTableId')
    return ec2_ids 

def get_ec2_security_group_ids(ec2):
    ec2_ids = [] 
    securitygroups_response = ec2.describe_security_groups()
    while 'NextToken' in securitygroups_response.keys():
        ec2_ids += utils.extract_id(securitygroups_response, 'SecurityGroups', 'GroupId')
        token = securitygroups_response['NextToken']
        securitygroups_response = ec2.describe_security_groups(NextToken=token)
    ec2_ids += utils.extract_id(securitygroups_response, 'SecurityGroups', 'GroupId')
    return ec2_ids 

def get_ec2_snapshot_ids(ec2):
    ec2_ids = [] 
    snapshots_response = ec2.describe_snapshots(OwnerIds =['self'])
    while 'NextToken' in snapshots_response.keys():
        ec2_ids += utils.extract_id(snapshots_response, 'Snapshots', 'SnapshotId')
        token = images_response['NextToken']
        snapshots_response = ec2.describe_snapshots(OwnerIds =['self'])
    ec2_ids += utils.extract_id(snapshots_response, 'Snapshots', 'SnapshotId')
    return ec2_ids 

def get_ec2_spot_instance_request_ids(ec2):
    ec2_ids = [] 
    spot_instance_requests_response = ec2.describe_spot_instance_requests()
    while 'NextToken' in spot_instance_requests_response.keys():
        ec2_ids += utils.extract_id(spot_instance_requests_response, 'SpotInstanceRequests', 'SpotInstanceRequestId')
        token = spot_instance_requests_response['NextToken']
        spot_instance_requests_response = ec2.describe_spot_instance_requests(NextToken=token)
    ec2_ids += utils.extract_id(spot_instance_requests_response, 'SpotInstanceRequests', 'SpotInstanceRequestId')
    return ec2_ids 

def get_ec2_subnet_ids(ec2):
    ec2_ids = [] 
    subnet_response = ec2.describe_subnets()
    while 'NextToken' in subnet_response.keys():
        ec2_ids += utils.extract_id(subnet_response, 'Subnets', 'SubnetId')
        token = subnet_response['NextToken']
        subnet_response = ec2.describe_subnets(NextToken=token)
    ec2_ids += utils.extract_id(subnet_response, 'Subnets', 'SubnetId')
    return ec2_ids 

def get_ec2_traffic_mirror_filter_ids(ec2):
    ec2_ids = [] 
    tm_filter_response = ec2.describe_traffic_mirror_filters()
    while 'NextToken' in tm_filter_response.keys():
        ec2_ids += utils.extract_id(tm_filter_response, 'TrafficMirrorFilters', 'TrafficMirrorFilterId')
        token = tm_filter_response['NextToken']
        tm_filter_response = ec2.describe_traffic_mirror_filters(NextToken=token)
    ec2_ids += utils.extract_id(tm_filter_response, 'TrafficMirrorFilters', 'TrafficMirrorFilterId')
    return ec2_ids 

def get_ec2_traffic_mirror_session_ids(ec2):
    ec2_ids = [] 
    tm_session_response = ec2.describe_traffic_mirror_sessions()
    while 'NextToken' in tm_session_response.keys():
        ec2_ids += utils.extract_id(tm_session_response, 'TrafficMirrorSessions', 'TrafficMirrorSessionId')
        token = tm_session_response['NextToken']
        tm_session_response = ec2.describe_traffic_mirror_sessions(NextToken=token)
    ec2_ids += utils.extract_id(tm_session_response, 'TrafficMirrorSessions', 'TrafficMirrorSessionId')
    return ec2_ids 

def get_ec2_traffic_mirror_target_ids(ec2):
    ec2_ids = [] 
    tm_target_response = ec2.describe_traffic_mirror_targets()
    while 'NextToken' in tm_target_response.keys():
        ec2_ids += utils.extract_id(tm_target_response, 'TrafficMirrorTargets', 'TrafficMirrorTargetId')
        token = tm_target_response['NextToken']
        tm_target_response = ec2.describe_traffic_mirror_targets(NextToken=token)
    ec2_ids += utils.extract_id(tm_target_response, 'TrafficMirrorTargets', 'TrafficMirrorTargetId')
    return ec2_ids 

def get_ec2_transit_gateway_ids(ec2):
    ec2_ids = [] 
    transit_gateway_response = ec2.describe_transit_gateways()
    while 'NextToken' in transit_gateway_response.keys():
        ec2_ids += utils.extract_id(transit_gateway_response, 'TransitGateways', 'TransitGatewayId')
        token = transit_gateway_response['NextToken']
        transit_gateway_response = ec2.describe_transit_gateways(NextToken=token)
    ec2_ids += utils.extract_id(transit_gateway_response, 'TransitGateways', 'TransitGatewayId')
    return ec2_ids 

def get_ec2_transit_gateway_attachment_ids(ec2):
    ec2_ids = [] 
    transit_gateway_attachment_response = ec2.describe_transit_gateway_attachments()
    while 'NextToken' in transit_gateway_attachment_response.keys():
        ec2_ids += utils.extract_id(transit_gateway_attachment_response, 'TransitGatewayAttachments', 'TransitGatewayAttachmentId')
        token = transit_gateway_attachment_response['NextToken']
        transit_gateway_attachment_response = ec2.describe_transit_gateway_attachments(NextToken=token)
    ec2_ids += utils.extract_id(transit_gateway_attachment_response, 'TransitGatewayAttachments', 'TransitGatewayAttachmentId')
    return ec2_ids 

def get_ec2_transit_gateway_multicast_domain_ids(ec2):
    ec2_ids = [] 
    transit_gateway_multicast_response = ec2.describe_transit_gateway_multicast_domains()
    while 'NextToken' in transit_gateway_multicast_response.keys():
        ec2_ids += utils.extract_id(transit_gateway_multicast_response, 'TransitGatewayMulticastDomains', 'TransitGatewayMulticastDomainId')
        token = transit_gateway_multicast_response['NextToken']
        transit_gateway_multicast_response = ec2.describe_transit_gateway_multicast_domains(NextToken=token)
    ec2_ids += utils.extract_id(transit_gateway_multicast_response, 'TransitGatewayMulticastDomains', 'TransitGatewayMulticastDomainId')
    return ec2_ids 

def get_ec2_transit_gateway_route_table_ids(ec2):
    ec2_ids = [] 
    transit_gateway_route_table_response = ec2.describe_transit_gateway_route_tables()
    while 'NextToken' in transit_gateway_route_table_response.keys():
        ec2_ids += utils.extract_id(transit_gateway_route_table_response, 'TransitGatewayRouteTables', 'TransitGatewayRouteTableId')
        token = transit_gateway_route_table_response['NextToken']
        transit_gateway_route_table_response = ec2.describe_transit_gateway_route_tables(NextToken=token)
    ec2_ids += utils.extract_id(transit_gateway_route_table_response, 'TransitGatewayRouteTables', 'TransitGatewayRouteTableId')
    return ec2_ids 

def get_ec2_volume_ids(ec2):
    ec2_ids = [] 
    volume_response = ec2.describe_volumes()
    while 'NextToken' in volume_response.keys():
        ec2_ids += utils.extract_id(volume_response, 'Volumes', 'VolumeId')
        token = volume_response['NextToken']
        volume_response = ec2.describe_volumes(NextToken=token)
    ec2_ids += utils.extract_id(volume_response, 'Volumes', 'VolumeId')
    return ec2_ids 

def get_ec2_vpc_ids(ec2):
    ec2_ids = [] 
    vpc_response = ec2.describe_vpcs()
    while 'NextToken' in vpc_response.keys():
        ec2_ids += utils.extract_id(vpc_response, 'Vpcs', 'VpcId')
        token = vpc_response['NextToken']
        vpc_response = ec2.describe_vpcs(NextToken=token)
    ec2_ids += utils.extract_id(vpc_response, 'Vpcs', 'VpcId')
    return ec2_ids 

def get_ec2_vpc_endpoint_ids(ec2):
    ec2_ids = [] 
    endpoints_response = ec2.describe_vpc_endpoints()
    while 'NextToken' in endpoints_response.keys():
        ec2_ids += utils.extract_id(endpoints_response, 'VpcEndpoints', 'VpcEndpointId')
        token = endpoints_response['NextToken']
        endpoints_response = ec2.describe_vpc_endpoints(NextToken=token)
    ec2_ids += utils.extract_id(endpoints_response, 'VpcEndpoints', 'VpcEndpointId')
    return ec2_ids 

def get_ec2_vpc_endpoint_service_ids(ec2):
    ec2_ids = [] 
    endpoint_services_response = ec2.describe_vpc_endpoint_services()
    while 'NextToken' in endpoint_services_response.keys():
        endpoint_services = endpoint_services_response['ServiceDetails']
        for endpoint_service in endpoint_services:
            if endpoint_service['Owner'] == utils.Account.account_id:
                ec2_ids.append(endpoint_service['ServiceId'])
        token = endpoint_services_response['NextToken']
        endpoint_services_response = ec2.describe_vpc_endpoint_services(NextToken=token)
    endpoint_services = endpoint_services_response['ServiceDetails']
    for endpoint_service in endpoint_services:
        if endpoint_service['Owner'] == utils.Account.account_id:
            ec2_ids.append(endpoint_service['ServiceId'])
    return ec2_ids 

def get_ec2_vpc_peering_connections(ec2):
    ec2_ids = [] 
    peering_response = ec2.describe_vpc_peering_connections()
    while 'NextToken' in peering_response.keys():
        ec2_ids += utils.extract_id(peering_response, 'VpcPeeringConnections', 'VpcPeeringConnectionId')
        token = peering_response['NextToken']
        peering_response = ec2.describe_vpc_peering_connections(NextToken=token)
    ec2_ids += utils.extract_id(peering_response, 'VpcPeeringConnections', 'VpcPeeringConnectionId')
    return ec2_ids 

def get_ec2_vpn_connection_ids(ec2):
    ec2_ids = []
    vpn_connection_response = ec2.describe_vpn_connections()
    ec2_ids += utils.extract_id(vpn_connection_response, 'VpnConnections', 'VpnConnectionId')
    return ec2_ids 

def get_ec2_vpn_gateway_ids(ec2):
    ec2_ids = [] 
    vpn_response = ec2.describe_vpn_gateways()
    ec2_ids += utils.extract_id(vpn_response, 'VpnGateways', 'VpnGatewayId')
    return ec2_ids 
