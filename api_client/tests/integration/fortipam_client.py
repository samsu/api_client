#!/usr/bin/env python3

import os
import sys
import time

import logging

import api_client.fortipam_client as client


logger = logging.getLogger('test')
formatter = ('%(asctime)s - %(name)s - %(levelname)s - '
             '%(message)s - %(pathname)s:%(lineno)d')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)

ApiClient = client.FortiPAMApiClient


if __name__ == "__main__":
    host = os.getenv('test_fpam_host')
    port = os.getenv('test_fpam_port', 443)
    user = os.getenv('test_fpam_user')
    password = os.getenv('test_fpam_password')

    api = [(host, port, True)]
    cli = ApiClient(api, user, password)
    secret_name = 'test10001'
    message = {
        "folder": 3,
        "name": secret_name,
        "secret_template": "FortiProduct (SSH Password)",
        "host": host,
        "username": user,
        "password": password,
        "url": "",
        "inherit-permission": "enable"
    }
    res = cli.request('CREATE_SECRET', **message)

    time.sleep(2)
    res = cli.request('GET_SECRETS')
    secrets = res.body['results']
    secret_id = 0
    for secret in secrets:
        if secret['name'] == secret_name:
            secret_id = secret['id']
            break
    res = cli.request('DELETE_SECRET', id=secret_id)

    # test FortiPAM folder API
    folder_name = "Auto_folder"
    message = {
        "name": folder_name
    }
    res = cli.request('CREATE_FOLDER', **message)
    time.sleep(2)
    res = cli.request('GET_FOLDERS')
    folders = res.body['results']
    for folder in folders:
        if folder['name'] == folder_name:
            folder_id = folder['id']
            break
    res = cli.request('DELETE_FOLDER', id=folder_id)
    res = cli.request('LOGOUT')
