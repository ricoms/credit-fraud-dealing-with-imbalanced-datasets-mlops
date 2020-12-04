.PHONY = help test clean
.DEFAULT_GOAL = help

project-name=credit-fraud
DOCKER_IMAGE_NAME=credit-fraud-ml

hyperparameters_file=ml/input/config/hyperparameters.json
hyperparameters=`cat ${hyperparameters_file}`

CURRENT_UID := $(shell id -u)
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

# train: ${DATA_FILE}
# 	cd src/ && ./train \
# 		--project_name ${project-name} \
# 		--input_dir ../${DATA_FILE}

docker-train: build-image ${DATA_FILE}
	docker run --rm \
		-u ${CURRENT_UID}:${CURRENT_UID} \
		-v ${PWD}/ml:/opt/ml \
		${DOCKER_IMAGE_NAME} train \
			--project_name ${project-name} \
			--input_dir /opt/${DATA_FILE}

serve: build-image ml/output/credit-card-fraud/model.joblib
	docker run --rm -it \
		-v $(PWD)/ml:/opt/ml \
		-p 8080:8080 \
		${DOCKER_IMAGE_NAME} \
			serve \
				--num_cpus=1

predict: scripts/predict.sh ml/input/api/payload.json
	./scripts/predict.sh ml/input/api/payload.json application/json

# CICD commands

lint-docker:
	docker run --rm -i hadolint/hadolint:v1.17.6-3-g8da4f4e-alpine < Dockerfile

lint-python:
	pipenv run flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
	pipenv run flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

lint: lint-docker lint-python
	
coverage:
	pipenv run pytest --cov-report=term-missing --cov=src --cov-fail-under=0.4
	pipenv run pytest --cov-report=html --cov=src

build-image:
	docker build -f Dockerfile -t ${DOCKER_IMAGE_NAME} .