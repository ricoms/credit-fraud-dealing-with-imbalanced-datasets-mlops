#!/bin/bash

docker-compose up -d

curl --header "Content-Type: application/json" --request POST --data-binary @../../ml/input/api/payload.json http://localhost:8080/invocations > output.json

docker-compose down