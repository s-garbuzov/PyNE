#!/usr/bin/env python

# third-party modules
import json
from requests import (request, RequestException)
from requests.auth import HTTPBasicAuth

# this package local modules
from Module9.controllers.odl.netconf_topology import NETCONFNodeTopoInfo
from Module9.devices.netconf.common import NETCONFDevice


class ODLController(object):
    """Represents an instance of Opendaylight Controller."""

    def __init__(self, ip_addr, http_port,
                 admin_name, admin_password, timeout=5):
        """ODLController object constructor.

        :param ip_addr: (required)
            IP address of the Controller.
        :param http_port: (required)
            HTTP port number on the Controller.
        :param admin_name: (required)
            administrative user login name.
        :param admin_password: (required)
            administrative user login password.
        :param timeout: (optional)
            communication timeout.
        """

        self._ip_addr = ip_addr
        self._http_port = http_port
        self._uname = admin_name
        self._pswd = admin_password
        self._timeout = timeout

    def description(self):
        '''
        d = {'ip_addr': self._ip_addr, 'http_port': self._http_port,
             'admin_name': self._uname, 'admin_password': self._pswd,
             'timeout': self._timeout}
        return d
        '''
        s = ("ip_addr={}, http_port={}, "
             "admin_name={}, admon_password={}, "
             "timeout={}").format(self._ip_addr, self._http_port,
                                  self._uname, self._pswd,
                                  self._timeout)
        return s

    def _http_request(self, method, url, **kwargs):
        """Sends an HTTP request to the Controller
        and returns the result of communication.
        """
        return request(method, url, **kwargs)

    def _restconf_get(self, path, headers=None):
        """Sends a RESTCONF GET request to the Controller
        and returns the result of communication.
        NOTE: RESTCONF protocol uses HTTP methods to identify
             the Create, Retrieve, Update, Delete operation
             for a particular resource.
        """
        url_prefix = ("http://{}:{}/restconf").format(self._ip_addr,
                                                      self._http_port)
        url = url_prefix
        if(path.startswith('/') is False):
            url += "/"
        url += path
        try:
            response = \
                self._http_request(method='GET', url=url, headers=headers,
                                   auth=HTTPBasicAuth(self._uname, self._pswd),
                                   timeout=self._timeout)
            return response
            """
            method = 'GET'
            response = request(method, url, data=data, headers=headers,
                               auth=HTTPBasicAuth(self._uname, self._pswd),
                               timeout=self._timeout)
            print "<<<<<<<<"
            print vars(response)
            print response.status_code
#            print requests.codes
            print ">>>>>>>>"
            response.raise_for_status()
            return response.content
            """
#        except (ConnectionError, Timeout) as e:
#        # ConnectionError; Timeout; HTTPError, TooManyRedirects
#        except (ConnectionError, Timeout, HTTPError, TooManyRedirects) as e:
#            print("!!!Error: (%s)" % (e.message))
#            print("!!!Error: (%s)" % (e.filename))
#            print("!!!Error: " + repr(e))
#            print("!!!Error: type=%s, reason %s" % (type(e), dir(e)))
        except RequestException as e:
            print("!!!Error: (%s)" % (repr(e)))
            return None

    def _restconf_post(self, path, payload=None, headers=None):
        """Sends a RESTCONF POST request to the Controller
        and returns the result of communication.
        NOTE: RESTCONF protocol uses HTTP methods to identify
             the Create, Retrieve, Update, Delete operation
             for a particular resource.
        """
        url_prefix = ("http://{}:{}/restconf").format(self._ip_addr,
                                                      self._http_port)
        url = url_prefix
        if(path.startswith('/') is False):
            url += "/"
        url += path
        try:
            response = \
                self._http_request(method='POST', url=url,
                                   data=payload, headers=headers,
                                   auth=HTTPBasicAuth(self._uname, self._pswd),
                                   timeout=self._timeout)
            return response
        except RequestException as e:
            print("!!!Error: (%s)" % (repr(e)))
            return None

    def _restconf_put(self, path, payload=None, headers=None):
        """Sends a RESTCONF PUT request to the Controller
        and returns the result of communication.
        NOTE: RESTCONF protocol uses HTTP methods to identify
             the Create, Retrieve, Update, Delete operation
             for a particular resource.
        """
        url_prefix = ("http://{}:{}/restconf").format(self._ip_addr,
                                                      self._http_port)
        url = url_prefix
        if(path.startswith('/') is False):
            url += "/"
        url += path
        pass

    def _restconf_delete(self, path, headers=None):
        """Sends a RESTCONF DELETE request to the Controller
        and returns the result of communication.
        NOTE: RESTCONF protocol uses HTTP methods to identify
             the Create, Retrieve, Update, Delete operation
             for a particular resource.
        """
        url_prefix = ("http://{}:{}/restconf").format(self._ip_addr,
                                                      self._http_port)
        url = url_prefix
        if(path.startswith('/') is False):
            url += "/"
        url += path
        try:
            response = \
                self._http_request(method='DELETE', url=url, headers=headers,
                                   auth=HTTPBasicAuth(self._uname, self._pswd),
                                   timeout=self._timeout)
            return response
        except RequestException as e:
            print("!!!Error: (%s)" % (repr(e)))
            return None

    def schemas_list(self):
        """Return list of all YANG data model schemas supported
        by the Controller."""
        success = None
        data = None
        path = ("operational/opendaylight-inventory:nodes/"
                "node/controller-config/yang-ext:mount/"
                "ietf-netconf-monitoring:netconf-state/schemas")
        headers = {'accept': 'application/yang.data+json'}
        response = self._restconf_get(path, headers)
        if(response is None):
            success = False
            data = "Connection error"
        elif(response.status_code == 200):
            try:
                if(response.headers.get('content-type') !=
                        'application/yang.data+json'):
                    raise ValueError("unexpected response content encoding")
                # Deserialize response JSON content to Python object
                d = json.loads(response.content)
                # Extract the data
                data = d['schemas']['schema']
                success = True
            except(Exception) as e:
                success = False
                data = ("Failed to parse response (%s)" % repr(e))
        else:
            success = False
            err_msg = "HTTP error %s" % response.status_code
            if(response.content is not None):
                data = "%s (%s)" % (err_msg, response.content)
            else:
                data = "%s (%s)" % (err_msg, "Internal server error")

        return success, data

    def schema_info(self, identifier, version):
        """Return detailed information about given YANG data model schema.

        :param identifier:
            unique identifier of the schema (name of the YANG module
            or submodule)
        :param str version:
            version of the schema (value of the revision statement in
            the YANG module or submodule)
        """
        pass

    def topology_ids(self):
        success = None
        data = []
        path = ("operational/network-topology:network-topology")
        headers = {'accept': 'application/yang.data+json'}
        response = self._restconf_get(path, headers)
        if(response is None):
            success = False
            data = "Connection error"
        elif(response.status_code == 200):
            try:
                if(response.headers.get('content-type') !=
                        'application/yang.data+json'):
                    raise ValueError("unexpected response content encoding")
                # Deserialize response JSON content to Python object
                d = json.loads(response.content)
                # Extract the data
                topo_list = d['network-topology']['topology']
                topo_list = d['network-topology']['topology']
                for item in topo_list:
                    topo_id = item.get('topology-id')
                    if(topo_id is not None):
                        data.append(topo_id)
                success = True
            except(Exception) as e:
                success = False
                data = ("Failed to parse response (%s)" % repr(e))
        else:
            success = False
            err_msg = "HTTP error %s" % response.status_code
            if(response.content is not None):
                data = "%s (%s)" % (err_msg, response.content)
            else:
                data = "%s (%s)" % (err_msg, "Internal server error")

        return success, data

    def topology_info(self, topo_id):
        success = None
        data = []
        path = ("operational/network-topology:network-topology/"
                "topology/{}").format(topo_id)
        headers = {'accept': 'application/yang.data+json'}
        response = self._restconf_get(path, headers)
        if(response is None):
            success = False
            data = "Connection error"
        elif(response.status_code == 200):
            try:
                if(response.headers.get('content-type') !=
                        'application/yang.data+json'):
                    raise ValueError("unexpected response content encoding")
                # Deserialize response JSON content to Python object
                d = json.loads(response.content)
                # Extract the data
                data = d['topology'][0]
                success = True
            except(Exception) as e:
                success = False
                data = ("Failed to parse response (%s)" % repr(e))
        else:
            success = False
            err_msg = "HTTP error %s" % response.status_code
            if(response.content is not None):
                data = "%s (%s)" % (err_msg, response.content)
            else:
                data = "%s (%s)" % (err_msg, "Internal server error")

        return success, data

    def netconf_nodes_ids(self):
        success = None
        data = []
        path = ("operational/network-topology:network-topology/"
                "topology/topology-netconf")
        headers = {'accept': 'application/yang.data+json'}
        response = self._restconf_get(path, headers)
        if(response is None):
            success = False
            data = "Connection error"
        elif(response.status_code == 200):
            try:
                if(response.headers.get('content-type') !=
                        'application/yang.data+json'):
                    raise ValueError("unexpected response content encoding")
                # Deserialize response JSON content to Python object
                d = json.loads(response.content)
                # Extract the data
                nodes_list = d['topology'][0]['node']
                for item in nodes_list:
                    node_id = item.get('node-id')
                    if(node_id is not None):
                        data.append(node_id)
                success = True
            except(Exception) as e:
                success = False
                data = ("Failed to parse response (%s)" % repr(e))
        else:
            success = False
            err_msg = "HTTP error %s" % response.status_code
            if(response.content is not None):
                data = "%s (%s)" % (err_msg, response.content)
            else:
                data = "%s (%s)" % (err_msg, "Internal server error")

        return success, data

    def netconf_node_mount(self, node):
        success = None
        data = None
        assert(isinstance(node, NETCONFDevice))
        mr = NETCONFMountRequest(node.node_id,
                                 node.ip_addr,
                                 node.port,
                                 node.admin_name,
                                 node.admin_password)
        path = mr.path
        payload = mr.payload
        headers = {'content-type': 'application/yang.data+json',
                   'accept': 'text/json, text/html, application/xml, */*'}
        response = self._restconf_post(path, payload, headers)
        if(response is None):
            success = False
            data = "Connection error"
        elif(response.status_code == 200 or response.status_code == 204):
            success = True
            data = "Success"
        else:
            success = False
            err_msg = "HTTP error %s" % response.status_code
            if(response.content is not None):
                data = "%s (%s)" % (err_msg, response.content)
            else:
                data = "%s (%s)" % (err_msg, "Internal server error")

        return success, data

    def netconf_node_unmount(self, node_id):
        success = None
        data = None
        path = ("config/network-topology:network-topology/"
                "topology/topology-netconf/node/controller-config/"
                "yang-ext:mount/config:modules/"
                "module/odl-sal-netconf-connector-cfg:"
                "sal-netconf-connector/{}").format(node_id)

        response = self._restconf_delete(path)
        if(response is None):
            success = False
            data = "Connection error"
        elif(response.status_code == 200 or response.status_code == 204):
            success = True
            data = "Success"
        else:
            success = False
            err_msg = "HTTP error %s" % response.status_code
            if(response.content is not None):
                data = "%s (%s)" % (err_msg, response.content)
            else:
                data = "%s (%s)" % (err_msg, "Internal server error")

        return success, data

    def netconf_node_is_connected(self, node_id):
        status = False
        success, data = self.netconf_node_topo_info(node_id)
        if(success):
            assert(isinstance(data, NETCONFNodeTopoInfo))
            status = data.connected
        return status

    def netconf_node_is_mounted(self, node_id):
        status = False
        success, data = self.netconf_node_topo_info(node_id)
        if(success):
            assert(isinstance(data, NETCONFNodeTopoInfo))
            status = True
        return status

    def netconf_node_topo_info(self, node_id):
        success = None
        data = None
        path = ("operational/network-topology:network-topology/"
                "topology/topology-netconf/node/{}").format(node_id)
        headers = {'accept': 'application/yang.data+json'}
        response = self._restconf_get(path, headers)
        if(response is None):
            success = False
            data = "Connection error"
        elif(response.status_code == 200):
            try:
                if(response.headers.get('content-type') !=
                        'application/yang.data+json'):
                    raise ValueError("unexpected response content encoding")
                # Deserialize response JSON content to Python object
                d = json.loads(response.content)
                node = d['node'][0]
                print node.keys()
                data = NETCONFNodeTopoInfo(**node)
                success = True
            except(Exception) as e:
                success = False
                data = ("Failed to parse response (%s)" % repr(e))
        else:
            success = False
            err_msg = "HTTP error %s" % response.status_code
            if(response.content is not None):
                data = "%s (%s)" % (err_msg, response.content)
            else:
                data = "%s (%s)" % (err_msg, "Internal server error")

        return success, data

class NETCONFMountRequest(object):
    """Helper class that used for RESTCONF request content preparation
    for mounting NETCONF device on the Controller"""
    def __init__(self, device_name, ip_addr, netconf_port,
                 user_name, user_password):
        _req_template = {
            'name': None,
            'odl-sal-netconf-connector-cfg:address': None,
            'odl-sal-netconf-connector-cfg:port': None,
            'odl-sal-netconf-connector-cfg:username': None,
            'odl-sal-netconf-connector-cfg:password': None,
            ('odl-sal-netconf-connector-cfg:'
             'between-attempts-timeout-millis'): 2000,
            'odl-sal-netconf-connector-cfg:max-connection-attempts': 0,
            'odl-sal-netconf-connector-cfg:event-executor': {
                'type': 'netty:netty-event-executor',
                'name': 'global-event-executor'
            },
            'odl-sal-netconf-connector-cfg:binding-registry': {
                'type': ('opendaylight-md-sal-binding:'
                         'binding-broker-osgi-registry'),
                'name': 'binding-osgi-broker'
            },
            'odl-sal-netconf-connector-cfg:processing-executor': {
                'type': 'threadpool:threadpool',
                'name': 'global-netconf-processing-executor'
            },
            'odl-sal-netconf-connector-cfg:client-dispatcher': {
                'type': 'odl-netconf-cfg:netconf-client-dispatcher',
                'name': 'global-netconf-dispatcher'
            },
            'odl-sal-netconf-connector-cfg:reconnect-on-changed-schema': True,
            'odl-sal-netconf-connector-cfg:connection-timeout-millis': 20000,
            'odl-sal-netconf-connector-cfg:dom-registry': {
                'type': 'opendaylight-md-sal-dom:dom-broker-osgi-registry',
                'name': 'dom-broker'},
            'odl-sal-netconf-connector-cfg:sleep-factor': 1.5,
            'type': 'odl-sal-netconf-connector-cfg:sal-netconf-connector',
            'odl-sal-netconf-connector-cfg:tcp-only': False
        }

        _req_template['name'] = device_name
        _req_template['odl-sal-netconf-connector-cfg:address'] = ip_addr
        _req_template['odl-sal-netconf-connector-cfg:port'] = netconf_port
        _req_template['odl-sal-netconf-connector-cfg:username'] = user_name
        _req_template['odl-sal-netconf-connector-cfg:password'] = user_password
        self.module = [_req_template]

    def _json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @property
    def payload(self):
        return self._json()

    @property
    def path(self):
        path = ("config/network-topology:network-topology/"
                "topology/topology-netconf/node/controller-config/"
                "yang-ext:mount/config:modules")
        return path

if __name__ == '__main__':
    IP_ADDR = "172.22.18.70"
    HTTP_PORT = 8181
    UNAME = "admin"
    PSWD = "admin"
    ctrl = ODLController(IP_ADDR, HTTP_PORT, UNAME, PSWD)

    NC_NODE_ID = "vRouter"
    NC_DEV_IPADDR = "172.22.17.110"
    NC_DEV_PORT = 830
    NC_ADMIN_NAME = "vyatta"
    NC_ADMIN_PSWD = "vyatta"
    nc_device = NETCONFDevice(NC_NODE_ID, NC_DEV_IPADDR, NC_DEV_PORT,
                              NC_ADMIN_NAME, NC_ADMIN_PSWD)

    """
    print nc_device.node_id
    print nc_device.ip_addr
    print nc_device.port
    print nc_device.admin_name
    print nc_device.admin_password
    """

    """
    success, data = ctrl.netconf_device_mount(nc_device)
    if(success):
        print ("Successfully mounted '%s' device" % nc_device.node_id)
        print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)
    """

    success, nc_node_info = ctrl.netconf_device_info(nc_device.node_id)
    data = nc_node_info
    if(success):
        assert(isinstance(data, NETCONFNodeTopoInfo))
        print ("Successfully obtained '%s' device info" % nc_device.node_id)
        device_info = data
        print vars(device_info)
        print device_info.connected
        print device_info.ip_addr
        print device_info.port_num
        print "Capabilities:"
        clist = device_info.capabilities
        for item in clist:
            print "  %s" % item
#        print clist
#        l = ["\n".join(clist)]
#        print l
#        s = "\n".join(clist)
#        print s.ljust(5)
#        s = l
#        print "%s" % l
#        print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)







    """
    success, data = ctrl.netconf_device_unmount(nc_device.node_id)
    if(success):
        print ("Successfully unmounted '%s' device" % nc_device.node_id)
        print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)
    """

    """
    success, data = ctrl.netconf_device_ids()
    if(success):
        assert(isinstance(data, list))
        print "\n".strip()
        print ("NETCONF Nodes Identifiers:")
        for item in data:
            print "  '%s'" % item
        print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)
    """

    """
    topo_id = "topology-netconf"
    success, data = ctrl.topology_info(topo_id)
    if(success):
#        assert(isinstance(data, list))
        print "\n".strip()
        print ("Network Topology Info - '%s':" % topo_id)
        print json.dumps(data, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)
        print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)
    """

    """
    success, data = ctrl.topology_ids()
    if(success):
        assert(isinstance(data, list))
        print ("Network Topology Identifiers:")
        for item in data:
            print "  '%s'" % item
        print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)
    """
    """
    success, data = ctrl.schemas_list()
    if(success):
        assert(isinstance(data, list))
        print "YANG data model schemas:"
        print json.dumps(data, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)
        print "\n".strip()
    else:
        print("!!!Error, reason: [%s]" % data)
    """
