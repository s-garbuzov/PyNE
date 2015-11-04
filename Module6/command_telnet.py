#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via TELNET connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Cisco IOS device.

command_telnet.py

"""

# built-in modules
import time
import telnetlib


def disable_cli_paging(device, telnet_conn, read_delay=1):
    """
    Disable CLI paging on a remote device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to a remote server.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: True on success, False otherwise
    """

    # Execute the command
    cmd = 'terminal length 0\n'
    telnet_conn.write(cmd)
    oper_prompt = "%r" % device['oper_prompt']
    config_prompt = device['config_prompt']
    dummy, match, dummy = telnet_conn.expect([oper_prompt, config_prompt],
                                             read_delay)
    if(match is not None):
        return True
    else:
        return False


def check_config_mode(device, telnet_conn):
    """
    Check if CLI on the device is in configuration mode.
    :param dict device: dictionary containing information about target device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to the device.
    :return: True if CLI is in configuration mode, False otherwise
    Returns a boolean
    """
    cmd = '\n'
    telnet_conn.write(cmd)
    config_prompt = device['config_prompt']
    idx, dummy, dummy = telnet_conn.expect([config_prompt])
    if(idx == 0):
        return True
    else:
        return False


def enter_cli_cfg_mode(device, telnet_conn, read_delay=1):
    """
    Enter CLI configuration mode on a remote device.
    :param dict device: dictionary containing information about target device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to the device.
    :param int read_delay: time to wait for command completion
    :return: True on success, False otherwise
    """

    if(check_config_mode(device, telnet_conn) is True):
        return True

    cmd = "configure\n"
    telnet_conn.write(cmd)
    config_prompt = device['config_prompt']
    idx, dummy, dummy = telnet_conn.expect([config_prompt], read_delay)
    if(idx == 0):
        return True
    else:
        return True


def connect_telnet(device):
    """
    Establish TELNET connection to a remote device.
    :param dict device: dictionary containing information about target device.
    :return: an instance of telnetlib.Telnet class connected
        to remote TELNET server on success, None otherwise.
    """

    try:
        # Create an instance object of the 'Telnet' class
        telnet_client = telnetlib.Telnet()

        # uncomment following line to enable 'telnetlib' debug tracing
        # telnet_client.set_debuglevel(1)

        # Connect to device
        ip_addr = device['ip_addr']
        port = device['port']
        timeout = device['timeout']
        if(device['verbose']):
            print("Connecting to %s:%s" % (device['ip_addr'], device['port']))
        telnet_client.open(ip_addr, port, timeout)
        if(device['verbose']):
            print("Connection to %s:%s has been established" %
                  (device['ip_addr'], device['port']))

        # Login to device
        uname = device['username']
        if uname:
            login_prompt = device['login_prompt']
            response = telnet_client.read_until(login_prompt, timeout)
            if login_prompt not in response:
                disconnect_telnet(device, telnet_client)
                err_msg = ("Failed to get expected '%s' login prompt" %
                           login_prompt)
                raise ValueError(err_msg)
                return None
            telnet_client.write('%s\n' % uname)

        pswd = device['password']
        if pswd:
            pswd_prompt = device['password_prompt']
            response = telnet_client.read_until(pswd_prompt, timeout)
            if pswd_prompt not in response:
                disconnect_telnet(device, telnet_client)
                err_msg = ("Failed to get expected '%s' password prompt" %
                           pswd_prompt)
                raise ValueError(err_msg)
                return None
            telnet_client.write('%s\n' % pswd)

        # Check if we got to the console prompt
        oper_prompt = "%r" % device['oper_prompt']
        config_prompt = device['config_prompt']
        dummy, match, dummy = \
            telnet_client.expect([oper_prompt, config_prompt], timeout)
        if(match is None):
            disconnect_telnet(device, telnet_client)
            err_msg = ("Login failed (uname=%s, pswd=%s)" % (uname, pswd))
            raise ValueError(err_msg)
            return None

        if(device['verbose']):
            print("Successfully logged on to %s:%s" %
                  (device['ip_addr'], device['port']))

        return telnet_client

    except (Exception) as e:
        print "!!!Error: %s " % e
        return None


def disconnect_telnet(device, telnet_client):
    """Close TELNET connection to a remote device
    :param dict device: dictionary containing information about target device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to the device.
    """
    try:
        telnet_client.close()
        if(device['verbose']):
            print("Connection to %s:%s has been closed" %
                  (device['ip_addr'], device['port']))
    except (Exception) as e:
        print "!!!Error: %s " % e


def execute_command(device, cli_command, read_delay=1):
    """Execute a CLI command on a remote device over established TELNET channel.
    :param dict device: dictionary containing information about target device.
    :param str cli_command: CLI command to be executed.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: output of the command on success, error message otherwise.
    """

    assert(isinstance(device, dict))
    output = None

    # Connect to device and execute the command
    telnet_conn = connect_telnet(device)
    if(telnet_conn is not None):
        # Turn off CLI paging and enter configuration mode
        disable_cli_paging(device, telnet_conn, read_delay)
        enter_cli_cfg_mode(device, telnet_conn, read_delay)

        # Execute command and wait for command completion
        telnet_conn.write(cli_command)
        if((device['verbose'])):
            print("CLI command %r has been executed" % cli_command)
        time.sleep(read_delay)

        # Read result from the receive buffer
        # 'expect' call returns a tuple of three items:
        # - the index in the list of the first regular expression
        #   that matches
        # - the match object returned
        # - the text read up till and including the match
        oper_prompt = "%r" % device['oper_prompt']
        config_prompt = device['config_prompt']
        dummy, match, text = \
            telnet_conn.expect([oper_prompt, config_prompt], read_delay)
        if match is not None:
            output = text

        # Close connection
        disconnect_telnet(device, telnet_conn)

    return output


def main():
    # Remote device TELNET session specific info
    device = {
        'ip_addr': '172.22.17.111',
        'port': 23,
        'timeout': 3,
        'username': 'testuser',
        'password': 'testpassword',
        'login_prompt': 'sername:',
        'password_prompt': 'assword:',
        'oper_prompt': '$',
        'config_prompt': '#',
        'secret': 'secret',
        'verbose': True
    }

    cmd_string = "show interfaces\n"
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
