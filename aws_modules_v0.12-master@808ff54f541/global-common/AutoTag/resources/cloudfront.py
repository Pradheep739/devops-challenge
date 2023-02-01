import boto3
import utils 

def tag_cloudfront():
    cloudfront = boto3.client('cloudfront', region_name=utils.Account.region)
    
    #CloudFront Arns
    cloudfront_arns = get_cloudfront_arns(cloudfront)
    
    #Filtered CloudFront Arns 
    filtered_cloudfront_arns = [] 
    
    #Filter and Tag CloudFront
    for arn in cloudfront_arns:
        cloudfront_updated = False 
        cloudfront_tags = cloudfront.list_tags_for_resource(Resource=arn)['Tags']
        cloudfront_tags_items = cloudfront_tags['Items']
        cloudfront_tags_keys = [cloudfront_tag['Key'] for cloudfront_tag in cloudfront_tags_items] 
        
        default_cloudfront_tags_list = utils.cloudfront_tags['Items']
        
        for default_cloudfront_tag in default_cloudfront_tags_list:
            if default_cloudfront_tag['Key'] not in cloudfront_tags_keys:
                updated_cloudfront_tags = {
                    'Items': [
                        {
                            'Key': default_cloudfront_tag['Key'],
                            'Value': default_cloudfront_tag['Value'] 
                        }
                    ]
                }
                cloudfront.tag_resource(Resource=arn, Tags=updated_cloudfront_tags)
                cloudfront_updated = True 
        if cloudfront_updated: 
            filtered_cloudfront_arns.append(arn)
    
    return filtered_cloudfront_arns

def get_cloudfront_arns(cloudfront):
    cloudfront_arns = [] 
    distribution_response = cloudfront.list_distributions()['DistributionList']
    quantity = distribution_response['Quantity']
    if quantity > 0:
        while 'NextMarker' in distribution_response.keys():
            cloudfront_arns += utils.extract_id(distribution_response, 'Items', 'ARN')
            marker = distribution_response['NextMarker']
            distribution_response = cloudfront.list_distributions(Marker=marker)['DistributionList']
        cloudfront_arns += utils.extract_id(distribution_response, 'Items', 'ARN')
    streaming_response = cloudfront.list_streaming_distributions()['StreamingDistributionList']
    quantity = streaming_response['Quantity']
    if quantity > 0:
        while 'NextMarker' in streaming_response.keys():
            cloudfront_arns += utils.extract_id(streaming_response, 'Items', 'ARN')
            marker = streaming_response['NextMarker']
            streaming_response = cloudfront.list_streaming_distributions(Marker=marker)['StreamingDistributionList']
        cloudfront_arns += utils.extract_id(streaming_response, 'Items', 'ARN')
    return cloudfront_arns