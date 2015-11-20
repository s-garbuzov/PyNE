#!/usr/bin/env python

"""
Sample script that retrieves NETCONF capabilities of the Controller
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.controllers.odl.netconf_topology import NETCONFNodeTopoInfo
from Module9.utils.utilities import yaml_cfg_load


if __name__ == "__main__":

    NC_NODE_ID = "controller-config"
    ctrl_cfg_path = "../config/ctrl.yml"
    ctrl_cfg = yaml_cfg_load(ctrl_cfg_path)
    if(ctrl_cfg is None):
        print("!!!Error: failed to get Controller configuration)")
        exit(1)

    ctrl = ODLController(ctrl_cfg['ip_addr'], ctrl_cfg['http_port'],
                         ctrl_cfg['admin_name'], ctrl_cfg['admin_pswd'])

    print("\n").strip()
    print("Controller: '%s:%s'" % (ctrl.ip_addr, ctrl.port))
    print("\n").strip()
    print("  NETCONF Node '%s'" % NC_NODE_ID)
    print("\n").strip()

    result = ctrl.netconf_node_topo_info(NC_NODE_ID)
    if(result.status == http.OK):
        assert(isinstance(result.data, NETCONFNodeTopoInfo))
        device_info = result.data
        clist = device_info.capabilities_available
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
