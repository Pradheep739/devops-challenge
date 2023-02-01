'''
Tagging of Critical Resources periodically with default tags 
After tagging actions are completed, this function will log statistics of resources with updated tags 
(resource IDs/ARNs, number of resources updated for each resource type, and total number of resources updated)
'''

import boto3 
import utils 
from resources import apigateway, apigatewayv2, autoscaling, cloudfront, cloudwatch, dynamodb, ec2, ecr, \
    ecs, efs, eks, elb, glue, kinesis, kms, lambdas, rds, redshift, s3, sns, sqs, waf

def tag_all():
    apigateway_ids = apigateway.tag_apigateway() 
    apigatewayv2_ids = apigatewayv2.tag_apigatewayv2() 
    autoscaling_ids = autoscaling.tag_autoscaling() 
    cloudfront_ids = cloudfront.tag_cloudfront() 
    cloudwatch_ids = cloudwatch.tag_cloudwatch()  
    dynamodb_ids = dynamodb.tag_dynamodb() 
    ec2_ids = ec2.tag_ec2() 
    ecr_ids = ecr.tag_ecr() 
    ecs_ids = ecs.tag_ecs() 
    efs_ids = efs.tag_efs()  
    eks_ids = eks.tag_eks() 
    elb_ids = elb.tag_elb()  
    elbv2_ids = elb.tag_elbv2() 
    glue_ids = glue.tag_glue()
    kinesis_ids = kinesis.tag_kinesis()
    kms_ids = kms.tag_kms()
    lambda_ids = lambdas.tag_lambdas()
    rds_ids = rds.tag_rds()
    redshift_ids = redshift.tag_redshift()
    s3_ids = s3.tag_s3()
    sns_ids = sns.tag_sns()
    sqs_ids = sqs.tag_sqs()
    waf_ids = waf.tag_waf()
    wafv2_ids = waf.tag_wafv2()
    
    resource_statistics = {'APIGateway': apigateway_ids, 'APIGatewayV2': apigatewayv2_ids, \
        'Autoscaling Group': autoscaling_ids, 'CloudFront': cloudfront_ids, 'CloudWatch': cloudwatch_ids, \
        'DynamoDB': dynamodb_ids, 'EC2': ec2_ids, 'ECR': ecr_ids, 'ECS': ecs_ids, 'EFS': efs_ids, \
        'EKS': eks_ids, 'ELB': elb_ids, 'ELB V2': elbv2_ids, 'Glue': glue_ids, 'Kinesis': kinesis_ids, \
        'KMS': kms_ids, 'Lambda': lambda_ids, 'RDS': rds_ids, 'Redshift': redshift_ids, 'S3': s3_ids, \
        'SNS': sns_ids, 'SQS': sqs_ids, 'WAF': waf_ids, 'WAF V2': wafv2_ids}

    for resource_type in resource_statistics.keys():
        print('----------------------------')
        print(resource_type)
        print(resource_statistics[resource_type])
        print(len(resource_statistics[resource_type]))

    resources_total = apigateway_ids + apigatewayv2_ids + cloudfront_ids + cloudwatch_ids + dynamodb_ids + ec2_ids + ecr_ids + ecs_ids + efs_ids + eks_ids + elb_ids + elbv2_ids + glue_ids + kinesis_ids + kms_ids + lambda_ids + rds_ids + redshift_ids + s3_ids + sns_ids + sqs_ids + waf_ids + wafv2_ids 
    
    print('----------------------------')
    print('Total Resource Count')
    print(len(resources_total))
    