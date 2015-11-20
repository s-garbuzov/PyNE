#!/usr/bin/env python

"""
Sample script that requests Controller to return the content
of a particular YANG data model schema.
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController


if __name__ == "__main__":

    CTRL_IP_ADDR = "172.22.18.70"
    CTRL_HTTP_PORT = 8181
    CTRL_UNAME = "admin"
    CTRL_PSWD = "admin"
    ctrl = ODLController(CTRL_IP_ADDR, CTRL_HTTP_PORT, CTRL_UNAME, CTRL_PSWD)

    node_id = 'controller-config'
    schema_id = "network-topology"
    schema_version = "2013-10-21"
    result = ctrl.schema_info(node_id, schema_id, schema_version)
    print("\n").strip()
    if(result.status == http.OK):
        print("Controller : '%s:%s'" % (ctrl.ip_addr, ctrl.port))
        print("Node ID    : '%s'" % node_id)
        print("YANG model : '%s@%s'" % (schema_id, schema_version))
        print "\n".strip()
        print result.data
    else:
        print("!!!Error, reason: %s" % result.brief)
#        print("!!!Error, reason: %s" % result.details)
    print("\n").strip()
