import boto3 
import utils
def tag_s3():
    s3 = boto3.client('s3', region_name=utils.Account.region)
    #S3 Bucket Names 
    s3_names = get_s3_bucket_names(s3)
    #Filtered S3 Bucket Names 
    filtered_s3_names = [] 
    #S3 Tag
    for name in s3_names:
        s3_updated = False 
        try: 
            s3_tags = s3.get_bucket_tagging(Bucket=name)['TagSet']
            s3_tags_map = {}
            for s3_tag in s3_tags:
                s3_tags_map[s3_tag['Key']] = s3_tag['Value']
            s3_keys = [s3_tag['Key'] for s3_tag in s3_tags]
            default_s3_tags_list = utils.s3_tags['TagSet']
            updated_s3_tag_set = [] 
            #Add default tags to updated tagset that are not present in existing s3 tags 
            for default_s3_tag in default_s3_tags_list: 
                if default_s3_tag['Key'] not in s3_keys: 
                    updated_s3_tag_set.append(default_s3_tag)
                    s3_updated = True
                else:
                    existing_key = default_s3_tag['Key']
                    existing_value = s3_tags_map[existing_key]
                    updated_s3_tag_set.append({'Key': existing_key, 'Value': existing_value})
            #Collect list of keys in updated_s3_tag_set
            updated_s3_tag_keys = [updated_s3_tag['Key'] for updated_s3_tag in updated_s3_tag_set]
            #Add existing tags that are not present in updated tagset 
            for existing_key,existing_value in s3_tags_map.items(): 
                if existing_key not in updated_s3_tag_keys:
                    updated_s3_tag_set.append({'Key': existing_key, 'Value': existing_value})
            formatted_s3_tag_set = {'TagSet': updated_s3_tag_set}
            s3.put_bucket_tagging(Bucket=name, Tagging=formatted_s3_tag_set)
        except Exception as e: 
            if 'NoSuchTagSet' in str(e): 
                s3.put_bucket_tagging(Bucket=name, Tagging=utils.s3_tags)
                s3_updated = True 
            else:
                print(e)
        if s3_updated: 
            filtered_s3_names.append(name) 
    return filtered_s3_names 
def get_s3_bucket_names(s3):
    buckets_response = s3.list_buckets()
    s3_names = utils.extract_id(buckets_response, 'Buckets', 'Name')
    return s3_names
