#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device over established SSH connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Cisco IOS device.

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


def enable_privileged_commands(device, rsh):
    """Turn on privileged commands execution.
    :param dict device: dictionary containing information about target device.
    :param paramiko.channel.Channel rsh: channel connected to a remote shell.
    """
    cmd = "enable\n"
    # Execute the command (wait for command to complete)
    rsh.send(cmd)
    time.sleep(1)
    output = rsh.recv(device['max_bytes'])
    if(device['password_prompt'] in output):
        password = "%s\n" % device['password']
        rsh.send(password)
        rsh.recv(device['max_bytes'])


def disable_paging(device, rsh):
    """
    Disable CLI paging on a remote device.
    :param dict device: dictionary containing information about target device.
    :param paramiko.channel.Channel rsh: channel connected to a remote shell.
    :return: None
    """

    cmd = 'terminal length 0\n'
    # Execute the command (wait for command to complete)
    rsh.send(cmd)
    time.sleep(1)

    # Flush out the receive buffer
    rsh.recv(device['max_bytes'])


def check_config_mode(device, rsh):
    """
    Check if CLI on the device is in configuration mode.
    :param dict device: dictionary containing information about target device.
    :param paramiko.channel.Channel rsh: channel connected to a remote shell.
    :return: True if CLI is in configuration mode, False otherwise
    Returns a boolean
    """
    cmd = '\n'
    rsh.send(cmd)
    output = rsh.recv(device['max_bytes'])
    config_prompt = "(%s)%s" % ('config', device['admin_prompt'])
    if(config_prompt in output):
        return True
    else:
        return False


def enter_config_mode(device, rsh):
    """
    Enter CLI configuration mode on a remote device.
    :param dict device: dictionary containing information about target device.
    :param paramiko.channel.Channel rsh: channel connected to a remote shell.
    :return: None
    """

    if(check_config_mode(device, rsh) is True):
        return

    cmd = "configure terminal\n"
    # Execute the command (wait for command to complete)
    rsh.send(cmd)
    time.sleep(1)

    # Flush out the receive buffer
    rsh.recv(device['max_bytes'])


def connect_ssh(device):
    """
    Establish SSH connection to a remote device.
    :param dict device: dictionary containing information about target device.
    :return: an instance of paramiko.SSHClient class connected
        to the device on success, None on failure.
    """

    try:
        # Create an instance object of the 'SSHClient' class
        ssh_client = paramiko.SSHClient()

        # Allow auto adding of unknown hosts to the known hosts in local
        # SSH configuration (make sure it is okay with your security
        # policy requirements)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if(device['verbose']):
            print("Connecting to %s:%s" % (device['ip_addr'], device['port']))

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
            print("Connection to %s:%s has been established" %
                  (device['ip_addr'], device['port']))
        return ssh_client
    except (paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException,
            socket.error) as e:
        print "!!!Error: %s " % e
        return None


def disconnect_ssh(device, ssh_conn):
    """
    Close active SSH connection to a remote device.
    :param paramiko.SSHClient ssh_conn: object instance connected
        to a remote SSH server.
    :return: None
    """
    try:
        ssh_conn.close()
        if(device['verbose']):
            print("Connection to %s:%s has been closed" %
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

    # Connect to device
    ssh_conn = connect_ssh(device)
    if(ssh_conn is not None):
        try:
            # Start an interactive shell session on the remote SSH server
            # (read initial prompt data just to flush the receive buffer)
            remote_shell = ssh_conn.invoke_shell()
            remote_shell.recv(device['max_bytes'])

            # Enter privilege mode and turn off CLI paging
            enable_privileged_commands(device, remote_shell)
            disable_paging(device, remote_shell)

            # Execute and wait for command completion,
            # then read result from the receive buffer
            remote_shell.send(cli_command)
            time.sleep(read_delay)
            output = remote_shell.recv(device['max_bytes'])
            if((device['verbose'])):
                print("CLI command %r has been executed" % cli_command)
        except (paramiko.SSHException) as e:
            print("!!!Error: %s\n" % e)
        finally:
            # Close connection
            disconnect_ssh(device, ssh_conn)

    return output


def main():
    # Remote device SSH session specific info
    device = {
        'ip_addr': '10.30.30.3',
        'port': 22,
        'timeout': 3,
        'username': 'admin',
        'password': 'cisco',
        'login_prompt': 'sername:',
        'password_prompt': 'assword:',
        'oper_prompt': '>',
        'admin_prompt': '#',
        'secret': 'cisco',
        'max_bytes': 9000,  # The maximum amount of data to be received at once
        'verbose': True
    }

#    cmd_string = "show interfaces\n"
    cmd_string = "show interfaces | include line protocol\n"
    print("\nCommand to be executed: %s" % cmd_string)
    output = execute_command(device, cmd_string, read_delay=1)
    if(output is not None):
        print("\nCommand execution result:\n")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print output
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("\n")
    else:
        print("Failed to execute command")


if __name__ == '__main__':
    main()
