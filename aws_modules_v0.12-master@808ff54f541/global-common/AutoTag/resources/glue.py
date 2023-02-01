import boto3 
import utils 

def tag_glue():
    glue = boto3.client('glue', region_name=utils.Account.region)
    
    #Glue Arns (Crawler, Trigger, Job, DevEndpoint)
    crawler_arns = get_crawler_arns(glue)
    trigger_arns = get_trigger_arns(glue)
    job_arns = get_job_arns(glue)
    dev_endpoint_arns = get_dev_endpoint_arns(glue)
    
    #Filtered Glue Arns
    filtered_glue_arns = [] 
    
    #Filter and Tag Crawlers
    for crawler_arn in crawler_arns: 
        crawler_updated = False 
        crawler_tags = glue.get_tags(ResourceArn=crawler_arn)['Tags']
        crawler_keys = list(crawler_tags.keys())
        for k,v in utils.glue_tags.items():
            if k not in crawler_keys: 
                glue.tag_resource(ResourceArn=crawler_arn, TagsToAdd={k:v})
                crawler_updated = True 
        if crawler_updated:
            filtered_glue_arns.append(crawler_arn)
    
    #Filter and Tag Triggers
    for trigger_arn in trigger_arns: 
        trigger_updated = False 
        trigger_tags = glue.get_tags(ResourceArn=trigger_arn)['Tags']
        trigger_keys = list(trigger_tags.keys())
        for k,v in utils.glue_tags.items():
            if k not in trigger_keys: 
                glue.tag_resource(ResourceArn=trigger_arn, TagsToAdd={k:v})
                trigger_updated = True 
        if trigger_updated:
            filtered_glue_arns.append(trigger_arn)
    
    #Filter and Tag Jobs
    for job_arn in job_arns: 
        job_updated = False 
        job_tags = glue.get_tags(ResourceArn=job_arn)['Tags']
        job_keys = list(job_tags.keys())
        for k,v in utils.glue_tags.items():
            if k not in job_keys: 
                glue.tag_resource(ResourceArn=job_arn, TagsToAdd={k:v})
                job_updated = True 
        if job_updated:
            filtered_glue_arns.append(job_arn)
    
    #Filter and Tag DevEndpoints
    for dev_endpoint_arn in dev_endpoint_arns: 
        dev_endpoint_updated = False 
        dev_endpoint_tags = glue.get_tags(ResourceArn=dev_endpoint_arn)['Tags']
        dev_endpoint_keys = list(dev_endpoint_tags.keys())
        for k,v in utils.glue_tags.items():
            if k not in dev_endpoint_keys: 
                glue.tag_resource(ResourceArn=dev_endpoint_arn, TagsToAdd={k:v})
                dev_endpoint_updated = True 
        if dev_endpoint_updated:
            filtered_glue_arns.append(dev_endpoint_arn)
    
    return filtered_glue_arns 

def get_crawler_arns(glue):
    crawler_names = [] 
    crawler_response = glue.list_crawlers()
    while 'NextToken' in crawler_response.keys():
        crawler_names += crawler_response['CrawlerNames']
        token = crawler_response['NextToken']
        crawler_response = glue.list_crawlers(NextToken=token)
    crawler_names += crawler_response['CrawlerNames']
    crawler_arns = [glue_get_arn('crawler', crawler_name) for crawler_name in crawler_names]
    return crawler_arns

def get_trigger_arns(glue):
    trigger_names = []
    trigger_response = glue.list_triggers()
    while 'NextToken' in trigger_response.keys():
        trigger_names += trigger_response['TriggerNames']
        token = trigger_response['NextToken']
        trigger_response = glue.list_triggers(NextToken=token)
    trigger_names += trigger_response['TriggerNames']
    trigger_arns = [glue_get_arn('trigger', trigger_name) for trigger_name in trigger_names]
    return trigger_arns
    
def get_job_arns(glue):
    job_names = [] 
    job_response = glue.list_jobs()
    while 'NextToken' in job_response.keys():
        job_names += job_response['JobNames']
        token = job_response['NextToken']
        job_response = glue.list_jobs(NextToken=token)
    job_names += job_response['JobNames']
    job_arns = [glue_get_arn('job', job_name) for job_name in job_names]
    return job_arns
    
def get_dev_endpoint_arns(glue):
    dev_endpoint_names = [] 
    dev_endpoint_response = glue.list_dev_endpoints()
    token = dev_endpoint_response['NextToken']
    while token != '':
        dev_endpoint_names += dev_endpoint_response['DevEndpointNames']
        token = dev_endpoint_response['NextToken']
        dev_endpoint_response = glue.list_dev_endpoints(NextToken=token)
    dev_endpoint_names += dev_endpoint_response['DevEndpointNames']
    dev_endpoint_arns = [glue_get_arn('devEndpoint', dev_endpoint_name) for dev_endpoint_name in dev_endpoint_names]
    return dev_endpoint_arns

def glue_get_arn(resource_type, resource_name):
    return f'arn:aws:glue:{utils.Account.region}:{utils.Account.account_id}:{resource_type}/{resource_name}'