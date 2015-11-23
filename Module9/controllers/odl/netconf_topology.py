"""
Helper classes for parsing NETCONF topology information.
"""

# this package local modules
# from Module9.utils.utilities import dbg_trace_print


class NETCONFTopoInfo(object):
    """Class that is used to parse NETCONF topology information
    obtained from the Controller's topologies data tree."""
    def __init__(self, **kwargs):
        self.nodes = []
        prefix = "netconf-node-topology:"
        for k, v in kwargs.items():
            if(isinstance(k, basestring)):
                k = k.replace(prefix, "").replace("-", "_")
            if(k == 'node'):
                for n in v:
                    data = NETCONFNodeTopoInfo(**n)
                    self.nodes.append(data)
            else:
                setattr(self, k, v)

    @property
    def identifier(self):
        if hasattr(self, 'topology_id'):
            return self.topology_id
        else:
            # dbg_trace_print("!!!Warning: missing expected attribute")
            return None

    @property
    def nodes_ids(self):
        node_ids = []
        for node in self.nodes:
            node_ids.append(node.identifier)
        return node_ids

    @property
    def nodes_list(self):
        return self.nodes


class NETCONFNodeTopoInfo(object):
    """Class that is used to parse NETCONF node information
    obtained from the Controller's topologies data tree."""
    def __init__(self, **kwargs):
        prefix = "netconf-node-topology:"
        for k, v in kwargs.items():
            if(isinstance(k, basestring)):
                k = k.replace(prefix, "").replace("-", "_")
            setattr(self, k, v)

    # NOTE: Above loop sets properties of this class based on the key names
    #       of the passed 'kwargs' dictionary. Methods functions defined down
    #       below are also properties of this class.
    #       To escape naming collision it is essential to make sure that
    #       method names and 'kwargs' key names differ.

    @property
    def identifier(self):
        if hasattr(self, 'node_id'):
            return self.node_id
        else:
            # dbg_trace_print("!!!Warning: missing expected attribute")
            return None

    @property
    def connected(self):
        if hasattr(self, 'connection_status'):
            return (self.connection_status == 'connected')
        else:
            # dbg_trace_print("!!!Warning: missing expected attribute")
            return None

    @property
    def ip_addr(self):
        if hasattr(self, 'host'):
            return self.host
        else:
            # dbg_trace_print("!!!Warning: missing expected attribute")
            return None

    @property
    def port_num(self):
        if hasattr(self, 'port'):
            return self.port
        else:
            # dbg_trace_print("!!!Warning: missing expected attribute")
            return None

    @property
    def capabilities_available(self):
        if hasattr(self, 'available_capabilities'):
            return self.available_capabilities.get('available-capability')
        else:
            # dbg_trace_print("!!!Warning: missing expected attribute")
            return None

    @property
    def capabilities_unavailable(self):
        if hasattr(self, 'unavailable_capabilities'):
            data = []
            clist = self.unavailable_capabilities.get('unavailable-capability')
            if(clist):
                for item in clist:
                    s = ("%s, failure-reason: %s" %
                         (item.get('capability'), item.get('failure-reason')))
                    data.append(s)
            return data
        else:
            # dbg_trace_print("!!!Warning: missing expected attribute")
            return None
