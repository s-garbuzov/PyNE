#!/usr/bin/env python

"""
Sample script that retrieves list of YANG model schemas
supported by the Controller.
"""

# Python standard library modules
import httplib as http

# third-party modules
import json

# this package local modules
from Module9.controllers.odl.controller import ODLController


if __name__ == "__main__":

    CTRL_IP_ADDR = "172.22.18.70"
    CTRL_HTTP_PORT = 8181
    CTRL_UNAME = "admin"
    CTRL_PSWD = "admin"
    ctrl = ODLController(CTRL_IP_ADDR, CTRL_HTTP_PORT, CTRL_UNAME, CTRL_PSWD)

    node_id = 'controller-config'
    result = ctrl.schemas_list(node_id)
    print("\n").strip()
    if(result.status == http.OK):
        data = result.data
        assert(isinstance(data, list))
        print("Controller  : '%s:%s'" % (ctrl.ip_addr, ctrl.port))
        print("Node ID     : '%s'" % node_id)
        print "YANG models :"
        print json.dumps(data, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)
    else:
        print("!!!Error, reason: %s" % result.brief)
#        print("!!!Error, reason: %s" % result.details)
    print("\n").strip()
