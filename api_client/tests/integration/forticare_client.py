#!/usr/bin/env python3
import os
import sys
import logging

import api_client.forticare_client as client


logger = logging.getLogger('test')
formatter = ('%(asctime)s - %(name)s - %(levelname)s - '
             '%(message)s - %(pathname)s:%(lineno)d')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)

ApiClient = client.FortiCareApiClient


if __name__ == "__main__":
    # define the following environment variables before run
    host = os.getenv('test_fc_host')
    port = os.getenv('test_fc_port', 443)
    email = os.getenv('test_fc_account_email')
    sub_key_file = os.getenv('test_fas_sub_key_file')
    sub_cert_file = os.getenv('test_fas_sub_cert_file')
    sub_ca_file = os.getenv('test_fas_sub_ca_file')
    key_file = os.getenv('test_fas_key_file')
    cert_file = os.getenv('test_fas_cert_file')
    ca_file = os.getenv('test_fas_ca_file')

    api = [(host, port, True)]

    # Sub CA
    print("----TESTING API client with Sub CA certificate ------")

    server_hostname = "fortinet-ca2.fortinet.com"
    cli = ApiClient(api, key_file=sub_key_file,
                    cert_file=sub_cert_file, ca_file=sub_ca_file,
                    ssl_sni=server_hostname)
    cli.request('GET_ACCOUNT', email=email)

    # CA
    print("----TESTING API client with CA certificate ------")
    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file)
    cli.request('GET_ACCOUNT', email=email)
