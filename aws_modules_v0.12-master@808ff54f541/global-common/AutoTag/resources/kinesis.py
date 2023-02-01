import boto3 
import utils 

def tag_kinesis():
    kinesis = boto3.client('kinesis', region_name=utils.Account.region)
    
    #Kinesis Ids
    kinesis_ids = get_kinesis_stream_names(kinesis)
    
    #Filtered Kinesis Ids 
    filtered_kinesis_ids = []
    
    #Kinesis Tag
    for name in kinesis_ids:
        kinesis_updated = False 
        kinesis_tags_total = []
        kinesis_tags_response = kinesis.list_tags_for_stream(StreamName=name)
        while kinesis_tags_response['HasMoreTags']:
            kinesis_tags = kinesis_tags_response['Tags']
            kinesis_tags_total += kinesis_tags 
            exclusive_start_tag_key = kinesis_tags_total[-1]['Key']
            kinesis_tags_response = kinesis.list_tags_for_stream(StreamName=name, ExclusiveStartTagKey=exclusive_start_tag_key)
        kinesis_tags = kinesis_tags_response['Tags']
        kinesis_tags_total += kinesis_tags 
        kinesis_keys = [kinesis_tag['Key'] for kinesis_tag in kinesis_tags_total]
        for k,v in utils.kinesis_tags.items():
            if k not in kinesis_keys:
                kinesis.add_tags_to_stream(StreamName=name, Tags={k:v})
                kinesis_updated = True 

        if kinesis_updated:
            filtered_kinesis_ids.append(name) 
    
    return filtered_kinesis_ids 
        
def get_kinesis_stream_names(kinesis):
    stream_names = [] 
    stream_response = kinesis.list_streams()
    while stream_response['HasMoreStreams']:
        stream_names += stream_response['StreamNames']
        last_detected_name = stream_names[-1]
        stream_response = kinesis.list_streams(ExclusiveStartStreamName=last_detected_name)
    stream_names += stream_response['StreamNames']
    return stream_names