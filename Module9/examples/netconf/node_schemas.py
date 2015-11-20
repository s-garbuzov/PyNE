#!/usr/bin/env python

"""
Sample script that request Controller to return list of
YANG data model schemas supported by given NETCONF device.
"""

# Python standard library modules
import httplib as http

# third-party modules
import json

# this package local modules
from Module9.controllers.odl.controller import ODLController


if __name__ == "__main__":

    CTRL_IP_ADDR = "172.22.18.70"
    CTRL_HTTP_PORT = 8181
    CTRL_UNAME = "admin"
    CTRL_PSWD = "admin"
    ctrl = ODLController(CTRL_IP_ADDR, CTRL_HTTP_PORT, CTRL_UNAME, CTRL_PSWD)

    NC_NODE_ID = 'vRouter'

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

    result = ctrl.schemas_list(NC_NODE_ID)
    if(result.status == http.OK):
        data = result.data
        assert(isinstance(data, list))
        print("\n").strip()
        print("Controller  : '%s:%s'" % (ctrl.ip_addr, ctrl.port))
        print("Node ID     : '%s'" % NC_NODE_ID)
        print "YANG models :"
        print json.dumps(data, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)
        print("\n").strip()
    elif(result.status == http.NOT_FOUND):
        print("\n").strip()
        print("'%s' is not found" % NC_NODE_ID)
        print("\n").strip()
    else:
        print("\n").strip()
        print("!!!Error, reason: %s" % result.brief)
        print("\n").strip()
        exit(1)
