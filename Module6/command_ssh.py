#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via SSH connection.
NOTE: CLI commands are device specific, so this script
      needs to be adapted to a concrete device.

cli_command_ssh.py
"""

# built-in modules
import time
import socket

# third-party modules
import paramiko

# Remote device SSH session specific info
device = {
    'ip_addr': '172.22.17.110',
    'port': 830,
    'timeout': 3,
    'username': 'vyatta',
    'password': 'vyatta',
    'secret': 'secret',
    'verbose': True
}

# The maximum amount of data to be received at once
MAX_RCV_BUFFER = 1000


def disable_cli_paging(rsh):
    """
    Disable CLI paging on a remote device.
    :param paramiko.channel.Channel rsh: channel connected to a remote shell.
    :return: None
    """

    cmd = 'set terminal length 0\n'
    # Execute the command (wait for command to complete)
    rsh.send(cmd)
    time.sleep(1)

    # Flush out the receive buffer
    rsh.recv(MAX_RCV_BUFFER)


def enter_cli_cfg_mode(rsh):
    """
    Enter CLI configuration mode on a remote device.
    :param paramiko.channel.Channel rsh: channel connected to a remote shell.
    :return: None
    """

    cmd = "configure\n"
    # Execute the command (wait for command to complete)
    rsh.send(cmd)
    time.sleep(1)

    # Flush out the receive buffer
    rsh.recv(MAX_RCV_BUFFER)


def connect_ssh(device, verbose=False):
    """
    Establish SSH connection to a remote device.

    :param dict device: dictionary containing information for establishing
                        SSH session to a target device.
    :param bool verbose: enables code execution trace log.
    :return: an instance of paramiko.SSHClient class connected
             to remote SSH server on success, None otherwise.
    """

    try:
        # Create an instance object of the 'SSHClient' class
        rconn = paramiko.SSHClient()

        # Allow auto adding of unknown hosts to the known hosts in local
        # SSH configuration (make sure it is okay with your security
        # policy requirements)
        rconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # o 'look_for_keys' is set to False to disable searching
        #   for discoverable private key files in '~/.ssh/'
        # o 'allow_agent' is set to False to disable connecting
        #   to the SSH agent on the local machine for obtaining
        #   the private key
        rconn.connect(hostname=device['ip_addr'], port=device['port'],
                      username=device['username'], password=device['password'],
                      look_for_keys=False, allow_agent=False,
                      timeout=device['timeout'])
        return rconn
    except (paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException,
            socket.error) as e:
        if(verbose):
            print "!!!Error: %s " % e
        return None


def disconnect_ssh(rconn, verbose=False):
    """Close active SSH connection to a remote device.
    :param paramiko.SSHClient rconn: object instance connected
             to a remote SSH server.
    :param bool verbose: enables code execution trace log
    :return: None
    """
    try:
        rconn.close()
    except (Exception) as e:
        if(verbose):
            print "!!!Error, %s " % e


def execute_command(device, cli_command, read_delay=1):
    """Execute a CLI command on a remote device over established SSH channel.
    :param dict device: dictionary containing information for establishing
                        SSH session to a target device.
    :param str cli_command: CLI command to be executed.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: output of the command on success, error message otherwise.
    """

    assert(isinstance(device, dict))
    output = None
    verbose = device['verbose']

    # Connect to device and execute the command
    ssh_conn = connect_ssh(device, verbose)
    if ssh_conn:
        try:
            if(verbose):
                print("Established SSH connection to %s:%s\n" %
                      (device['ip_addr'], device['port']))

            # Start an interactive shell session on the remote SSH server
            # (read initial prompt data just to flush the receive buffer)
            rsh = ssh_conn.invoke_shell()
            rsh.recv(MAX_RCV_BUFFER)

            # Turn off CLI paging and enter configuration mode
            disable_cli_paging(rsh)
            enter_cli_cfg_mode(rsh)

            # Execute and wait for command completion,
            # then read result from the receive buffer
            rsh.send(cli_command)
            time.sleep(read_delay)
            output = rsh.recv(MAX_RCV_BUFFER)
        except (paramiko.SSHException) as e:
            output = "Failed to execute command"
            if(verbose):
                print("!!!Error: %s\n" % e)
        finally:
            disconnect_ssh(ssh_conn, verbose)
            if(verbose):
                print("Closed SSH connection to %s:%s\n" %
                      (device['ip_addr'], device['port']))
    else:
        output = "Failed to execute command"
        if(verbose):
            print("SSH connection to %s:%s has failed\n" %
                  (device['ip_addr'], device['port']))

    return output


if __name__ == '__main__':
    cmd_string = "show interfaces\n"
    output = execute_command(device, cmd_string, read_delay=1)
    print output
