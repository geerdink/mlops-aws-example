#!/bin/bash

# check if the api is running
curl http://localhost:5000/ping

# run this script on a local machine once the api is started to get a prediction
curl -vX POST -H 'Content-Type: application/json' -d '{"pregnancies": 1, "glucose": 189, "blood_pressure": 60, "skin_thickness": 23, "insulin": 846, "bmi": 30.1, "pedigree": 0.398, "age": 13}' http://localhost:5000/predict
