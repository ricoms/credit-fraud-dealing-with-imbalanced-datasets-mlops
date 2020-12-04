#!/usr/bin/env python

import requests
from pathlib import Path

url = 'http://credit-fraud-api:8080/invocations'
payload = open('/opt/payload.json')
headers = {'content-type': 'application/json'}
output_path = '/opt/output/response.json'

if Path(output_path).is_file():
    print(f"{output_path} exists.")
else:
    r = requests.post(url, data=payload, headers=headers)

    print(r.status_code)
    print(r.headers)
    print(r.content)

    with open(output_path,'wb') as f:
        f.write(r.content)