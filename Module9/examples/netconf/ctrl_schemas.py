#!/usr/bin/env python

"""
Sample script that retrieves list of YANG data model schemas
supported by the Controller.
"""

# Python standard library modules
import httplib as http

# third-party modules
import json

# this package local modules
from Module9.controllers.odl.controller import ODLController
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

    result = ctrl.schemas_list(NC_NODE_ID)
    print("\n").strip()
    if(result.status == http.OK):
        data = result.data
        assert(isinstance(data, list))
        print("Controller  : '%s:%s'" % (ctrl.ip_addr, ctrl.port))
        print("Node ID     : '%s'" % NC_NODE_ID)
        print "YANG models :"
        print json.dumps(data, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)
    else:
        print("!!!Error, reason: %s" % result.brief)
#        print("!!!Error, reason: %s" % result.details)
    print("\n").strip()
