#!/usr/bin/env python3

import os
import sys
import logging

import api_client.fortiauth_client as client


logger = logging.getLogger('test')
formatter = ('%(asctime)s - %(name)s - %(levelname)s - '
             '%(message)s - %(pathname)s:%(lineno)d')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)

ApiClient = client.FortiAuthApiClient


if __name__ == "__main__":
    # define the following environment variables before run
    user = os.getenv('test_fac_user')
    password = os.getenv('test_fac_password')
    host = os.getenv('test_fac_host')
    port = os.getenv('test_fac_port', 443)

    api = [(host, port, True)]

    cli = ApiClient(api, user, password)

    print("----TESTING USERGROUPS------")
    message = {"name": "test123"}
    cli.request('GET_USERGROUPS')
    res = cli.request("CREATE_USERGROUP", **message)
    res_body = res.body
    gid = getattr(res_body, 'id', None)
    res = cli.request('GET_USERGROUPS', **message)
    res_body = res.body
    if not gid and isinstance(res_body, list) and len(res_body) > 0:
        gid = res_body[0]['id']

    if gid:
        message = {"id": gid}
        cli.request("DELETE_USERGROUP", **message)
