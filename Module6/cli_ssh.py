#!/usr/bin/env python

# Example of a script that executes CLI commands on a remote
# device via SSH connection

# built-in modules
import time
import socket

# third-party modules
import paramiko


# SSH session specific data
IP_ADDR = '172.22.17.110'
PORT_NUM = 830
USERNAME = 'vyatta'
PASSWORD = 'vyatta'

# CLI session specific data
TIMEOUT = 5
RCV_BUFF_SIZE = 1000


def cli_disable_paging(rsh):
    """Disable CLI paging on a remote device"""

    # Execute the command
    cmd = 'set terminal length 0\n'
    rsh.send(cmd)
    # wait for command to complete
    time.sleep(1)

    # Flush out the read buffer
    rsh.recv(RCV_BUFF_SIZE)


def cli_enter_cfg_mode(rsh):
    """Execute CLI command for entering the configuration mode
    on a remote device
    """

    # Execute the command
    cmd = "configure\n"
    rsh.send(cmd)
    # wait for command to complete
    time.sleep(1)

    # Flush out the read buffer
    rsh.recv(RCV_BUFF_SIZE)


def cli_get_interfaces(rsh):
    """Obtain interface information from a remote device"""

    # Execute the command
    rsh.send('show interfaces\n')
    # wait for command to complete
    time.sleep(1)

    # Read the result of executed CLI command from the
    # channel buffer
    output = rsh.recv(RCV_BUFF_SIZE)
    return output


def connect_ssh(ip, port, uname, pswd):
    """Establish SSH connection to a remote device"""

    # Create an instance object of the 'SSHClient' class
    rconn = paramiko.SSHClient()

    # Allow auto adding of unknown hosts to the known hosts in local
    # SSH configuration (make sure it is okay with your security
    # policy requirements)
    rconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Establish SSH connection
    try:
        # o 'look_for_keys' is set to False to disable searching
        #   for discoverable private key files in '~/.ssh/'
        # o 'allow_agent' is set to False to disable connecting
        #   to the SSH agent on the local machine for obtaining
        #   the private key
        rconn.connect(ip, username=uname, password=pswd, port=830,
                      look_for_keys=False, allow_agent=False)
        return rconn
    except (paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException,
            socket.error) as e:
        print "!!!Error: %s " % e
        return None


def disconnect_ssh(rconn):
    """Close SSH connection to a remote device"""
    try:
        rconn.close()
    except (Exception) as e:
        print "!!!Error, %s " % e


# Connect to a remote SSH server and execute few CLI commands
ssh_conn = connect_ssh(ip=IP_ADDR, port=PORT_NUM,
                       uname=USERNAME, pswd=PASSWORD)
if ssh_conn:
    print "Established SSH connection to %s\n" % IP_ADDR
    try:
        # Start an interactive shell session on the remote SSH server
        rsh = ssh_conn.invoke_shell()
#        print "Initiated interactive shell session\n"

        # Read the initial prompt data from the channel
        # (flush out the read buffer)
        output = rsh.recv(RCV_BUFF_SIZE)

        # Turn off CLI paging
        cli_disable_paging(rsh)

        # Enter configuration mode
        cli_enter_cfg_mode(rsh)

        # Read and show list of interfaces
        output = cli_get_interfaces(rsh)
        print "%s\n" % output
    except (paramiko.SSHException) as e:
        print "!!!Error: %s\n" % e
    finally:
        disconnect_ssh(ssh_conn)
        print "Closed SSH connection to %s\n" % IP_ADDR
else:
    print "SSH connection to %s has failed\n" % IP_ADDR
