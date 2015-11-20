#!/usr/bin/env python


# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.controllers.odl.netconf_topology import NETCONFTopoInfo


if __name__ == "__main__":

    CTRL_IP_ADDR = "172.22.18.70"
    CTRL_HTTP_PORT = 8181
    CTRL_UNAME = "admin"
    CTRL_PSWD = "admin"
    ctrl = ODLController(CTRL_IP_ADDR, CTRL_HTTP_PORT, CTRL_UNAME, CTRL_PSWD)

    topo_id = 'topology-netconf'

    print("\n").strip()
    print("Controller: '%s:%s'" % (CTRL_IP_ADDR, CTRL_HTTP_PORT))
    print("\n").strip()
    print("NETCONF Topology information")

    result = ctrl.topology_info(topo_id)
    if(result.status == http.OK):
        assert(isinstance(result.data, NETCONFTopoInfo))
        topo_info = result.data
        print("\n").strip()
        nodes_list = topo_info.nodes_list
        print("  Topology ID : '%s'" % topo_info.identifier)
        print("  Nodes Count : %s" % len(nodes_list))
        nodes_ids = topo_info.nodes_ids
        g = 2
        chunks = [nodes_ids[x:x + g] for x in xrange(0, len(nodes_ids), g)]
        s = "Nodes IDs"
        print("  Nodes IDs   :"),
        for i in range(0, len(chunks)):
            n = 0 if i == 0 else len(s) + 9
            print "%s%s" % (" " * n, ", ".join(chunks[i]))

        for node in nodes_list:
            print("\n").strip()
            print("  Node '%s'" % node.identifier)
            print("\n").strip()
            print("    IP Address        : %s" % node.ip_addr)
            print("    TCP Port Number   : %s" % node.port_num)
            print("    Connection Status : %s" %
                  "connected" if node.connected else "disconnected")
        print("\n").strip()
    else:
        print("\n").strip()
        print("!!!Error, reason: %s" % result.brief)
        print("\n").strip()
#        print("!!!Error, reason: %s" % result.details)
        exit(1)
