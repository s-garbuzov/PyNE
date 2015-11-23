#!/usr/bin/env python

"""
Sample script that retrieves NETCONF device capabilities information
from the Controller
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.controllers.odl.netconf_topology import NETCONFNodeTopoInfo
from Module9.utils.utilities import yaml_cfg_load


if __name__ == "__main__":

    # Read Controller info from the local configuration file
    ctrl_cfg_path = "../config/ctrl.yml"
    ctrl_cfg = yaml_cfg_load(ctrl_cfg_path)
    if(ctrl_cfg is None):
        print("!!!Error, reason: failed to get Controller configuration")
        exit(1)

    # Read NETCONF devices info from the local configuration file
    nc_dev_cfg_path = "../config/netconf.yml"
    nc_dev_cfg = yaml_cfg_load(nc_dev_cfg_path)
    if(nc_dev_cfg is None):
        print("!!!Error, reason: failed to get NETCONF devices configuration")
        exit(1)

    # Allocate object instance that represents the Controller
    ctrl = ODLController(ctrl_cfg['ip_addr'], ctrl_cfg['http_port'],
                         ctrl_cfg['admin_name'], ctrl_cfg['admin_pswd'])

    print("\n").strip()
    print("Controller: '%s:%s'" % (ctrl.ip_addr, ctrl.port))
    print("\n").strip()

    # Communicate to the Controller and display the result of communication
    for item in nc_dev_cfg:
        node_id = item['name']
        result = ctrl.netconf_node_topo_info(node_id)
        if(result.status == http.OK):
            assert(isinstance(result.data, NETCONFNodeTopoInfo))
            device_info = result.data
            clist = device_info.capabilities_available
            print("  NETCONF Node '%s'" % node_id)
            print("\n").strip()
            if(clist):
                print("    Available Capabilities:")
                print("\n").strip()
                for item in clist:
                    print "      %s" % item
                print "\n".strip()
            else:
                print("    Available Capabilities: None")
            clist = device_info.capabilities_unavailable
            if(clist):
                print("    Unavailable Capabilities:")
                print "\n".strip()
                for item in clist:
                    print "      %s" % item
                print "\n".strip()
            else:
                print("    Unavailable Capabilities: None")
            print "\n".strip()
        elif(result.status == http.NOT_FOUND):
            print("  '%s' is not found" % node_id)
            print("\n").strip()
        else:
            print("!!!Error, reason: %s" % result.brief)
            print("\n").strip()
