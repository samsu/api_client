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
        "username": "test_abc"
    }
    import pdb;pdb.set_trace()
    print cli.request("GET_USERS", username='test1')
    #print cli.request("CREATE_USER", username='test1')
    print cli.request("GET_USERS", username='test1')
    print cli.request("MODIFY_USER", id='3', first='changed')
    print cli.request("GET_USERS", username='test1')
    print cli.request("DELETE_USER", id='3')

