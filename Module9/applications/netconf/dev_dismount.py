#!/usr/bin/env python

"""
Sample script that dismounts NETCONF device from the Controller
"""


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

    success, data = ctrl.netconf_node_unmount(nc_device.node_id)
    if(success):
        print ("Successfully unmounted '%s' device" % nc_device.node_id)
        print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)
