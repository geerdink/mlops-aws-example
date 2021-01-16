#!/bin/bash

# this is step 1 of the deployment pipeline: uploading the model and testing the API

# upload the model to the test environment
aws s3 cp ../api/model/pima_model.joblib s3://diabetes-model-test

# run the unit tests
../venv/bin/python -m unittest discover

# if tests are successful: upload the model to production, creating a new version
aws s3 cp ../api/model/pima_model.joblib s3://diabetes-model-prod
