#!/bin/bash


REQUIRED_FILE1="../../ml/input/api/payload.json"
REQUIRED_FILE2="../../ml/output/credit-card-fraud/model.joblib" 

if [ -f $REQUIRED_FILE1 ] && [ -f $REQUIRED_FILE2 ]; then
    docker-compose up --build -d

    while [ ! -f response.json ]
    do
    sleep 0.2
    done

    ls -l response.json

    docker-compose down
else
   echo "Files $REQUIRED_FILE1 and $REQUIRED_FILE2 does not exist."
fi

