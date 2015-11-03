
# built-in modules
import telnetlib


class TELNETChannel(object):
    """TBD"""
    def __init__(self, ip_addr, port,
                 admin_name, admin_pswd,
                 login_prompt, password_prompt,
                 oper_prompt, admin_prompt,
                 timeout=None, verbose=False):
        self.channel = None
        self.ip_addr = ip_addr
        self.port = port
        self.admin_name = admin_name
        self.admin_pswd = admin_pswd
        self.login_prompt = login_prompt
        self.pswd_prompt = password_prompt
        self.oper_prompt = oper_prompt
        self.admin_prompt = admin_prompt
        self.timeout = timeout
        self.verbose = verbose

    def open(self):
        if(self.channel is not None):
            return self.channel

        try:
            rconn = telnetlib.Telnet()
            rconn.open(self.ip_addr, self.port, self.timeout)
            # rconn.set_debuglevel(1)
            if(self.admin_name):
                login_prompt = self.login_prompt
                response = rconn.read_until(login_prompt, self.timeout)
                if login_prompt not in response:
                    self.close()
                    return None
                rconn.write('%s\n' % self.admin_name)
            if(self.admin_pswd):
                pswd_prompt = self.pswd_prompt
                response = rconn.read_until(pswd_prompt, self.timeout)
                if pswd_prompt not in response:
                    self.close()
                    return None
                rconn.write('%s\n' % self.admin_pswd)
            oper_prompt = '\%s' % self.oper_prompt
            admin_prompt = self.admin_prompt
            r = rconn.expect([oper_prompt, admin_prompt], self.timeout)
            if(r[0] == -1):
                self.close()
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
        oper_prompt = '\%s' % self.oper_prompt
        admin_prompt = self.admin_prompt
        dummy, dummy, text = self.channel.expect([oper_prompt, admin_prompt],
                                                 self.timeout)
        return text
