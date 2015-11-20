#!/usr/bin/env python

"""
Sample script that requests Controller to return list of topology identifiers.
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

    result = ctrl.topology_ids()
    print("\n").strip()
    if(result.status == http.OK):
        assert(isinstance(result.data, list))
        print("Controller: '%s:%s'" % (ctrl.ip_addr, ctrl.port))
        print "\n".strip()
        print ("Network Topology Identifiers:")
        print "\n".strip()
        for item in result.data:
            print "  '%s'" % item
    else:
        print("!!!Error, reason: %s" % result.brief)
#        print("!!!Error, reason: %s" % result.details)
    print("\n").strip()
