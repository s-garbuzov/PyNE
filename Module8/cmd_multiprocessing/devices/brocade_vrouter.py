
# built-in modules
import time
import socket
import telnetlib

# third-party modules
import paramiko


class BrocadeVRouter(object):
    """Brocade vRouter device."""

    MAX_RCV_BUFFER = 1000
    OPER_PROMPT = '$'
    ADMIN_PROMPT = '#'

    def __init__(self, **kwargs):
        """Return a new instance object."""
        self.ssh_conn = None
        self.telnet_conn = None
        self.session = None
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

    def open_session(self):
        if(self.session is not None):
            return

        if(self.channel == 'ssh'):
            ses = SSHSession(self.ip_addr, self.port,
                             self.admin_name, self.admin_pswd,
                             self.timeout, self.verbose)
            ses.connect()
            self.session = ses
        elif(self.channel == 'telnet'):
            print "create TELNET session"
            ses = TELNETSession(self.ip_addr, self.port,
                                self.admin_name, self.admin_pswd,
                                self.timeout, self.verbose)
            ses.connect()
            self.session = ses
        else:
            assert False, 'unexpected attribute value: %s' % self.channel

    def close_session(self):
        if(self.session is not None):
            self.session.disconnect()

    def disable_paging(self):
        cmd = 'set terminal length 0\n'
        self.session.send(cmd)
        time.sleep(0)  # wait command to complete
        self.session.recv()

    def enter_cfg_mode(self):
        cmd = "configure\n"
        self.session.send(cmd)
        time.sleep(0)  # wait command to complete
        self.session.recv()

    def execute_command(self, command, read_delay=1):
        assert(self.session is not None)
        self.disable_paging()
        self.enter_cfg_mode()
        self.session.send(command)
        time.sleep(read_delay)  # wait command to complete
        output = self.session.recv()
#        print output
        return output


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
            if(self.verbose):
                print("Established SSH connection to %s:%s\n" %
                      (self.ip_addr, self.port))
        except (paramiko.BadHostKeyException,
                paramiko.AuthenticationException,
                paramiko.SSHException,
                socket.error) as e:
            if(self.verbose):
                print "!!!Error: %s " % e

    def disconnect(self):
        assert(self.channel is not None)
        if self.channel is not None:
            try:
                self.channel.close()
                if(self.verbose):
                    print("Closed SSH connection to %s:%s\n" %
                          (self.ip_addr, self.port))
            except (Exception) as e:
                if(self.verbose):
                    print "!!!Error, %s " % e

    def send(self, data):
        assert(self.remote_shell is not None)
        self.remote_shell.send(data)

    def recv(self):
        assert(self.remote_shell is not None)
        return self.remote_shell.recv(self.MAX_RCV_BUFFER)


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
        if(self.channel is not None):
            return self.channel

        try:
            rconn = telnetlib.Telnet()
            rconn.open(self.ip_addr, self.port, self.timeout)
            # rconn.set_debuglevel(1)
            if(self.admin_name):
                login_prompt = 'login:'
                response = rconn.read_until(login_prompt, self.timeout)
                if login_prompt not in response:
                    self.disconnect()
                    return None
                rconn.write('%s\n' % self.admin_name)
            if(self.admin_pswd):
                pswd_prompt = 'assword:'
                response = rconn.read_until(pswd_prompt, self.timeout)
                if pswd_prompt not in response:
                    self.disconnect()
                    return None
                rconn.write('%s\n' % self.admin_pswd)
            oper_prompt = '\%s' % self.OPER_PROMPT
            r = rconn.expect([oper_prompt], self.timeout)
            if(r[0] == -1):
                self.disconnect()
                return None

            self.channel = rconn
            return rconn
        except (Exception) as e:
            if(self.verbose):
                print "!!!Error: %s " % e
            return None

    def disconnect(self):
        if self.channel is not None:
            try:
                self.channel.close()
            except (Exception) as e:
                print "!!!Error, %s " % e

    def send(self, data):
        assert(self.channel is not None)
        self.channel.write(data)

    def recv(self, timeout=1):
        assert(self.channel is not None)
        return self.channel.read_until(self.ADMIN_PROMPT, 1)

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
