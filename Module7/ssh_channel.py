
# built-in modules
import socket

# third-party modules
import paramiko


class SSHChannel(object):
    """Represents SSH connection to a remote device."""
    def __init__(self, ip_addr, port,
                 admin_name, admin_pswd,
                 max_rcv_buffer=1000,
                 timeout=None, verbose=False):
        self._channel = None
        self._remote_shell = None
        self._max_bytes = max_rcv_buffer
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
            rconn = paramiko.SSHClient()
            rconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rconn.connect(hostname=self.ip_addr, port=self.port,
                          username=self.admin_name, password=self.admin_pswd,
                          look_for_keys=False, allow_agent=False,
                          timeout=self.timeout)
            rsh = rconn.invoke_shell()
            rsh.recv(self._max_bytes)
            self._remote_shell = rsh
            self._channel = rconn
            return self._channel
        except (paramiko.BadHostKeyException,
                paramiko.AuthenticationException,
                paramiko.SSHException,
                socket.error) as e:
            print "!!!Error: %s " % e
            return None

    def close(self):
        assert(self._channel is not None)
        if self._channel is not None:
            try:
                self._channel.close()
            except (Exception) as e:
                print "!!!Error, %s " % e

    def send(self, data):
        assert(self._remote_shell is not None)
        self._remote_shell.send(data)

    def recv(self):
        assert(self._remote_shell is not None)
        return self._remote_shell.recv(self._max_bytes)
