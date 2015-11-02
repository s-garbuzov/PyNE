
# built-in modules
import time


from cmd_multiprocessing.channels.ssh_channel import SSHChannel
from cmd_multiprocessing.channels.telnet_channel import TELNETChannel


class BrocadeVRouter(object):
    """Brocade vRouter device."""

    MAX_RCV_BUFFER = 1000
    OPER_PROMPT = '$'
    ADMIN_PROMPT = '#'

    def __init__(self, **kwargs):
        """Allocate and return a new instance object."""
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

    def connect(self):
        if(self._channel is not None):
            return self._channel

        if(self.channel == 'ssh'):
            channel = SSHChannel(self.ip_addr, self.port,
                                 self.admin_name, self.admin_pswd,
                                 self.timeout, self.verbose)
        elif(self.channel == 'telnet'):
            channel = TELNETChannel(self.ip_addr, self.port,
                                    self.admin_name, self.admin_pswd,
                                    self.timeout, self.verbose)
        else:
            assert False, 'unexpected attribute value: %s' % self.channel

        channel.open()
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
#        print output
        return output


if __name__ == "__main__":
    device1 = {'ip_addr': "172.22.17.110",
               'port': 830,
               'device_type': 'brocade_vrouter',
               'channel': 'ssh',
               'admin_name': 'vyatta',
               'admin_pswd': 'vyatta',
               'timeout': 7,
               'verbose': True
               }
    device2 = {'ip_addr': "172.22.17.110",
               'port': 23,
               'device_type': 'brocade_vrouter',
               'channel': 'telnet',
               'admin_name': 'vyatta',
               'admin_pswd': 'vyatta',
               'timeout': 7,
               'verbose': True
               }

    obj = BrocadeVRouter(**device1)
    obj.open_session()

    obj.execute_command("show interfaces\n")

    obj.close_session()
