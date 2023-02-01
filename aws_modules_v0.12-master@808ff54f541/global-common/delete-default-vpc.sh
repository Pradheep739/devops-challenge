#!/bin/bash
#The following script will delete default VPC in all regions.
printf "Stating to delete default VPC's in all regions\n"
for region in $(aws ec2 describe-regions | jq -r .Regions[].RegionName); do
  
  # get default vpc
  vpc=$(aws ec2 --region ${region} describe-vpcs --filter Name=isDefault,Values=true | jq -r .Vpcs[0].VpcId)
  if [ "${vpc}" = "null" ]; then
    printf "No default vpc found in region ${region}\n"
    continue
  fi
  printf "Found default vpc ${vpc} in region ${region}\n"

  # get internet gateway
  igw=$(aws ec2 --region ${region} describe-internet-gateways --filter Name=attachment.vpc-id,Values=${vpc} \
    | jq -r .InternetGateways[0].InternetGatewayId)
  if [ "${igw}" != "null" ]; then
    printf "Detaching and deleting internet gateway ${igw} in region ${region}\n"
    aws ec2 --region ${region} detach-internet-gateway --internet-gateway-id ${igw} --vpc-id ${vpc}
    aws ec2 --region ${region} delete-internet-gateway --internet-gateway-id ${igw}
  fi

  # get subnets
  subnets=$(aws ec2 --region ${region} \
    describe-subnets --filters Name=vpc-id,Values=${vpc} \
    | jq -r .Subnets[].SubnetId)
  if [ "${subnets}" != "null" ]; then
    for subnet in ${subnets}; do
      printf "Deleting subnet ${subnet} in region ${region}\n"
      aws ec2 --region ${region} delete-subnet --subnet-id ${subnet}
    done
  fi

  # https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-vpc.html
  # - You can't delete the main route table
  # - You can't delete the default network acl
  # - You can't delete the default security group

  # delete default vpc
  printf "Deleting vpc ${vpc} in region ${region}\n"
  aws ec2 --region ${region} delete-vpc --vpc-id ${vpc}

done
printf "Default VPC deletion has been completed\n"