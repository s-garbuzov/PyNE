#!/usr/bin/env python


# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.controllers.odl.netconf_topology import NETCONFTopoInfo
from Module9.utils.utilities import yaml_cfg_load


if __name__ == "__main__":

    NC_TOPO_ID = 'topology-netconf'
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
    print("NETCONF Topology information")

    result = ctrl.topology_info(NC_TOPO_ID)
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
