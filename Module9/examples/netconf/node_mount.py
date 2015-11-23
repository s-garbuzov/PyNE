#!/usr/bin/env python

"""
Sample script that mounts list of NETCONF devices specified in the local
configuration file to the NETCONF topology on the Controller.
"""

# Python standard library modules
import httplib as http

# this package local modules
from Module9.controllers.odl.controller import ODLController
from Module9.devices.netconf.common import NETCONFDevice
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
        result = ctrl.netconf_node_is_mounted(node_id)
        if(result.status == http.SERVICE_UNAVAILABLE or
           result.status == http.UNAUTHORIZED):
            print("!!!Error: Controller access failure, reason: %s"
                  % result.brief)
            print ("\n").strip()
            break
        elif(result.status == http.OK):
            print("  '%s' is already mounted" % node_id)
            print ("\n").strip()
        elif(result.status == http.NOT_FOUND):
            nc_device = NETCONFDevice(item['name'],
                                      item['ip_addr'], item['port'],
                                      item['admin_name'], item['admin_pswd'])
            result = ctrl.netconf_node_mount(nc_device)
            if(result.status == http.OK):
                print ("  Mounted '%s' device" % nc_device.node_id)
                print ("\n").strip()
            else:
                print("!!!Error, reason: %s" % result.brief)
                print ("\n").strip()
        else:
            print("!!!Error, reason: %s" % result.brief)
            print ("\n").strip()
