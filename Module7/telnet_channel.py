"""
Class that handles TELNET connection to a network device.
Defines methods that are generally applicable to different platforms.
"""

# built-in modules
import telnetlib


class TELNETChannel(object):
    """TELNET connection to a remote device."""
    def __init__(self, ip_addr, port,
                 admin_name, admin_pswd,
                 login_prompt, password_prompt,
                 oper_prompt, config_prompt,
                 timeout=None, verbose=False):
        self._channel = None
        self.ip_addr = ip_addr
        self.port = port
        self.admin_name = admin_name
        self.admin_pswd = admin_pswd
        self.login_prompt = login_prompt
        self.pswd_prompt = password_prompt
        self.oper_prompt = oper_prompt
        self.config_prompt = config_prompt
        self.timeout = timeout
        self.verbose = verbose

    def open(self):
        if(self._channel is not None):
            return self._channel

        try:
            # Create an instance object of the 'Telnet' class
            telnet_client = telnetlib.Telnet()

            # uncomment following line to enable 'telnetlib' debug tracing
            # telnet_client.set_debuglevel(1)

            # Connect to device
            if(self.verbose):
                print("Connecting to %s:%s" % (self.ip_addr, self.port))
            telnet_client.open(self.ip_addr, self.port, self.timeout)
            if(self.verbose):
                print("Connection to %s:%s has been established" %
                      (self.ip_addr, self.port))

            # Login to device
            if(self.admin_name):
                login_prompt = self.login_prompt
                response = telnet_client.read_until(login_prompt, self.timeout)
                if login_prompt not in response:
                    self.close()
                    err_msg = ("Failed to get expected '%s' login prompt" %
                               login_prompt)
                    raise ValueError(err_msg)
                telnet_client.write('%s\n' % self.admin_name)
            if(self.admin_pswd):
                pswd_prompt = self.pswd_prompt
                response = telnet_client.read_until(pswd_prompt, self.timeout)
                if pswd_prompt not in response:
                    self.close()
                    err_msg = ("Failed to get expected '%s' password prompt" %
                               pswd_prompt)
                    raise ValueError(err_msg)
                telnet_client.write('%s\n' % self.admin_pswd)

            # Check if we got to the console prompt
            oper_prompt = '\%s' % self.oper_prompt
            config_prompt = self.config_prompt
            dummy, match, dummy = \
                telnet_client.expect([oper_prompt, config_prompt],
                                     self.timeout)
            if(match is None):
                self.close()
                err_msg = ("Login failed (uname=%s, pswd=%s)" %
                           (self.admin_name, self.admin_pswd))
                raise ValueError(err_msg)

            self._channel = telnet_client
            return self._channel
        except (Exception) as e:
            print "!!!Error: %s " % e
            return None

    def close(self):
        if self._channel is not None:
            try:
                self._channel.close()
                if(self.verbose):
                    print("Connection to %s:%s has been closed" %
                          (self.ip_addr, self.port))
            except (Exception) as e:
                print "!!!Error, %s " % e

    def send(self, data):
        assert(self._channel is not None)
        self._channel.write(data)

    def recv(self, read_delay):
        assert(self._channel is not None)
        oper_prompt = "%r" % self.oper_prompt
#        oper_prompt = "\%s" % self.oper_prompt
        config_prompt = self.config_prompt
        dummy, dummy, text = self._channel.expect([oper_prompt, config_prompt],
                                                  read_delay)
        return text
