#!/usr/bin/env python3

import api_client.fas_client as client


ApiClient = client.FASApiClient

if __name__ == "__main__":
    api = [("127.0.0.1", 443, True)]
    # CA
    # replace the sn and cert with your own in the test
    sn = 'Fxxxxxxxxx'
    key_file = "./xxx.key"
    cert_file = "./xxx.crt"
    ca_file = "./xxx.cer"

    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file)
    print("----TESTING API client with CA certificate ------")
    res = cli.request('GET_USER', sn=sn, vdom='root')
