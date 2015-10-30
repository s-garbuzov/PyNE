import time
# import socket

# third-party modules
# import paramiko


class CiscoIOS(object):
    """TBD"""

    MAX_RCV_BUFFER = 1000

    def __init__(self, **kwargs):
        self.ssh_conn = None
        self.telnet_conn = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_version(self):
        time.sleep(0)
        status = True
        output = "1.1.1"
        return status, output

    def get_vendor(self):
        return "Cisco"

    def get_os_type(self):
        return "IOS"

    def get_ipaddr(self):
        ip_addr = None
        if(hasattr(self, 'ip_addr')):
            ip_addr = self.ip_addr
        return ip_addr

    def open_session(self):
        pass

    def close_session(self):
        pass

    def disable_paging(self):
        pass

    def enter_cfg_mode(self):
        pass

    def execute_command(self, command, read_delay=1):
        return "Unimplemented"
        pass


class SSHSession(object):
    MAX_RCV_BUFFER = 1000

    def __init__(self, ip_addr, port,
                 admin_name, admin_pswd,
                 timeout=None, verbose=False):
        self.ip_addr = ip_addr
        self.port = port
        self.admin_name = admin_name
        self.admin_pswd = admin_pswd
        self.timeout = timeout
        self.verbose = verbose
        self.channel = None
        self.remote_shell = None

    def connect(self):
        pass

    def disconnect(self):
        pass

    def send(self, data):
        pass

    def recv(self):
        pass


class TELNETSession(object):
    OPER_PROMPT = '$'
    ADMIN_PROMPT = '#'

    def __init__(self, ip_addr, port,
                 admin_name, admin_pswd,
                 timeout=None, verbose=False):
        self.channel = None
        self.ip_addr = ip_addr
        self.port = port
        self.admin_name = admin_name
        self.admin_pswd = admin_pswd
        self.timeout = timeout
        self.verbose = verbose
        self.channel = None

    def connect(self):
        pass

    def disconnect(self):
        pass

    def send(self, data):
        pass

    def recv(self, timeout=1):
        pass
