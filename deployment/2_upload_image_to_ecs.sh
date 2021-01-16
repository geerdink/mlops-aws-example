#!/bin/bash

# this is step 2 of the deployment pipeline: uploading (pushing) the Docker image
# that contains the API and model to AWS ECR (Elastic Container Registry)

# deploy the container
ecs-cli compose --project-name diabetes service up --create-log-groups --cluster-config diabetes --ecs-profile diabetes-profile

# check the status of the Fargate service
ecs-cli compose --project-name diabetes service ps --cluster-config diabetes --ecs-profile diabetes-profile

# check the url
curl FILL_IN.eu-west-1.compute.amazonaws.com:5000/ping

# get a prediction
curl -vX POST -H 'Content-Type: application/json' -d '{"pregnancies": 1, "glucose": 189, "blood_pressure": 60, "skin_thickness": 23, "insulin": 846, "bmi": 30.1, "pedigree": 0.398, "age": 63}' FILL_IN.eu-west-1.compute.amazonaws.com:5000/predict
