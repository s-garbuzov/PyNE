#!/usr/bin/env python

"""
Sample script that determines NETCONF device configuration (mounted/unmounted)
status on the Controller
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController


if __name__ == "__main__":

    CTRL_IP_ADDR = "172.22.18.70"
    CTRL_HTTP_PORT = 8181
    CTRL_UNAME = "admin"
    CTRL_PSWD = "admin"
    ctrl = ODLController(CTRL_IP_ADDR, CTRL_HTTP_PORT, CTRL_UNAME, CTRL_PSWD)

    NC_NODE_ID = "vRouter"
    result = ctrl.netconf_node_is_mounted(NC_NODE_ID)
    print("\n").strip()
    if(result.opcode == http.OK):
        print("'%s' is mounted" % NC_NODE_ID)
    elif(result.opcode == http.NOT_FOUND):
        print("'%s' is not mounted" % NC_NODE_ID)
    else:
        print("!!!Error, reason: %s" % result.brief)
#        print("!!!Error, reason: %s" % result.details)
    print("\n").strip()
