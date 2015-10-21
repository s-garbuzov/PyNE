class Device(object):
    """
    TBD: class docs
    """

    def __init__(self, dev_type, ip_addr=None, port=None):
        """
        In Python, this method is known as the constructor, it is called
        each time an instance object is generated from this class.
        """
        self.device_type = dev_type
        self.ip_addr = ip_addr
        self.port = port
        self.connected = False
        self.rconn = None

    def connect_ssh(self):
        pass

    def connect_telnet(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

