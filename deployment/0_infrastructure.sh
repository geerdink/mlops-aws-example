#!/bin/bash

# this is the base infrastructure for the application; run it once to set up the necessary AWS services

# create an ECR repository for storing the Docker image
aws ecr create-repository --repository-name diabetes

# create an S3 bucket with versioning enabled for the `test` version of the machine learning model
aws s3api create-bucket --bucket diabetes-model-test --region eu-west-1 --create-bucket-configuration LocationConstraint=eu-west-1
aws s3api put-bucket-versioning --bucket diabetes-model-test --versioning-configuration Status=Enabled

# create an S3 bucket with versioning enabled for the `production` version of the machine learning model
aws s3api create-bucket --bucket diabetes-model-prod --region eu-west-1 --create-bucket-configuration LocationConstraint=eu-west-1
aws s3api put-bucket-versioning --bucket diabetes-model-prod --versioning-configuration Status=Enabled

# create a role for ECS to enable Fargate
aws iam --region eu-west-1 create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://task-execution-assume-role.json
aws iam --region eu-west-1 attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# create a ECS cluster configuration
ecs-cli configure --cluster diabetes --default-launch-type FARGATE --config-name diabetes --region eu-west-1

# configure your profile (replace with your own key and secret)
ecs-cli configure profile --access-key AWS_ACCESS_KEY_ID --secret-key AWS_SECRET_ACCESS_KEY --profile-name tutorial-profile

# create an ECS cluster and security groups
ecs-cli up --cluster-config diabetes --ecs-profile diabetes-profile

# use a security group to enable access to port 5000
aws ec2 describe-security-groups --filters Name=vpc-id,Values=vpc-FILL_IN --region eu-west-1
aws ec2 authorize-security-group-ingress --group-id sg-FILL_IN --protocol tcp --port 5000 --cidr 0.0.0.0/0 --region eu-west-1
