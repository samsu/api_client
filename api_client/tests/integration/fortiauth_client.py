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

    print "----TESTING SYSTEMINFO------"
    cli.request("GET_SYSTEMINFO")

    print "----TESTING FTPSERVERS------"
    message = {
        "name": "test_ftpserver",
        "address": "127.0.0.1",
        "conn_type": "ftp",
        "port": 21
    }
    cli.request("CREATE_FTPSERVER", **message)
    cli.request("GET_FTPSERVERS")
    cli.request("GET_FTPSERVERS", id="1")
    cli.request("DELETE_FTPSERVER", id="1")
    cli.request("CREATE_FTPSERVER", **message)

    print "----TEST SCHEDULED BACKUP SETTINGS----"
    message = {
        "ftp": "test_ftpserver",
        "frequency": "monthly",
        "time": "23:59:59",
        "enabled": "true"
    }
    res = cli.request("GET_SCHEDULED_BACKUP_SETTING")
    res = cli.request("CREATE_SCHEDULED_BACKUP_SETTING", **message)
    cli.request("GET_SCHEDULED_BACKUP_SETTING")
    message['enabled'] = "false"
    cli.request("MODIFY_SCHEDULED_BACKUP_SETTING", **message)

    print "----TEST BACKUP AND RECOVERY----"
    res = cli.request("BACKUP_CONFIG")
