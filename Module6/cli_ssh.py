#!/usr/bin/env python

# Example of a script that executes CLI commands on a remote
# device via SSH connection

# built-in modules
import time
import socket

# third-party modules
import paramiko


# Remote device SSH session specific data that need change
IP_ADDR = '172.22.17.110'
PORT_NUM = 830
USERNAME = 'vyatta'
PASSWORD = 'vyatta'
# The maximum amount of data to be received from the remote
# device during CLI session
RCV_BUFF_SIZE = 1000


def cli_disable_paging(rsh):
    '''Disable CLI paging on a remote device'''

    # Execute CLI command that disables CLI paging
    rsh.send("set terminal length 0\n")
    time.sleep(1)

    # Read the channel buffer (clear output data that might
    # left in the buffer in result of the command execution)
    rsh.recv(RCV_BUFF_SIZE)


def cli_get_interfaces(rsh):
    '''Obtain interface information from a remote device'''

    # Execute CLI command that shows list of network
    # interfaces and wait for the command to complete
    rsh.send('show interfaces\n')
    time.sleep(1)

    # Read the result of executed CLI command from the
    # channel buffer and return it
    output = rsh.recv(RCV_BUFF_SIZE)
    return output


def connect_ssh(ip, port, uname, pswd):
    '''Establish SSH connection to a remote device'''

    # Create an instance of SSHClient object
    rconn = paramiko.SSHClient()

    # Allow auto adding of unknown hosts to the known hosts in local
    # SSH configuration (make sure it is okay with your security
    # policy requirements)
    rconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # establish SSH connection
    # o 'look_for_keys' is set to False to disable searching
    #   for discoverable private key files in '~/.ssh/'
    # o 'allow_agent' is set to False to disable connecting
    #   to the SSH agent on the local machine for obtaining
    #   the private key
    try:
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
    '''Terminate SSH connection with a remote device'''
    try:
        rconn.close()
    except (Exception) as e:
        print "!!!Error, %s " % e


if __name__ == '__main__':

    # Connect to a remote SSH server
    ssh_conn = connect_ssh(ip=IP_ADDR, port=PORT_NUM,
                           uname=USERNAME, pswd=PASSWORD)
    if ssh_conn:
        print "Established SSH connection to %s\n" % IP_ADDR
        try:
            # Start an interactive shell session on the remote SSH server
            rsh = ssh_conn.invoke_shell()
            print "Initiated interactive shell session\n"

            # Read the initial prompt data from the channel and display it
            output = rsh.recv(RCV_BUFF_SIZE)
            print "%s\n" % output

            # Turn off CLI paging
            cli_disable_paging(rsh)

            # Get list of interfaces available on the device and display it
            output = cli_get_interfaces(rsh)
            print "%s\n" % output
        except (paramiko.SSHException) as e:
            print "!!!Error: %s\n" % e
        finally:
            disconnect_ssh(ssh_conn)
            print "Closed SSH connection to %s\n" % IP_ADDR
    else:
        print "SSH connection to %s has failed\n" % IP_ADDR
