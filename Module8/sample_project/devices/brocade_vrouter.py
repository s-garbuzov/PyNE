"""
BrocadeVRouter class
"""

# this package local modules
from Module8.sample_project.channels.ssh_channel import SSHChannel
from Module8.sample_project.channels.telnet_channel import TELNETChannel


class BrocadeVRouter(object):
    """Brocade vRouter device with device specific methods."""

    def __init__(self, **kwargs):
        """Allocate and return a new instance object."""

        # Initialize this class attributes
        self._channel = None
        self.vendor = "Brocade"
        self.os_type = "Linux"
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_str(self):
        return "%s %s %s:%s" % (self.vendor, self.os_type,
                                self.ip_addr, self.port)

    def get_version(self):
        status = True
        output = "3.2.1R6"
        return status, output

    def get_vendor(self):
        return self.vendor

    def get_os_type(self):
        return self.os_type

    def get_ipaddr(self):
        return self.ip_addr

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
                                    self.oper_prompt, self.config_prompt,
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
        self.execute_command(cmd, 1)

    def enable_privileged_commands(self):
        self.enter_cfg_mode()

    def check_cfg_mode(self):
        assert(self._channel is not None)
        cmd = '\n'
        output = self.execute_command(cmd, 1)
        if(self.config_prompt in output):
            return True
        else:
            return False

    def enter_cfg_mode(self):
        assert(self._channel is not None)
        if not self.check_cfg_mode():
            cmd = "configure\n"
            self.execute_command(cmd, 1)

    def execute_command(self, command, read_delay=1):
        assert(self._channel is not None)
        self._channel.send(command)
        output = self._channel.recv(read_delay)
        return output
