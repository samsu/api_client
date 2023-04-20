#!/usr/bin/env python3

import time
import os
import inspect

import api_client.fortiauth_client as client


ApiClient=client.FortiAuthApiClient

if __name__ == "__main__":
    api = [("127.0.0.1", 443, True)]
    # replace the user and password with your own
    user = "test"
    password = "************************"
    cli = ApiClient(api, user, password)

    print("----TESTING USERGROUPS------")
    message = {
        "name": "test123"
    }
    cli.request('GET_USERGROUPS')
    cli.request("CREATE_USERGROUP", **message)
    cli.request('GET_USERGROUPS', **message)
    cli.request("DELETE_USERGROUP", **message)
