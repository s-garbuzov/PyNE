#!/usr/bin/env python

"""
Sample script that requests Controller to return the content
of a particular YANG data model schema supported by given
NETCONF device.
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

    NC_NODE_ID = 'vRouter'
    SCHEMA_ID = "ietf-yang-types"
    SCHEMA_VERSION = "2013-07-15"

    result = ctrl.netconf_node_is_mounted(NC_NODE_ID)
    node_is_mounted = False
    node_is_connected = False
    if(result.status == http.OK):
        node_is_mounted = True
        node = result.data
        if(node.connected):
            node_is_connected = True
    elif(result.status == http.NOT_FOUND):
        node_is_mounted = False
    else:
        print("\n").strip()
        print("!!!Error, reason: %s" % result.brief)
        print("\n").strip()
        exit(1)

    if(node_is_mounted is False):
        print("\n").strip()
        print("'%s' is not mounted" % NC_NODE_ID)
        print("\n").strip()
        exit(1)

    if(node_is_connected is False):
        print("\n").strip()
        print("'%s' is not connected" % NC_NODE_ID)
        print("\n").strip()
        exit(1)

    result = ctrl.schema_info(NC_NODE_ID, SCHEMA_ID, SCHEMA_VERSION)
    if(result.status == http.OK):
        print("\n").strip()
        print("Controller : '%s:%s'" % (ctrl.ip_addr, ctrl.port))
        print("Node ID    : '%s'" % NC_NODE_ID)
        print("YANG model : '%s@%s'" % (SCHEMA_ID, SCHEMA_VERSION))
        print "\n".strip()
        print result.data
        print("\n").strip()
    else:
        print("\n").strip()
        print("!!!Error, reason: %s" % result.brief)
        print("\n").strip()
        exit(1)
