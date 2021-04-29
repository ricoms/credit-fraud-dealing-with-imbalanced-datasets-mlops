.PHONY = help test clean
.DEFAULT_GOAL = help

project-name=credit-fraud
DOCKER_IMAGE_NAME=credit-fraud-ml

hyperparameters_file=ml/input/config/hyperparameters.json
hyperparameters=`cat ${hyperparameters_file}`

UID_GID := "$(shell id -u):$(shell id -g)"

time-stamp=$(shell date "+%Y-%m-%d-%H%M%S")
DATA_FILE = ml/input/data/training/creditcard.csv

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type make install"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "Other functionalities check Makefile targets"
	@echo "------------------------------------"

test:
	# Additional, optional, tests could go here
	pytest -v

clean:
	rm -r *.project

install:
	pip install --no-cache-dir pipenv==2020.8.13
	pipenv install --dev

train: ${DATA_FILE}
	cd src/ && ./train \
		--project_name ${project-name} \
		--input_dir ../${DATA_FILE}

data:
	kaggle datasets download mlg-ulb/creditcardfraud --unzip --path ml/input/data/training

profile-data:
	./scripts/data_profiler.py --data_path ml/input/data/training/creditcard.csv --output_dir ml/output/credit-card-fraud/

docker-build:	
	docker build -f docker/Dockerfile -t ${DOCKER_IMAGE_NAME} .

docker-train: ${DATA_FILE} docker-build
	docker run \
		-u ${UID_GID} \
		-v ${PWD}/ml:/opt/ml \
		${DOCKER_IMAGE_NAME} train \
			--project_name credit-fraud \
			--input_dir /opt/ml/input/data/training/creditcard.csv

serve: ml/output/credit-card-fraud/model.joblib docker-build
	docker run ${DOCKER_IMAGE_NAME} -v ./ml:/opt/ml:rw serve --num_cpus=1

predict: scripts/predict.sh ml/input/api/payload.json
	./scripts/predict.sh ml/input/api/payload.json application/json

# CICD commands

lint-docker:
	docker run --rm -i hadolint/hadolint:v1.17.6-3-g8da4f4e-alpine < Dockerfile

lint-python:
	flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

lint: lint-docker lint-python
	
coverage:
	pytest --cov-report=term-missing --cov=src --cov-fail-under=0.8
	pytest --cov-report=html --cov=src

build-image:
	docker build -f Dockerfile -t ${DOCKER_IMAGE_NAME} .