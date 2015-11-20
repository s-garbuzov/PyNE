#!/usr/bin/env python

"""
Sample script that retrieves NETCONF device capabilities
information from the Controller
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.controllers.odl.netconf_topology import NETCONFNodeTopoInfo


if __name__ == "__main__":

    CTRL_IP_ADDR = "172.22.18.70"
    CTRL_HTTP_PORT = 8181
    CTRL_UNAME = "admin"
    CTRL_PSWD = "admin"
    ctrl = ODLController(CTRL_IP_ADDR, CTRL_HTTP_PORT, CTRL_UNAME, CTRL_PSWD)

    NC_NODE_ID = "vRouter"

    print("\n").strip()
    print("Controller: '%s:%s'" % (ctrl.ip_addr, ctrl.port))
    print("\n").strip()
    print("  NETCONF Node '%s'" % NC_NODE_ID)

    result = ctrl.netconf_node_topo_info(NC_NODE_ID)
    if(result.status == http.OK):
        assert(isinstance(result.data, NETCONFNodeTopoInfo))
        device_info = result.data
        clist = device_info.capabilities_available
        print("\n").strip()
        if(clist):
            print("    Available Capabilities:")
            print("\n").strip()
            for item in clist:
                print "      %s" % item
            print "\n".strip()
        clist = device_info.capabilities_unavailable
        if(clist):
            print("    Unavailable Capabilities:")
            print "\n".strip()
            for item in clist:
                print "      %s" % item
            print "\n".strip()
        print "\n".strip()
    elif(result.status == http.NOT_FOUND):
        print("\n").strip()
        print("'%s' is not found" % NC_NODE_ID)
        print("\n").strip()
    else:
        print("\n").strip()
        print("!!!Error, reason: %s" % result.brief)
        print("\n").strip()
#        print("!!!Error, reason: %s" % result.details)
        exit(1)
