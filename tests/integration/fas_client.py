#!/usr/bin/env python

import api_client.fas_client as client


ApiClient = client.FASApiClient

if __name__ == "__main__":
    api = [("10.160.37.61", 443, True)]
    # CA
    print "----TESTING API client with CA certificate ------"
    # key_file = "/root/ca/cert201706291056.key"
    # cert_file = "/root/ca/cert201706291056.crt"
    # ca_file = "/root/ca/cacertkey1-sha2.pem"

    key_file = "/root/fgt/box/fgt_b.key"
    cert_file = "/root/fgt/fgt_b.crt"
    ca_file = "/root/fgt/test_root_Fortinet_CA.cer"

    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file)
    cli.request('GET_ACTIVATION')
