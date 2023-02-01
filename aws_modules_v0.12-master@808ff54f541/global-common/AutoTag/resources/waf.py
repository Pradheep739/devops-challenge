import boto3 
import utils

def tag_waf():
    waf = boto3.client('waf', region_name=utils.Account.region)
    
    #WAF Arns 
    waf_arns = get_waf_arns(waf)
    
    #Filtered WAF Arns 
    filtered_waf_arns = [] 
    
    #Filter and Tag WAF 
    for arn in waf_arns:
        waf_updated = False 
        waf_tags = waf.list_tags_for_resource(ResourceARN=arn)['TagInfoForResource']['TagList']
        waf_keys = [waf_tag['Key'] for waf_tag in waf_tags]
        for default_tag in utils.default_tags: 
            if default_tag['Key'] not in waf_keys: 
                waf.tag_resource(ResourceArn=arn, Tags=[default_tag])
                waf_updated = True 
        if waf_updated: 
            filtered_waf_arns.append(arn)
    
    return filtered_waf_arns

def tag_wafv2():
    wafv2 = boto3.client('wafv2', region_name=utils.Account.region)
    
    #WAFV2 Arns
    wafv2_arns = get_wafv2_arns(wafv2)
    
    #Filtered WAFV2 Arns 
    filtered_wafv2_arns = []
    
    #Filter and Tag WAFV2
    for arn in wafv2_arns:
        wafv2_updated = False 
        wafv2_tags = wafv2.list_tags_for_resource(ResourceARN=arn)['TagInfoForResource']['TagList']
        wafv2_keys = [wafv2_tag['Key'] for wafv2_tag in wafv2_tags]
        for default_tag in utils.default_tags: 
            if default_tag['Key'] not in wafv2_keys: 
                wafv2.tag_resource(ResourceARN=arn, Tags=[default_tag])
                wafv2_updated = True 
        if wafv2_updated: 
            filtered_wafv2_arns.append(arn) 
    
    return filtered_wafv2_arns 

def get_waf_arns(waf):
    rules_ids = [] 
    rules_response = waf.list_rules()
    while 'NextMarker' in rules_response.keys():
        rules_ids += utils.extract_id(rules_response, 'Rules', 'RuleId')
        marker = rules_response['NextMarker']
        rules_response = waf.list_rules(NextMarker=marker)
    rules_ids += utils.extract_id(rules_response, 'Rules', 'RuleId')
    waf_arns = [waf_get_arn('rule', rule_id) for rule_id in rules_ids]
    
    rule_groups_ids = [] 
    rule_groups_response = waf.list_rule_groups()
    while 'NextMarker' in rule_groups_response.keys():
        rule_groups_ids += utils.extract_id(rule_groups_response, 'RuleGroups', 'RuleGroupId')
        marker = rule_groups_response['NextMarker']
        rule_groups_response = waf.list_rule_groups(NextMarker=marker)
    rule_groups_ids += utils.extract_id(rule_groups_response, 'RuleGroups', 'RuleGroupId')
    waf_arns += [waf_get_arn('rulegroup', rule_group_id) for rule_group_id in rule_groups_ids]
    
    rate_based_rules_ids = [] 
    rate_based_rules_response = waf.list_rate_based_rules()
    while 'NextMarker' in rate_based_rules_response.keys():
        rate_based_rules_ids += utils.extract_id(rate_based_rules_response, 'Rules', 'RuleId')
        marker = rate_based_rules_response['NextMarker']
        rate_based_rules_response = waf.list_rate_based_rules(NextMarker=marker)
    rate_based_rules_ids += utils.extract_id(rate_based_rules_response, 'Rules', 'RuleId')
    waf_arns += [waf_get_arn('ratebasedrule', rate_based_rule_id) for rate_based_rule_id in rate_based_rules_ids]
    
    web_acl_ids = [] 
    web_acl_response = waf.list_web_acls()
    while 'NextMarker' in web_acl_response.keys():
        web_acl_ids += utils.extract_id(web_acl_response, 'WebACLs', 'WebACLId')
        marker = web_acl_response['NextMarker']
        web_acl_response = waf.list_web_acls(NextMarker=marker)
    web_acl_ids += utils.extract_id(web_acl_response, 'WebACLs', 'WebACLId')
    waf_arns += [waf_get_arn('webacl', web_acl_id) for web_acl_id in web_acl_ids]
    
    return waf_arns 

def waf_get_arn(resource_type, resource_id):
    return f'arn:aws:waf::{utils.Account.account_id}:{resource_type}/${resource_id}'

def get_wafv2_arns(wafv2):
    wafv2_arns = [] 
    try:
        wafv2_arns += extract_wafv2_arns(wafv2, 'webacl', 'CLOUDFRONT', 'WebACLs')
    except Exception as e: 
        print(e) 
        print('CloudFront scope valid only for us-east-1 region')
        
    wafv2_arns += extract_wafv2_arns(wafv2, 'webacl', 'REGIONAL', 'WebACLs')
    
    try: 
        wafv2_arns += extract_wafv2_arns(wafv2, 'ipset', 'CLOUDFRONT', 'IPSets')
    except Exception as e: 
        print(e) 
        print('CloudFront scope valid only for us-east-1 region')
        
    wafv2_arns += extract_wafv2_arns(wafv2, 'ipset', 'REGIONAL', 'IPSets')
    
    try: 
        wafv2_arns += extract_wafv2_arns(wafv2, 'rulegroup', 'CLOUDFRONT', 'RuleGroups')
    except Exception as e: 
        print(e) 
        print('CloudFront scope valid only for us-east-1 region')
        
    wafv2_arns += extract_wafv2_arns(wafv2, 'rulegroup', 'REGIONAL', 'RuleGroups')
    
    try: 
        wafv2_arns += extract_wafv2_arns(wafv2, 'regexpatternset', 'CLOUDFRONT', 'RegexPatternSets')
    except Exception as e: 
        print(e) 
        print('CloudFront scope valid only for us-east-1 region')
        
    wafv2_arns += extract_wafv2_arns(wafv2, 'regexpatternset', 'REGIONAL', 'RegexPatternSets')
    
    return wafv2_arns 

def extract_wafv2_arns(wafv2, resource_type, scope, key1):
    wafv2_arns = [] 
    
    if resource_type == 'webacl':
        response = wafv2.list_web_acls(Scope=scope)
    elif resource_type == 'ipset':
        response = wafv2.list_ip_sets(Scope=scope)
    elif resource_type == 'rulegroup':
        response = wafv2.list_rule_groups(Scope=scope)
    else:
        response = wafv2.list_regex_pattern_sets(Scope=scope)

    while 'NextMarker' in response.keys():
        resources = response[key1]
        for resource in resources:
            wafv2_arns.append(resource['ARN'])
        marker = response['NextMarker']
        if resource_type == 'webacl':
            response = wafv2.list_web_acls(Scope=scope, NextMarker=marker)
        elif resource_type == 'ipset':
            response = wafv2.list_ip_sets(Scope=scope, NextMarker=marker)
        elif resource_type == 'rulegroup':
            response = wafv2.list_rule_groups(Scope=scope, NextMarker=marker)
        else:
            response = wafv2.list_regex_pattern_sets(Scope=scope, NextMarker=marker)
    
    resources = response[key1]
    for resource in resources:
        wafv2_arns.append(resource['ARN'])
    
    return wafv2_arns
