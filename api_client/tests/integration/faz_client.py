import sys
import logging
import time
logger = logging.getLogger('test')
formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)

import api_client.faz_client as client


ApiClient = client.FortiAnalyzerApiClient

if __name__ == "__main__":
    api = [("10.160.37.137", 443, True)]
    user = "admin"
    password = "fortinet"
    cli = ApiClient(api, user=user, password=password)

    message = {
        "adom": "root",
        "sn": "FTCSRV0000953396",
    }
    res = cli.request('ADD_DEVICE', **message)
    assert(res['result'][0]['status']['code'] == 0)

    message = {
        "address": "10.160.37.138",
        "name": "953396",
        "adom": "root",
        "sn": "FTCSRV0000953396",
        "delay": "realtime",
        "id": 16,
        "reliable": "disable",
        "secure": "disable"
    }
    res = cli.request('ADD_FORWARDER', **message)
    assert(res['result'][0]['status']['code'] == 0)

    message = {
        "id": 16
    }
    res = cli.request('GET_FORWARDER', **message)
    assert(res['result'][0]['status']['code'] == 0)
    assert(res['result'][0]['data']['server-name'] == "953396")

    message = {
        "address": "10.160.37.138",
        "name": "new-name",
        "adom": "root",
        "sn": "FTCSRV0000953396",
        "delay": "realtime",
        "id": 16,
        "reliable": "disable",
        "secure": "disable"
    }
    res = cli.request('EDIT_FORWARDER', **message)
    assert(res['result'][0]['status']['code'] == 0)

    message = {
        "id": 16
    }
    res = cli.request('GET_FORWARDER', **message)
    assert(res['result'][0]['status']['code'] == 0)
    assert(res['result'][0]['data']['server-name'] == "new-name")

    message = {
        "id": 16
    }
    res = cli.request('DEL_FORWARDER', **message)
    assert(res['result'][0]['status']['code'] == 0)

    message = {
        "adom": "root",
        "sn": "FTCSRV0000953396",
    }
    res = cli.request('DEL_DEVICE', **message)
    assert(res['result'][0]['status']['code'] == 0)
