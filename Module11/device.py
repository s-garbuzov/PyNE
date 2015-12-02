

class Device(object):
    """Class representing a network device."""

    def __init__(self, name, os_type, ip_addr=None, iflist=[]):
        """The constructor of an instance of this class."""
        self._name = name
        self._os_type = os_type
        self._ip_addr = ip_addr
        self._iflist = iflist

    @property
    def name(self):
        return self._name

    @property
    def os_type(self):
        return self._os_type

    @property
    def ip_addr(self):
        return self._ip_addr

    @ip_addr.setter
    def ip_addr(self, value):
        self._ip_addr = value

    @property
    def interfaces(self):
        return self._iflist

    @interfaces.setter
    def interfaces(self, value):
        self._iflist = value

    @property
    def if_count(self):
        return len(self._iflist)
