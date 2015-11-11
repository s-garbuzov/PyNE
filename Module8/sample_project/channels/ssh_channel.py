"""
Class that handles SSH connection to a network device.
Defines methods that are generally applicable to different platforms.
"""


# Python standard library modules
import socket
import time

# third-party modules
import paramiko


class SSHChannel(object):
    """SSH connection to a remote device."""

    def __init__(self, ip_addr, port,
                 admin_name, admin_pswd,
                 max_bytes=1000,
                 timeout=None, verbose=False):
        self._channel = None
        self._remote_shell = None
        self._max_bytes = max_bytes
        self.ip_addr = ip_addr
        self.port = port
        self.admin_name = admin_name
        self.admin_pswd = admin_pswd
        self.timeout = timeout
        self.verbose = verbose

    def open(self):
        if(self._channel is not None):
            return self._channel

        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if(self.verbose):
                print("Connecting to %s:%s" % (self.ip_addr, self.port))
            ssh_client.connect(hostname=self.ip_addr, port=self.port,
                               username=self.admin_name,
                               password=self.admin_pswd,
                               look_for_keys=False, allow_agent=False,
                               timeout=self.timeout)
            rsh = ssh_client.invoke_shell()
            rsh.recv(self._max_bytes)
            self._remote_shell = rsh
            self._channel = ssh_client
            if(self.verbose):
                print("Connection to %s:%s has been established" %
                      (self.ip_addr, self.port))
            return self._channel
        except (paramiko.BadHostKeyException,
                paramiko.AuthenticationException,
                paramiko.SSHException,
                socket.error) as e:
            print("!!!Error: [%s:%s] %s " % (self.ip_addr, self.port, e))

    def close(self):
        assert(self._channel is not None)
        if self._channel is not None:
            try:
                self._channel.close()
                if(self.verbose):
                    print("Connection to %s:%s has been closed" %
                          (self.ip_addr, self.port))
            except (Exception) as e:
                print("!!!Error: [%s:%s]  %s " % (self.ip_addr, self.port, e))

    def send(self, data):
        assert(self._remote_shell is not None)
        self._remote_shell.send(data)

    def recv(self, read_delay):
        assert(self._remote_shell is not None)
        time.sleep(read_delay)
        return self._remote_shell.recv(self._max_bytes)
