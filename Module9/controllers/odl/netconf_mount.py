
# third-party modules
import json


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
