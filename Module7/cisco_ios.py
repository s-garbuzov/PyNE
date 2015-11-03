"""
CiscoIOS class (subclass of the NetworkDevice base class)
"""

import time

from network_device import NetworkDevice
from telnet_channel import TELNETChannel
from ssh_channel import SSHChannel


# Subclass of the 'NetworkDevice' base class
class CiscoIOS(NetworkDevice):
    """
    Class representing an instance of a Cisco network device running IOS.
    Defines device specific methods.
    """

    def __init__(self, **kwargs):
        # Invoke the superclass initialization method to initialize
        # inherited attributes
        NetworkDevice.__init__(self, 'Cisco', 'ios')
        self._channel = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        """ Method that overloads  Python's build-in __repr__ method"""
        return "Cisco IOS device(%s:%s)" % (self.ip_addr, self.port)

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
                                 self.admin_name, self.admin_pswd,
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
        cmd = 'terminal length 0\n'
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
#        print output
        return output