import os
import flask
import json
import joblib
import pandas
import boto3
import sklearn  # needed for joblib

from domain.patient import create_patient, patient_names

app = flask.Flask('Diabetes')

diabetes_model = None


def get_model(environment: str):
    global diabetes_model

    # set the file path for the model
    cwd = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(cwd, 'model/', 'pima_model.joblib')

    # download the model from S3 to a local folder
    s3 = boto3.client('s3')
    print(f'Getting model from {environment}...')
    s3.download_file(f'diabetes-model-{environment}', 'pima_model.joblib', model_path)

    # load the model
    print(f'Loading model from {model_path}...')
    diabetes_model = joblib.load(model_path)


@app.route('/ping', methods=['GET'])
def ping():
    return flask.Response(response=json.dumps('pong'), status=200, mimetype='application/json')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Expects a data record of a patient
    :return: Prediction whether a patient has diabetes (1) or not (0)
    """
    data = json.dumps(flask.request.get_json())
    print('Predicting patient: ', data)

    # prepare data
    patient = create_patient(data)
    df = pandas.read_csv(patient.to_array(), names=patient_names())

    # get prediction
    prediction = diabetes_model.predict(df.values)
    print('Prediction: ', prediction)

    return flask.Response(response=json.dumps(int(prediction[0])), status=200, mimetype='application/json')


if __name__ == '__main__':
    get_model('prod')  # change this to 'test' if running on a local machine
    app.run(host='0.0.0.0', port=5000)
