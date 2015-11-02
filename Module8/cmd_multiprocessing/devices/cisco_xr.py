import time
# import socket

# third-party modules
# import paramiko


class CiscoXR(object):
    """TBD"""

    MAX_RCV_BUFFER = 1000

    def __init__(self, **kwargs):
        self.ssh_conn = None
        self.telnet_conn = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_version(self, **kwargs):
        time.sleep(0)
        status = False
        output = None
        return status, output

    def get_vendor(self):
        return "Cisco"

    def get_os_type(self):
        return "IOS-XR"

    def get_ipaddr(self):
        ip_addr = None
        if(hasattr(self, 'ip_addr')):
            ip_addr = self.ip_addr
        return ip_addr

    def connect(self):
        pass

    def disconnect(self):
        pass

    def disable_paging(self):
        pass

    def enter_cfg_mode(self):
        pass

    def execute_command(self, command, read_delay=1):
        return "Unimplemented"
        pass
