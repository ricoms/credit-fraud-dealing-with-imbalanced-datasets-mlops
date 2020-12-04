# credit-fraud-dealing-with-imbalanced-datasets-mlops

Reimplementing a Kaggle solution into mlops.

The solution implemented here is from [credit-fraud-dealing-with-imbalanced-datasets notebook](https://www.kaggle.com/janiobachmann/credit-fraud-dealing-with-imbalanced-datasets) which provides exploration and multiple  solutions to the [Credict Card Fraud Detection Kaggle challenge](https://www.kaggle.com/mlg-ulb/creditcardfraud).

## 1 Software Need/Solution

This repository contains a solution to kaggle credit-fraud challenge and focus on organization and automation for deployment of the model. This fulfills the need of deploying an online and a batch api for prediction requests.

## 2 Prerequisites

This software does not requires specific hardwares. This project is based on 
[**Python 3.8**](https://www.python.org/downloads/release/python-380/), 
[**dvc**](https://dvc.org/doc/install), 
[**kaggle**](https://github.com/Kaggle/kaggle-api), 
[**pipenv**](https://github.com/pypa/pipenv), 
[**Makefile**](https://www.gnu.org/software/make/),
and [**Docker**](https://www.docker.com/get-started).

### 2.1 Setup

Install requirements cited on section 2 or guarantee those are functioning in your local setup.

Kaggle API requires you to setup an API Token as described [here](https://github.com/Kaggle/kaggle-api#api-credentials).

DVC is using AWS S3 remote as an artifact repository, just as an example as all required files (model, metrics and plots) are available within the repo. If you would like to use an AWS S3 remote you will be required to setup AWS credentials as described [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html#envvars-set). This repository CICD is using my personal AWS account using registered secrets within Github Actions.

## 3 Build

### 3.1 Locally

I'm using **DVC** package that helps me create a DAG (direct acyclic graph) of codes to run the complete experiment. The steps existing in this repository are shown in file `dvc.yaml`. If you wish to run the experiment in full just run `dvc repro`, if you wish to run partially just run `dvc repro get-data` - being `get-data` the step name, also this can be run for multiple targets as decribed [here](https://dvc.org/doc/command-reference/repro#repro).

## 4 How to run it?

### 4.1 Machine Learning training

To run a full experiment just use the command:

`dvc repro` 

This will run two steps described in `dvc.yaml` file.

After this you should have a new `ml/output/credit-card-fraud/model.joblib` file. This file is the serialization of a Machien Learning algorithm that you can now serve.

### 4.1 Machine Learning serving

For serving there are two possibilities: online prediction and batch prediction.

#### **Online Prediction**

run the command `make serve`, this will freeze your terminal and raise a local **Docker** container which will have an api awaiting **POST** requests for predictions. This repo provides a small sample `ml/input/api/payload.json` which will be used if you run on another terminal the command `make predict`. This should allow you to see something like the image below:

![Serve predict](images/serve-predict.png?raw=true "Serve predict")

The left terminal is serving the API where we can see the 'server' logs, while the right terminal sent a payload for prediction and received an online answer.

#### **Offline/Batch Prediction**

For this I setup a small module at this path `scripts/batch_predict/` which contains three files `batch_predict.sh`, `docker-compose.yml` and `request.py`. This modules uses [**docker-compose**](https://docs.docker.com/compose/). Inside this folder you run `./batch_predict.sh`. This script will verify if required files (`model.joblib` and `payload.json` exists in their expected folders), will raise the docker configuration setup defined at `docker-compose.yml`, will wait until a `response.json` is generated, and finally will destroy the docker configuration setup.


## 5 How do I install it?

This is a service software, the idea is to turn its final result (the algorithm) an API. If you intend to develop I provide detailed package requirements with `Pipfile` and `Pipfile.lock` for pipenv. Also `Makefile` provide the command `make install` which will install requirements using pipenv.

<!-- ## 5 Is the software ready?


### 5.1 Hello World


### 5.2 Hello Mars


## 6 Tips and Tricks

% code samples

% config tips

## 7 Troubleshooting

% FAQs

% Bugs

## 8 Contributions

% Community

% Explain How -->

## 6 Licensing and Credits

The repo provides the capability of training and serving a `sklearn` model capable of predicting possible credit fraud attempts. It uses the publicly available dataset [Credict Card Fraud Detection Kaggle challenge](https://www.kaggle.com/mlg-ulb/creditcardfraud).


<!-- ## 6 List of Changes -->
