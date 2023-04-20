#!/usr/bin/env python

import api_client.forticare_client as client

ApiClient = client.FortiCareApiClient


if __name__ == "__main__":
    api = [("127.0.0.1", 443, True)]
    # replace the email and
    email = "***@***.com"
    # Sub CA
    print("----TESTING API client with Sub CA certificate ------")
    # replace related cert information with your own in the test
    key_file = "./xxx.key"
    cert_file = "./xxx.crt"
    ca_file = "./xxx.pem"
    server_hostname = "fortinet-ca2.fortinet.com"
    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file,
                    ssl_sni=server_hostname)
    cli.request('GET_ACCOUNT', email=email)

    # CA
    print("----TESTING API client with CA certificate ------")
    # replace related cert information with your own in the test
    key_file = "./xxx.key"
    cert_file = "./xxx.crt"
    ca_file = "./xxx.pem"
    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file)
    cli.request('GET_ACCOUNT', email=email)
