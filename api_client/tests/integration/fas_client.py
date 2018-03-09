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
    res = cli.request('GET_ACTIVATION', sn='FG60DP4615001748', vdom='root')
    print "GET_ACTIVATION = ", res
    if not res:
        res = cli.request('ADD_ACTIVATION', sn='FG60DP4615001748',
                          vdom='root', namespace='default')
        print "ADD_ACTIVATION = ", res
    if isinstance(res, list):
        res_delete = []
        for record in res:
            _res = cli.request('DELETE_ACTIVATION', id=record['id'])
            res_delete.append(_res)
    elif isinstance(res, dict):
        res_delete = cli.request('DELETE_ACTIVATION', id=res['id'])
    print "DELETE_ACTIVATION = ", res_delete
