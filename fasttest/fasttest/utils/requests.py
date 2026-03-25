import json
import requests
from xffasttest.common.dict import Dict
class Requests:

    @staticmethod
    def get(url: str, headers: dict={}) -> dict:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = Dict(json.loads(response.text))
            return data
        else:
            raise Exception(data)


    @staticmethod
    def post(url: str, data: dict={}, headers: dict={}) -> dict:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            data = Dict(json.loads(response.text))
            return data
        else:
            raise Exception(data)