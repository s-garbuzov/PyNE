#!/usr/bin/env python

"""
Sample script that requests Controller to return the content
of a particular YANG data model schema.
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

    # Following is a hard-coded value used by the Controller
    # for self-identification as a NETCONF node
    NC_NODE_ID = "controller-config"
    # Allocate object instance that represents the Controller
    ctrl = ODLController(ctrl_cfg['ip_addr'], ctrl_cfg['http_port'],
                         ctrl_cfg['admin_name'], ctrl_cfg['admin_pswd'])

    # Hard coded references to the "network-topology" YANG model data schema
    SCHEMA_ID = "network-topology"
    SCHEMA_VERSION = "2013-10-21"
    # Communicate to the Controller and display the result of communication
    result = ctrl.schema_info(NC_NODE_ID, SCHEMA_ID, SCHEMA_VERSION)
    print("\n").strip()
    if(result.status == http.OK):
        print("Controller : '%s:%s'" % (ctrl.ip_addr, ctrl.port))
        print("Node ID    : '%s'" % NC_NODE_ID)
        print("YANG model : '%s@%s'" % (SCHEMA_ID, SCHEMA_VERSION))
        print "\n".strip()
        print result.data
    else:
        print("!!!Error, reason: %s" % result.brief)
    print("\n").strip()
