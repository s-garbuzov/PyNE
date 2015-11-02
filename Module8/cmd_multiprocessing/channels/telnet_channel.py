

# built-in modules
import telnetlib


class TELNETChannel(object):
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

    def open(self):
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
            print "!!!Error: %s " % e
            return None

    def close(self):
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
