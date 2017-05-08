#!/usr/bin/env python

import time
import os
import inspect

import api_client.client as client


FortiosApiClient=client.FortiosApiClient

if __name__ == "__main__":
    api = [("10.160.37.98", 443, True)]
    user = "admin"
    password = "lRFUJKlKYTOM17fK6UYP8lxVS84bEj3N1gkUvUZ"
    cli = FortiosApiClient(api, user, password)
    cli.request('GET_USERGROUPS')
    print "----------"
    message = {
        "name": "ext_4093",
        "vlanid": 4093,
        "vdom": "root",
        "interface": "port1",
        "ip": "192.168.30.254 255.255.255.0"
    }
    #cli.request("ADD_VLAN_INTERFACE", message)
    message = {
        "name": "port5",
        "vdom": "root",
        "ip": "192.168.40.254 255.255.255.0"
        #"secondaryips": ["192.168.20.200 255.255.255.0", ]
        #"secondaryips": []
    }
    #print cli.request("SET_VLAN_INTERFACE", message)
    message = {
        "name": "ext_4093"
    }

    #print cli.request("GET_VLAN_INTERFACE", message)
