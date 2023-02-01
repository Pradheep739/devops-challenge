import boto3 
import utils 

def tag_sqs():
    sqs = boto3.client('sqs', region_name=utils.Account.region)
    
    #SQS Ids
    sqs_urls = get_sqs_urls(sqs)
    
    #Filtered SQS Ids 
    filtered_sqs_urls = [] 
    
    #SQS Tag
    for url in sqs_urls:
        sqs_updated = False 
        sqs_tags_response = sqs.list_queue_tags(QueueUrl=url)
        if 'Tags' in sqs_tags_response.keys():
            sqs_tags = sqs_tags_response['Tags']
            sqs_keys = list(sqs_tags.keys())
            for k,v in utils.sqs_tags.items():
                if k not in sqs_keys: 
                    sqs.tag_queue(QueueUrl=url, Tags={k:v})
                    sqs_updated = True 
        else: 
            sqs.tag_queue(QueueUrl=url, Tags=utils.sqs_tags)
            sqs_upated = True 
        if sqs_updated: 
            filtered_sqs_urls.append(url)
                
    return filtered_sqs_urls

def get_sqs_urls(sqs):
    sqs_urls = [] 
    if 'QueueUrls' in sqs.list_queues().keys():
        sqs_urls = sqs.list_queues()['QueueUrls']
    return sqs_urls 