#!/usr/bin/env python

import time
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from client import FortiosApiClient as FortiosApiClient

if __name__ == "__main__":
    api = [("10.160.37.98", 443, True)]
    user = "admin"
    password = "lRFUJKlKYTOM17fK6UYP8lxVS84bEj3N1gkUvUZ"
    cli = FortiosApiClient(api, user, password)
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
