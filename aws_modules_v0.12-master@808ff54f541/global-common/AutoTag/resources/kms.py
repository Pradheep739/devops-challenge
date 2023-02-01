import boto3 
import utils 

def tag_kms():
    kms = boto3.client('kms', region_name=utils.Account.region)
    
    #KMS Ids, Extract CMKs only  
    kms_ids = get_kms_ids(kms)
    
    #Filtered KMS Ids
    filtered_kms_ids = [] 
    
    #Filter and Tag KMS
    for kms_id in kms_ids:
        kms_updated = False 
        kms_tags = kms.list_resource_tags(KeyId=kms_id)['Tags']
        kms_keys = [kms_tag['TagKey'] for kms_tag in kms_tags]
        for kms_default_tag in utils.kms_tags: 
            if kms_default_tag['TagKey'] not in kms_keys: 
                kms.tag_resource(KeyId=kms_id, Tags=[kms_default_tag])
                kms_updated = True 
        if kms_updated:
            filtered_kms_ids.append(kms_id)
    return filtered_kms_ids 

def get_kms_ids(kms):
    kms_ids = [] 
    kms_response = kms.list_keys()
    while kms_response['Truncated']:
        kms_ids_all = utils.extract_id(kms_response, 'Keys', 'KeyId')
        for id in kms_ids_all:
            kms_key_response = kms.describe_key(KeyId=id)
            key_manager = kms_key_response['KeyMetadata']['KeyManager']
            key_state = kms_key_response['KeyMetadata']['KeyState']
            if key_manager == 'CUSTOMER' and (key_state == 'Enabled' or key_state == 'Disabled'):
                kms_ids.append(id)
        marker = kms_response['NextMarker']
        kms_response = kms.list_keys(Marker=marker)
    kms_ids_all = utils.extract_id(kms_response, 'Keys', 'KeyId')
    for id in kms_ids_all:
        kms_key_response = kms.describe_key(KeyId=id)
        key_manager = kms_key_response['KeyMetadata']['KeyManager']
        key_state = kms_key_response['KeyMetadata']['KeyState']
        if key_manager == 'CUSTOMER' and (key_state == 'Enabled' or key_state == 'Disabled'):
            kms_ids.append(id)
    return kms_ids 