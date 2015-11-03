
# built-in modules
import socket

# third-party modules
import paramiko


class SSHChannel(object):
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

    def open(self):
        if(self.channel is not None):
            return self.channel

        try:
            rconn = paramiko.SSHClient()
            rconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rconn.connect(hostname=self.ip_addr, port=self.port,
                          username=self.admin_name, password=self.admin_pswd,
                          look_for_keys=False, allow_agent=False,
                          timeout=self.timeout)
            rsh = rconn.invoke_shell()
            rsh.recv(self.MAX_RCV_BUFFER)
            self.remote_shell = rsh
            self.channel = rconn
        except (paramiko.BadHostKeyException,
                paramiko.AuthenticationException,
                paramiko.SSHException,
                socket.error) as e:
            print "!!!Error: %s " % e

    def close(self):
        assert(self.channel is not None)
        if self.channel is not None:
            try:
                self.channel.close()
            except (Exception) as e:
                print "!!!Error, %s " % e

    def send(self, data):
        assert(self.remote_shell is not None)
        self.remote_shell.send(data)

    def recv(self):
        assert(self.remote_shell is not None)
        return self.remote_shell.recv(self.MAX_RCV_BUFFER)
