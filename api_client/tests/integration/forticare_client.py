#!/usr/bin/env python

import api_client.forticare_client as client

ApiClient = client.FortiCareApiClient


if __name__ == "__main__":
    api = [("172.30.38.89", 443, True)]

    # Sub CA
    print "----TESTING API client with Sub CA certificate ------"
    key_file = "/root/subca/cert201706291056.key"
    cert_file = "/root/subca/cert201706291056.crt"
    cert_reqs = "/root/subca/cert201706291056.csr"
    ca_file = "/root/subca/chain.pem"
    server_hostname = "fortinet-ca2.fortinet.com"
    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file,
                    ssl_sni=server_hostname)
    cli.request('TEST')

    # CA
    print "----TESTING API client with CA certificate ------"
    key_file = "/root/ca/cert201706291056.key"
    cert_file = "/root/ca/cert201706291056.crt"
    ca_file = "/root/ca/cacertkey1-sha2.pem"
    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file)
    cli.request('TEST')
