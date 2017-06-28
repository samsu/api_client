#!/usr/bin/env python

import time
import os
import inspect

import api_client.client as client


ApiClient=client.FortiAuthApiClient

if __name__ == "__main__":
    api = [("10.160.37.98", 443, True)]
    user = "admin"
    password = "slRFUJKlKYTOM17fK6UYP8lxVS84bEj3N1gkUvUZ"
    cli = ApiClient(api, user, password)
    #print "----TESTING USER_GROUPS------"
    message = {
        "name": "test123"
    }
    #print cli.request('GET_USERGROUPS')
    #print cli.request("CREATE_USERGROUP", **message)
    #print cli.request('GET_USERGROUP', **message)
    #print cli.request("DELETE_USERGROUP", **message)

    print "----TESTING USERS------"
    message = {
        "username": "test_1"
    }
    import pdb;pdb.set_trace()
    print cli.request("GET_USERS", **message)
    add_message = {
        "username": "test_1",
        "token_auth": "true",
        "ftk_only": "false",
        "ftm_act_method": "email",
        "token_type": "sms",
        "email": "sansu@fortinet.com",
        "mobile_number": "+1-4085026006",
        "active": "true"
    }
    print cli.request("CREATE_USER", **add_message)
    res = cli.request("GET_USERS", **message)
    print res
    id = str(res[0]['id'])
    print cli.request("MODIFY_USER", id=id, first='changed')
    print cli.request("GET_USERS",  **message)
    print cli.request("DELETE_USER", id=id)

    message = {
        "status": "available"
    }
    print cli.request("GET_FORTITOKENS", **message)
    print cli.request("GET_FORTITOKENS")
