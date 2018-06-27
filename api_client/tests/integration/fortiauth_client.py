#!/usr/bin/env python

import time
import os
import inspect

import api_client.fortiauth_client as client


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
    print "----TESTING USERGROUPS------"
    cli.request('GET_USERGROUPS')
    cli.request("CREATE_USERGROUP", **message)
    cli.request('GET_USERGROUPS', **message)
    cli.request("DELETE_USERGROUP", **message)

    print "----TESTING USERS------"
    message = {
        "username": "test_1"
    }

    cli.request("GET_USERS", **message)
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
    cli.request("CREATE_USER", **add_message)
    res = cli.request("GET_USERS", **message)
    id = str(res[0]['id'])
    cli.request("MODIFY_USER", id=id, first='changed')
    cli.request("GET_USERS",  **message)
    cli.request("DELETE_USER", id=id)

    message = {
        "status": "available"
    }
    print "----TESTING FORTITOKENS------"
    cli.request("GET_FORTITOKENS", **message)
    cli.request("GET_FORTITOKENS")
