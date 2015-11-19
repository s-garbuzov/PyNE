#!/usr/bin/env python

"""
Sample script that retrieves NETCONF device information from the Controller
"""

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.controllers.odl.netconf_topology import NETCONFNodeTopoInfo
from Module9.devices.netconf.common import NETCONFDevice


if __name__ == "__main__":

    CTRL_IP_ADDR = "172.22.18.70"
    CTRL_HTTP_PORT = 8181
    CTRL_UNAME = "admin"
    CTRL_PSWD = "admin"
    ctrl = ODLController(CTRL_IP_ADDR, CTRL_HTTP_PORT, CTRL_UNAME, CTRL_PSWD)

    NC_NODE_ID = "vRouter"
    success, data = ctrl.netconf_node_topo_info(NC_NODE_ID)
    if(success):
        assert(isinstance(data, NETCONFNodeTopoInfo))
        print "\n".strip()
#        print("  NETCONF device '%s' topology information" % nc_device.node_id)
        print("  NETCONF topology information - '%s'" % NC_NODE_ID)
        print "\n".strip()
        device_info = data
        print("    Node ID           : %s" % device_info.identifier)
        print("    IP Address        : %s" % device_info.ip_addr)
        print("    TCP Port Number   : %s" % device_info.port_num)
        print("    Connection Status : %s" %
              'connected' if device_info.connected else 'disconnected')
        print "\n".strip()
        clist = device_info.capabilities_available
        if(clist):
            print("    Available Capabilities:")
            print "\n".strip()
#            print("      %s" % ('-'*78))
            for item in clist:
                print "      %s" % item
            print "\n".strip()
        clist = device_info.capabilities_unavailable
        if(clist):
            print("    Unavailable Capabilities:")
            print "\n".strip()
#            print("      %s" % ('-'*78))
            for item in clist:
                print "      %s" % item
            print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)
