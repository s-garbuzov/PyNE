import time
import socket

# third-party modules
import paramiko


class CiscoXR(object):
    MAX_RCV_BUFFER = 1000

    def __init__(self, **kwargs):
        self.ssh_conn = None
        self.telnet_conn = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_version(self, **kwargs):
        time.sleep(0)
        status = False
        output = None
        return status, output

    def get_vendor(self):
        return "Cisco"

    def get_os_type(self):
        return "IOS-XR"

    def get_ipaddr(self):
        ip_addr = None
        if(hasattr(self, 'ip_addr')):
            ip_addr = self.ip_addr
        return ip_addr

    def __disable_cli_paging(self, rsh):
        cmd = 'set terminal length 0\n'
        rsh.send(cmd)  # execute command remotely
        time.sleep(1)  # wait command to complete
        rsh.recv(self.MAX_RCV_BUFFER)  # flush receive buffer

    def __enter_cli_cfg_mode(self, rsh):
        cmd = "configure\n"
        rsh.send(cmd)  # execute command remotely
        time.sleep(1)  # wait command to complete
        rsh.recv(self.MAX_RCV_BUFFER)  # flush receive buffer

    def exec_cmd_ssh(self, cli_command, read_delay):
        output = None
        ssh_conn = self.connect_ssh()
        if ssh_conn:
            if(self.verbose):
                print("Established SSH connection to %s:%s\n" %
                      (self.ip_addr, self.port))
            try:
                rsh = ssh_conn.invoke_shell()
                rsh.recv(self.MAX_RCV_BUFFER)
                # Turn off CLI paging and enter configuration mode
                self.__disable_cli_paging(rsh)
                self.__enter_cli_cfg_mode(rsh)
                # Execute command, wait for completion, read result
                rsh.send(cli_command)
                time.sleep(read_delay)
                output = rsh.recv(self.MAX_RCV_BUFFER)
            except (paramiko.SSHException) as e:
                output = "Failed to execute command"
                if(self.verbose):
                    print("!!!Error: %s\n" % e)
            finally:
                self.disconnect_ssh()
                if(self.verbose):
                    print("Closed SSH connection to %s:%s\n" %
                          (self.ip_addr, self.port))
        else:
            output = "Failed to execute command"
            if(self.verbose):
                print("SSH connection to %s:%s has failed\n" %
                      (self.ip_addr, self.port))

        return output

    def connect_ssh(self):
        if self.ssh_conn is not None:
            return self.ssh_conn

        try:
            rconn = paramiko.SSHClient()
            rconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rconn.connect(hostname=self.ip_addr, port=self.port,
                          username=self.admin_name, password=self.admin_pswd,
                          look_for_keys=False, allow_agent=False,
                          timeout=self.timeout)
            self.ssh_conn = rconn
            return self.ssh_conn
        except (paramiko.BadHostKeyException,
                paramiko.AuthenticationException,
                paramiko.SSHException,
                socket.error) as e:
            if(self.verbose):
                print "!!!Error: %s " % e
            return None

    def disconnect_ssh(self):
        if self.ssh_conn is not None:
            try:
                self.ssh_conn.close()
            except (Exception) as e:
                if(self.verbose):
                    print "!!!Error, %s " % e
