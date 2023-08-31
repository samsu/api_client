#!/usr/bin/env python3

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

    cs_ids = ["953397"]  # , "953398", "953399"]
    for cid in cs_ids:
        # device
        sn = "FTCSRV0000" + cid
        # forwarder
        name = cid
        new_name = "new_" + name

        # delete residual forwarder records
        for name_to_delete in (name, new_name):
            message = {
                "fields": True,
                "name": name_to_delete
            }
            fwd_id = None
            res = cli.request('GET_FORWARDER', **message)
            if len(res['result'][0]['data']) > 0:
                fwd_id = res['result'][0]['data'][0]['id']
            if fwd_id is not None:
                message = {
                    "id": fwd_id
                }
                res = cli.request('DELETE_FORWARDER', **message)
        # delete residual device record(s)
        message = {
            "adom": "root",
            "sn": sn,
        }
        res = cli.request('DELETE_DEVICE', **message)

        # start to test
        message = {
            "adom": "root",
            "sn": sn,
        }
        res = cli.request('ADD_DEVICE', **message)
        assert(res['result'][0]['status']['code'] == 0)

        message = {
            "address": rmt_faz_ip,
            "name": name,
            "adom": "root",
            "sn": sn,
            "delay": "realtime",
            "reliable": "disable"
        }
        res = cli.request('ADD_FORWARDER', **message)
        assert(res['result'][0]['status']['code'] == 0)
        message = {
            "fields": True,
            "name": name
        }
        res = cli.request('GET_FORWARDER', **message)
        fwd_id = res['result'][0]['data'][0]['id']
        assert(res['result'][0]['status']['code'] == 0)
        assert(res['result'][0]['data'][0]['server-name'] == name)
        message = {
            "address": rmt_faz_ip,
            "name": new_name,
            "adom": "root",
            "sn": sn,
            "delay": "realtime",
            "id": fwd_id,
            "reliable": "disable"
        }
        res = cli.request('MODIFY_FORWARDER', **message)
        assert(res['result'][0]['status']['code'] == 0)

        message = {
            "fields": True,
            "id": fwd_id
        }
        res = cli.request('GET_FORWARDER', **message)
        assert(res['result'][0]['status']['code'] == 0)
        assert(res['result'][0]['data']['server-name'] == new_name)

        message = {
            "id": fwd_id
        }
        res = cli.request('DELETE_FORWARDER', **message)
        assert(res['result'][0]['status']['code'] == 0)

        message = {
            "adom": "root",
            "sn": sn,
        }
        res = cli.request('DELETE_DEVICE', **message)
        assert(res['result'][0]['status']['code'] == 0)
