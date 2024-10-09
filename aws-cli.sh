#!/bin/bash

# Function to fetch EC2 instance public DNS by name
get_ec2_dns() {
  # Check if an instance name was provided
  if [ -z "$1" ]; then
    echo "Usage: Please provide the EC2 instance name."
    return 1
  fi

  INSTANCE_NAME=$1

  # Get the instance ID of the specified EC2 instance by its name
  INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=$INSTANCE_NAME" \
    --query "Reservations[*].Instances[*].InstanceId" \
    --output text)

  # Check if the instance was found
  if [ -z "$INSTANCE_ID" ]; then
    echo "No instance found with the name '$INSTANCE_NAME'."
    return 1
  fi

  # Fetch the public DNS name of the specified instance
  PUBLIC_DNS=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query "Reservations[*].Instances[*].PublicDnsName" \
    --output text)

  # Output the DNS name
  echo "$PUBLIC_DNS"
}


##!/bin/bash
#
## Function to fetch EC2 instance public IP and DNS by name
#get_ec2_cdn() {
#  # Check if an instance name was provided
#  if [ -z "$1" ]; then
#    echo "Usage: Please provide the EC2 instance name."
#    return 1
#  fi
#
#  INSTANCE_NAME=$1
#
#  # Get the instance ID of the specified EC2 instance by its name
#  INSTANCE_ID=$(aws ec2 describe-instances \
#    --filters "Name=tag:Name,Values=$INSTANCE_NAME" \
#    --query "Reservations[*].Instances[*].InstanceId" \
#    --output text)
#
#  # Check if the instance was found
#  if [ -z "$INSTANCE_ID" ]; then
#    echo "No instance found with the name '$INSTANCE_NAME'."
#    return 1
#  fi
#
#  # Fetch the public IP and DNS name of the specified instance
#  PUBLIC_IP=$(aws ec2 describe-instances \
#    --instance-ids $INSTANCE_ID \
#    --query "Reservations[*].Instances[*].PublicIpAddress" \
#    --output text)
#
#  PUBLIC_DNS=$(aws ec2 describe-instances \
#    --instance-ids $INSTANCE_ID \
#    --query "Reservations[*].Instances[*].PublicDnsName" \
#    --output text)
#
#  # Output the results
#  echo "Instance Name: $INSTANCE_NAME"
#  echo "Instance ID: $INSTANCE_ID"
#  echo "Public IP Address: $PUBLIC_IP"
#  echo "Public DNS Name: $PUBLIC_DNS"
#}
