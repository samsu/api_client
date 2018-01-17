#!/usr/bin/env python

import api_client.fas_client as client


ApiClient = client.FASApiClient

if __name__ == "__main__":
    api = [("10.160.37.61", 443, True)]
    # CA
    print "----TESTING API client with CA certificate ------"
    # sn is 'FG60DP4615001748' in the test
    key_file = "/root/fgt/box/fgt_b.key"
    cert_file = "/root/fgt/box/fgt_b.crt"
    ca_file = "/root/fgt/box/test_root_Fortinet_CA.cer"

    cli = ApiClient(api, key_file=key_file,
                    cert_file=cert_file, ca_file=ca_file)
    print cli.request('GET_ACTIVATION', sn='FG60DP4615001748')
    print cli.request('ADD_ACTIVATION', sn='FG60DP4615001748', vdom='root',
                      namespace='default')
    #print cli.request('GET_ACTIVATION', sn='FG60DP4615001748')
    #print cli.request('DELETE_ACTIVATION')
