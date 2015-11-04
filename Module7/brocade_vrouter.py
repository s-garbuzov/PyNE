"""
BrocadeVRouter class (subclass of the NetworkDevice base class)
"""

# built-in modules
import time

# this project local modules
from network_device import NetworkDevice
from ssh_channel import SSHChannel
from telnet_channel import TELNETChannel


class BrocadeVRouter(NetworkDevice):
    """Brocade vRouter device."""

    def __init__(self, **kwargs):
        """Allocate and return a new instance object."""
        NetworkDevice.__init__(self, 'Brocade', 'Linux')
        self._channel = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_version(self):
        time.sleep(0)
        status = True
        output = "3.2.1R6"
        return status, output

    def get_vendor(self):
        return "Brocade"

    def get_os_type(self):
        return "Linux"

    def get_ipaddr(self):
        ip_addr = None
        if(hasattr(self, 'ip_addr')):
            ip_addr = self.ip_addr
        return ip_addr

    def connected(self):
        return True if(self._channel is not None) else False

    def connect(self):
        if(self._channel is not None):
            return self._channel

        channel = None
        if(self.channel == 'ssh'):
            channel = SSHChannel(self.ip_addr, self.port,
                                 self.username, self.password,
                                 self.max_bytes,
                                 self.timeout, self.verbose)
        elif(self.channel == 'telnet'):
            channel = TELNETChannel(self.ip_addr, self.port,
                                    self.username, self.password,
                                    self.login_prompt, self.password_prompt,
                                    self.oper_prompt, self.admin_prompt,
                                    self.timeout, self.verbose)
        else:
            assert False, 'unexpected attribute value: %s' % self.channel

        if(channel.open() is not None):
            self._channel = channel
        return self._channel

    def disconnect(self):
        if(self._channel is not None):
            self._channel.close()

    def disable_paging(self):
        assert(self._channel is not None)
        cmd = 'set terminal length 0\n'
        self.execute_command(cmd, 0)

    def enter_cfg_mode(self):
        assert(self._channel is not None)
        cmd = "configure\n"
        self.execute_command(cmd, 0)

    def execute_command(self, command, read_delay=1):
        assert(self._channel is not None)
        self._channel.send(command)
        time.sleep(read_delay)  # wait command to complete
        output = self._channel.recv()
        return output
