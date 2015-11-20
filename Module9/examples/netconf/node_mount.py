#!/usr/bin/env python

"""
Sample script that adds a NETCONF device
to the Controller's configuration.
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.devices.netconf.common import NETCONFDevice


if __name__ == "__main__":

    IP_ADDR = "172.22.18.70"
    HTTP_PORT = 8181
    UNAME = "admin"
    PSWD = "admin"
    ctrl = ODLController(IP_ADDR, HTTP_PORT, UNAME, PSWD)

    NC_NODE_ID = "vRouter"
    NC_DEV_IPADDR = "172.22.17.110"
    NC_DEV_PORT = 830
    NC_ADMIN_NAME = "vyatta"
    NC_ADMIN_PSWD = "vyatta"
    nc_device = NETCONFDevice(NC_NODE_ID, NC_DEV_IPADDR, NC_DEV_PORT,
                              NC_ADMIN_NAME, NC_ADMIN_PSWD)

    print("\n").strip()
    print("Controller: '%s:%s'" % (IP_ADDR, HTTP_PORT))
    print("NETCONF Node: '%s'" % nc_device.node_id)

    result = ctrl.netconf_node_is_mounted(nc_device.node_id)
    node_is_mounted = False
    if(result.status == http.OK):
        node_is_mounted = True
    elif(result.status == http.NOT_FOUND):
        node_is_mounted = False
    else:
        print ("\n").strip()
        print("!!!Error, reason: %s" % result.brief)
        print ("\n").strip()
        exit(1)

    if(node_is_mounted):
        print("\n").strip()
        print("'%s' is already mounted" % NC_NODE_ID)
        print ("\n").strip()
    else:
        result = ctrl.netconf_node_mount(nc_device)
        if(result.status == http.OK):
            print("\n").strip()
            print ("Mounted '%s' device" % nc_device.node_id)
            print ("\n").strip()
        else:
            print("\n").strip()
            print("!!!Error, reason: %s" % result.brief)
            print ("\n").strip()
            exit(1)
