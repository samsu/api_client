import os
import sys
import logging

import api_client.faz_client as client


logger = logging.getLogger('test')
formatter = ('%(asctime)s - %(name)s - %(levelname)s - '
             '%(message)s - %(pathname)s:%(lineno)d')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)

ApiClient = client.FortiAnalyzerApiClient


if __name__ == "__main__":
    # replace the following ip and credential before run
    faz_ip = os.getenv('test_faz_ip')
    rmt_faz_ip = os.getenv('test_rmt_faz_ip')
    user = os.getenv('test_faz_user')
    password = os.getenv('test_faz_password')
    api = [(faz_ip, 443, True)]
    cli = ApiClient(api, user=user, password=password)

    message = {
        "adom": "root",
        "sn": "FTCSRV0000953396",
    }
    res = cli.request('ADD_DEVICE', **message)
    assert(res['result'][0]['status']['code'] == 0)

    message = {
        "address": rmt_faz_ip,
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
        "address": rmt_faz_ip,
        "name": "new-name",
        "adom": "root",
        "sn": "FTCSRV0000953396",
        "delay": "realtime",
        "id": 16,
        "reliable": "disable",
        "secure": "disable"
    }
    res = cli.request('MODIFY_FORWARDER', **message)
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
    res = cli.request('DELETE_FORWARDER', **message)
    assert(res['result'][0]['status']['code'] == 0)

    message = {
        "adom": "root",
        "sn": "FTCSRV0000953396",
    }
    res = cli.request('DELETE_DEVICE', **message)
    assert(res['result'][0]['status']['code'] == 0)
