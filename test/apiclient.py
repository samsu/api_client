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
    print cli.request('GET_USERGROUPS')
    print "----------"
    message = {
        "name": "test123"
    }
    print cli.request("CREATE_USERGROUPS", **message)
    print cli.request('GET_USERGROUPS')
    print cli.request("DELETE_USERGROUPS", **message)

