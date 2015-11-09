"""
CiscoIOS class (subclass of the NetworkDevice base class)
"""

# this project local modules
from Module7.network_device import NetworkDevice
from Module7.telnet_channel import TELNETChannel
from Module7.ssh_channel import SSHChannel


# Subclass of the 'NetworkDevice' base class
class CiscoIOS(NetworkDevice):
    """Cisco IOS device with device specific methods."""

    def __init__(self, **kwargs):
        """Allocate and return a new instance object."""

        # Invoke the superclass initialization method to initialize
        # inherited attributes
        NetworkDevice.__init__(self, 'Cisco', 'IOS')
        # Initialize this class attributes
        self._channel = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_str(self):
        return "%s %s %s:%s" % (self.get_vendor(), self.get_os_type(),
                                self.ip_addr, self.port)

    def get_addr(self):
        return self.ip_addr

    def get_port(self):
        return self.port

    def get_firmware_version(self):
        """
        Class specific method that retrieves and returns
        the firmware version from the device.
        """
        pass

    def connected(self):
        return True if(self._channel is not None) else False

    def connect(self):
        if(self._channel is not None):
            return self._channel

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

    def enable_privileged_commands(self):
        assert(self._channel is not None)
        cmd = "enable\n"
        self._channel.send(cmd)
        output = self._channel.recv(read_delay=1)
        if(self.password_prompt in output):
            password = "%s\n" % self.password
            self._channel.send(password)
            output = self._channel.recv(read_delay=1)

    def disable_paging(self):
        assert(self._channel is not None)
        cmd = 'terminal length 0\n'
        self.execute_command(cmd, 1)

    def check_cfg_mode(self):
        assert(self._channel is not None)
        cmd = '\n'
        output = self.execute_command(cmd, 1)
        config_prompt = "(%s)%s" % ('config', self.admin_prompt)
        if(config_prompt in output):
            return True
        else:
            return False

    def enter_cfg_mode(self):
        assert(self._channel is not None)
        if not self.check_cfg_mode():
            cmd = "configure terminal\n"
            self.execute_command(cmd, 1)

    def execute_command(self, command, read_delay=1):
        assert(self._channel is not None)
        self._channel.send(command)
        output = self._channel.recv(read_delay)
        return output
