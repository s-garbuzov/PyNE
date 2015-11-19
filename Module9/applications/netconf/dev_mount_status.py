#!/usr/bin/env python

"""
Sample script that determines NETCONF device configuration (mounted/unmounted)
status on the Controller
"""

# this package local modules
from Module9.controllers.odl.controller import ODLController

if __name__ == "__main__":

    CTRL_IP_ADDR = "172.22.18.70"
    CTRL_HTTP_PORT = 8181
    CTRL_UNAME = "admin"
    CTRL_PSWD = "admin"
    ctrl = ODLController(CTRL_IP_ADDR, CTRL_HTTP_PORT, CTRL_UNAME, CTRL_PSWD)

    NC_NODE_ID = "vRouter"
    status = ctrl.netconf_node_is_mounted(NC_NODE_ID)
    print("NETCONF device '%s' is %s" %
          (NC_NODE_ID, 'mounted' if(status) else 'not found'))
