import boto3
import utils

def tag_efs():
    efs = boto3.client('efs', region_name=utils.Account.region)
    
    #EFS Ids
    efs_ids = get_efs_file_system_ids(efs)
    
    #Filtered EFS Ids 
    filtered_efs_ids = [] 
    
    #Filter and Tag EFS 
    for efs_id in efs_ids:
        efs_updated = False 
        efs_tags = efs.describe_tags(FileSystemId=efs_id)['Tags']
        efs_keys = [efs_tag['Key'] for efs_tag in efs_tags]
        for default_tag in utils.default_tags: 
            if default_tag['Key'] not in efs_keys: 
                efs.create_tags(FileSystemId=efs_id, Tags=[default_tag])
                efs_updated = True 
        if efs_updated: 
            filtered_efs_ids.append(efs_id)
    
    return filtered_efs_ids

def get_efs_file_system_ids(efs):
    efs_ids = [] 
    fs_response = efs.describe_file_systems()
    while 'NextMarker' in fs_response.keys():
        efs_ids += utils.extract_id(fs_response, 'FileSystems', 'FileSystemId')
        marker = fs_response['NextMarker']
        fs_response = efs.describe_file_systems(Marker=marker)
    efs_ids += utils.extract_id(fs_response, 'FileSystems', 'FileSystemId')
    return efs_ids 