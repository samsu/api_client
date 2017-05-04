#!/usr/bin/env python

import time
from client import FortiosApiClient as FortiosApiClient

if __name__ == "__main__":
    api = [("10.160.37.98", 443, True)]
    user = "admin"
    password = ""
    cli = FortiosApiClient(api, user, password)
    print "----------"
    message = {
        "name": "ext_4093",
        "vlanid": 4093,
        "vdom": "root",
        "interface": "port1",
        "ip": "192.168.30.254 255.255.255.0"
    }
    cli.request("ADD_VLAN_INTERFACE", message)
    message = {
        "name": "port5",
        "vdom": "root",
        "ip": "192.168.40.254 255.255.255.0"
        #"secondaryips": ["192.168.20.200 255.255.255.0", ]
        #"secondaryips": []
    }
    print cli.request("SET_VLAN_INTERFACE", message)
    message = {
        "name": "ext_4093"
    }

    #print cli.request("GET_VLAN_INTERFACE", message)

