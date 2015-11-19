

class NETCONFDevice(object):
    """Represents NETCONF capable device"""

    def __init__(self, node_id, ip_addr, port=830,
                 admin_name=None, admin_password=None):
        self._id = node_id
        self._addr = ip_addr
        self._port = port
        self._uname = admin_name
        self._upswd = admin_password

    @property
    def node_id(self):
        return self._id

    @node_id.setter
    def node_id(self, value):
        self._id = value

    @property
    def ip_addr(self):
        return self._addr

    @ip_addr.setter
    def ip_addr(self, value):
        self._addr = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def admin_name(self):
        return self._uname

    @admin_name.setter
    def admin_name(self, value):
        self._uname = value

    @property
    def admin_password(self):
        return self._upswd

    @admin_password.setter
    def admin_password(self, value):
        self._upswd = value
