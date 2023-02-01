import boto3
import utils 

def tag_dynamodb():
    dynamodb = boto3.client('dynamodb', region_name=utils.Account.region)
    
    #DynamoDB Arns
    dynamodb_arns = get_dynamodb_arns(dynamodb)
    
    #Filtered DynamoDB Arns 
    filtered_dynamodb_arns = [] 
    
    #Filter and Tag DynamoDB 
    for arn in dynamodb_arns:
        dynamodb_updated = False 
        dynamodb_tags = dynamodb.list_tags_of_resource(ResourceArn=arn)['Tags']
        dynamodb_keys = [dynamodb_tag['Key'] for dynamodb_tag in dynamodb_tags]
        for default_tag in utils.default_tags: 
            if default_tag['Key'] not in dynamodb_keys: 
                dynamodb.tag_resource(ResourceArn=arn, Tags=[default_tag])
                dynamodb_updated = True
        if dynamodb_updated: 
            filtered_dynamodb_arns.append(arn)
    
    return filtered_dynamodb_arns

def get_dynamodb_arns(dynamodb):
    dynamodb_arns = [] 
    dynamo_response = dynamodb.list_tables()
    table_names = dynamo_response['TableNames']
    while 'LastEvaluatedTableName' in dynamo_response.keys():
        for table_name in table_names:
            table_response = dynamodb.describe_table(TableName=table_name)
            table = table_response['Table']
            dynamodb_arns.append(table['TableArn'])
        last_evaluated_table_name = dynamo_response['LastEvaluatedTableName']
        dynamo_response = dynamodb.list_tables(ExclusiveStartTableName=last_evaluated_table_name)
        table_names = dynamo_response['TableNames']
    for table_name in table_names:
        table_response = dynamodb.describe_table(TableName=table_name)
        table = table_response['Table']
        dynamodb_arns.append(table['TableArn'])
    return dynamodb_arns