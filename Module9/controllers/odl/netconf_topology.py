
class NETCONFNodeTopoInfo(object):
    """Helper class that used to parse NETCONF node information
    obtained from the Controller's topologies data tree"""
    def __init__(self, **kwargs):
        prefix = "netconf-node-topology:"
        print type(kwargs)
        for k, v in kwargs.items():
            if(isinstance(k, basestring)):
                k = k.replace(prefix, "").replace("-", "_")
#            print "++%s" % k
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
            assert(False), "[NETCONFNodeTopoInfo] missing expected attribute"
            return None

    @property
    def connected(self):
        if hasattr(self, 'connection_status'):
            return (self.connection_status == 'connected')
        else:
            assert(False), "[NETCONFNodeTopoInfo] missing expected attribute"
            return None

    @property
    def ip_addr(self):
        if hasattr(self, 'host'):
            return self.host
        else:
            assert(False), "[NETCONFNodeTopoInfo] missing expected attribute"
            return None

    @property
    def port_num(self):
        if hasattr(self, 'port'):
            return self.port
        else:
            assert(False), "[NETCONFNodeTopoInfo] missing expected attribute"
            return None

    @property
    def capabilities_available(self):
        if hasattr(self, 'available_capabilities'):
            return self.available_capabilities.get('available-capability')
        else:
            assert(False), "[NETCONFNodeTopoInfo] missing expected attribute"
            return None

    @property
    def capabilities_unavailable(self):
        if hasattr(self, 'unavailable_capabilities'):
            data = []
            clist = self.unavailable_capabilities.get('unavailable-capability')
            for item in clist:
                s = ("%s, failure-reason: %s" %
                     (item.get('capability'), item.get('failure-reason')))
                data.append(s)
            return data
        else:
            assert(False), "[NETCONFNodeTopoInfo] missing expected attribute"
            return None
