#!/usr/bin/env python

"""
Sample script that requests Controller to return list of node identifiers
in the NETCONF topology.
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.utils.utilities import yaml_cfg_load


if __name__ == "__main__":

    # Read Controller info from the local configuration file
    ctrl_cfg_path = "../config/ctrl.yml"
    ctrl_cfg = yaml_cfg_load(ctrl_cfg_path)
    if(ctrl_cfg is None):
        print("!!!Error, reason: failed to get Controller configuration")
        exit(1)

    # Allocate object instance that represents the Controller
    ctrl = ODLController(ctrl_cfg['ip_addr'], ctrl_cfg['http_port'],
                         ctrl_cfg['admin_name'], ctrl_cfg['admin_pswd'])

    # Communicate to the Controller and display the result of communication
    result = ctrl.netconf_nodes_ids()
    print("\n").strip()
    if(result.status == http.OK):
        assert(isinstance(result.data, list))
        print("Controller: '%s:%s'" % (ctrl.ip_addr, ctrl.port))
        print "\n".strip()
        print ("NETCONF Nodes Identifiers:")
        print "\n".strip()
        for item in result.data:
            print "  '%s'" % item
    else:
        print("!!!Error, reason: %s" % result.brief)
    print("\n").strip()
