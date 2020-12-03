import json


class HealthCheckResource:
    def on_get(self, request, response):
        body = {'data': {'status': 'ok'}}
        response.body = json.dumps(body)
