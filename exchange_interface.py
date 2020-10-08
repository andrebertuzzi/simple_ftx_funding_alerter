import requests
import json


class FtxClient:
    def __init__(self, base_url=None):
        self._base_url = 'https://ftx.com/api/'

    def get_all_futures(self):
        url = f'{self._base_url}/futures'
        response = json.loads((requests.get(url)).content)
        futures_names = [symbol['name']
                         for symbol in response['result'] if symbol['perpetual'] == True]
        return futures_names

    def get_funding_rate(self, future):
        url = f'{self._base_url}/futures/{future}/stats'
        response = json.loads((requests.get(url)).content)
        funding_rate = response['result']['nextFundingRate']
        return funding_rate
