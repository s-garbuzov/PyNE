#!/usr/bin/env python

"""
Sample script that removes a NETCONF device
from the Controller's configuration.
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController


if __name__ == "__main__":

    IP_ADDR = "172.22.18.70"
    HTTP_PORT = 8181
    UNAME = "admin"
    PSWD = "admin"
    ctrl = ODLController(IP_ADDR, HTTP_PORT, UNAME, PSWD)

    NC_NODE_ID = "vRouter"

    print("\n").strip()
    print("Controller: '%s:%s'" % (IP_ADDR, HTTP_PORT))
    print("NETCONF Node: '%s'" % NC_NODE_ID)

    result = ctrl.netconf_node_is_mounted(NC_NODE_ID)
    node_is_mounted = False
    if(result.status == http.OK):
        node_is_mounted = True
    elif(result.status == http.NOT_FOUND):
        node_is_mounted = False
    else:
        print ("\n").strip()
        print("!!!Error, reason: %s" % result.brief)
        exit(1)

    if(node_is_mounted is False):
        print("\n").strip()
        print("'%s' is not mounted" % NC_NODE_ID)
        print("\n").strip()
    else:
        result = ctrl.netconf_node_unmount(NC_NODE_ID)
        if(result.status == http.OK):
            print("\n").strip()
            print ("Unmounted '%s' device" % NC_NODE_ID)
            print("\n").strip()
        else:
            print("\n").strip()
            print("!!!Error, reason: %s" % result.brief)
            print("\n").strip()
            exit(1)
