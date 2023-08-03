#!/usr/bin/env python3

import os
import sys
import logging

import api_client.fas_client as client


logger = logging.getLogger('test')
formatter = ('%(asctime)s - %(name)s - %(levelname)s - '
             '%(message)s - %(pathname)s:%(lineno)d')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)

ApiClient = client.FASApiClient
GenericApiClient = client.FASGenericApiClient

if __name__ == "__main__":
    # define the following environment variables before run
    sn = os.getenv('test_fgt_sn')
    key_file = os.getenv('test_fgt_key_file')
    cert_file = os.getenv('test_fgt_cert_file')
    ca_file = os.getenv('test_fgt_ca_file')
    client_id = os.getenv('test_fas_client_id')
    client_secret = os.getenv('test_fas_client_secret')
    host = os.getenv('test_fas_host')
    port_int = os.getenv('test_fas_int_port', 443)
    port = os.getenv('test_fas_port', 443)

    api = [(host, port_int, True)]
    # CA
    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file)
    print("----TESTING API client with CA certificate ------")
    res = cli.request('GET_USER', sn=sn, vdom='root')

    # GenericApiClient
    api = [(host, port, True)]
    cli = GenericApiClient(api, client_id=client_id,
                           client_secret=client_secret)
    print("----TESTING Generic API client ------")
    res = cli.request('GET_REALM')
