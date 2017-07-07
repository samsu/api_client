#!/usr/bin/env python

import time
import os
import inspect

import api_client.forticare_client as client


ApiClient=client.FortiCareApiClient

if __name__ == "__main__":
    api = [("172.30.38.89", 443, True)]
    key_file = "/root/subca/cert201706291056.key"
    cert_file = "/root/subca/cert201706291056.crt"
    cert_reqs = "/root/subca/cert201706291056.csr"
    ca_file = "/root/subca/chain.pem"
    server_hostname = "fortinet-ca2.fortinet.com"

    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file,
                    ssl_sni=server_hostname)

    print "----TESTING ------"
    cli.request('TEST')
