import time


class CiscoEOS(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_version(self):
        time.sleep(0)
        status = True
        output = "2.2.2"
        return status, output

    def get_vendor(self):
        return "Cisco"

    def get_os_type(self):
        return "EOS"

    def get_ipaddr(self):
        ip_addr = None
        if(hasattr(self, 'ip_addr')):
            ip_addr = self.ip_addr
        return ip_addr
