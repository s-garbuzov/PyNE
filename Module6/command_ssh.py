#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device over established SSH connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.

NOTES: Requires installation of the 'paramiko' Python package
          pip install paramiko
       The 'paramiko' package is documented at:
          http://docs.paramiko.org
       Complete set of SSH client operations is available at:
          http://docs.paramiko.org/en/1.15/api/client.html

command_ssh.py

"""

# built-in modules
import time
import socket

# third-party modules
import paramiko


def disable_cli_paging(device, remote_shell):
    """
    Disable CLI paging on a remote device.
    :param dict device: dictionary containing target device information.
    :param paramiko.channel.Channel rsh: channel connected to a remote shell.
    :return: None
    """

    cmd = 'set terminal length 0\n'
    # Execute the command (wait for command to complete)
    remote_shell.send(cmd)
    time.sleep(1)

    # Flush out the receive buffer
    remote_shell.recv(device['max_bytes'])


def enter_cli_cfg_mode(device, remote_shell):
    """
    Enter CLI configuration mode on a remote device.
    :param dict device: dictionary containing target device information.
    :param paramiko.channel.Channel rsh: channel connected to a remote shell.
    :return: None
    """

    cmd = "configure\n"
    # Execute the command (wait for command to complete)
    remote_shell.send(cmd)
    time.sleep(1)

    # Flush out the receive buffer
    remote_shell.recv(device['max_bytes'])


def connect_ssh(device):
    """
    Establish SSH connection to a remote device.

    :param dict device: dictionary containing information for establishing
                        SSH session to a target device.
    :return: an instance of paramiko.SSHClient class connected
             to remote SSH server on success, None otherwise.
    """

    try:
        # Create an instance object of the 'SSHClient' class
        ssh_client = paramiko.SSHClient()

        # Allow auto adding of unknown hosts to the known hosts in local
        # SSH configuration (make sure it is okay with your security
        # policy requirements)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # o 'look_for_keys' is set to False to disable searching
        #   for discoverable private key files in '~/.ssh/'
        # o 'allow_agent' is set to False to disable connecting
        #   to the SSH agent on the local machine for obtaining
        #   the private key
        ssh_client.connect(hostname=device['ip_addr'], port=device['port'],
                           username=device['username'],
                           password=device['password'],
                           look_for_keys=False, allow_agent=False,
                           timeout=device['timeout'])
        if(device['verbose']):
            print("SSH connection to %s:%s has been established" %
                  (device['ip_addr'], device['port']))
        return ssh_client
    except (paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException,
            socket.error) as e:
        print "!!!Error: %s " % e
        return None


def disconnect_ssh(device, ssh_client):
    """Close active SSH connection to a remote device.
    :param paramiko.SSHClient rconn: object instance connected
        to a remote SSH server.
    :return: None
    """
    try:
        ssh_client.close()
        if(device['verbose']):
            print("SSH connection to %s:%s has been closed" %
                  (device['ip_addr'], device['port']))
    except (Exception) as e:
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

    # Connect to remote SSH server running on the device
    ssh_conn = connect_ssh(device)
    if ssh_conn:
        try:
            # Start an interactive shell session on the remote SSH server
            # (read initial prompt data just to flush the receive buffer)
            remote_shell = ssh_conn.invoke_shell()
            remote_shell.recv(device['max_bytes'])

            # Turn off CLI paging and enter configuration mode
            disable_cli_paging(device, remote_shell)
            enter_cli_cfg_mode(device, remote_shell)

            # Execute and wait for command completion,
            # then read result from the receive buffer
            remote_shell.send(cli_command)
            time.sleep(read_delay)
            output = remote_shell.recv(device['max_bytes'])
            if((device['verbose'])):
                print("CLI command %r has been executed" % cli_command)
        except (paramiko.SSHException) as e:
            output = "Failed to execute command"
            print("!!!Error: %s\n" % e)
        finally:
            # Terminate SSH session
            disconnect_ssh(device, ssh_conn)
    else:
        output = "Failed to execute command"
        if(device['verbose']):
            print("SSH connection to %s:%s has failed\n" %
                  (device['ip_addr'], device['port']))

    return output


def main():
    # Remote device SSH session specific info
    device = {
        'ip_addr': '172.22.17.110',
        'port': 830,
        'timeout': 3,
        'username': 'vyatta',
        'password': 'vyatta',
        'secret': 'secret',
        'max_bytes': 1000,  # The maximum amount of data to be received at once
        'verbose': True
    }

    cmd_string = "show interfaces\n"
    print("\nCommand to be executed: %s" % cmd_string)
    output = execute_command(device, cmd_string, read_delay=1)
    print("\nCommand execution result:\n")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print output
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("\n")


if __name__ == '__main__':
    main()
