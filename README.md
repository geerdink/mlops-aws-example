# Diabetes prediction

This application gives a prediction whether a patient has diabetes.
Once running, the API will utilize a machine learning model that is exported to joblib format.
The API endpoint accepts a JSON object of a patient, and returns a prediction in the form of a `1` or `0`.

## Architecture
The API runs as a Fargate service.
It retrieves the machine learning model from a versioned S3 bucket.

The model is logically separated from the API code.
This ensures that they can be release individually, making the application flexible.
Obviously there is a dependency between the API and the model, since the API has to supply the input data in the correct format.
Therefore, before any new release of the model or the code, extensive testing should be done to guarantee a correctly working application.

> Note: the API currently uses only the latest version of the model that is uploaded to the S3 production bucket.

## Development
The code has been developed with Python 3.9.
To start developing, create a new virtual environment by running the following command from the main project folder: `python3 -m venv venv`.

The `python` and `pip` executables are now in the `venv` directory.
In IntelliJ IDEA, make sure to use this as your project SDK.

Install the required packages by running the following command: `venv/bin/pip install -r requirements.txt`.

## Testing
There are unit tests in the `api/test_api.py` file.
The tests can be run from IntelliJ IDEA, or with the `python -m unittest discover` command from the `api` directory.

## Running
To _run_ locally:
```bash
docker-compose build
docker-compose up
```

Then, use the scripts in the `scripts` folder for testing.

> Note: the current infrastructure setup is very limited and only suited for demonstration purposes.
> In an enterprise environment, there should be more infrastructure-as-code, for example by setting up a CloudFormation stack.

## Deployment
Prerequisites:
* install [Docker](https://docs.docker.com/get-docker/)
* install the [AWS CLI](https://aws.amazon.com/cli/)
* install the [AWS ECS CLI](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html)

To _deploy_ the application to AWS, there are a couple of scripts in the `deployment` folder.
They can be run in order from a local machine to create all the necessary infrastructure and do a release of the model and code.
This will result in a working API.

The steps are:
0. upload a new version of the model to the test environment
0. test the code with the newly uploaded model
0. upload the model to the production environment
0. create a new docker image

> Note: in an enterprise environment, this setup will _not_ qualify.
> The deployment scripts will be useful as a first start, but the deployment pipeline must be professionalized.
> Starting with a Git repo, a continuous delivery tool should be configured that builds, tests, and deploys the artifacts.
> The tool should take care of multiple environments, versioning, etc.
> For example, in AWS the CodeBuild and CodePipeline services can be used.
> For a more vendor-neutral approach, a setup with (Dockerized) Jenkins is also an option.
