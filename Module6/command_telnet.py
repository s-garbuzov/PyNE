#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via TELNET connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Cisco IOS-XR device.

command_telnet.py

"""

# built-in modules
import time
import telnetlib


def enable_privileged_commands(device_info, telnet_conn, read_delay=1):
    """Turn on privileged commands execution.
    :param dict device_info: dictionary containing information
        about target device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to the device.
    :param int read_delay: time to wait for the CLI command to complete.
    """
    cmd = "enable\n"
    telnet_conn.write(cmd)
    password_prompt = device_info['password_prompt']
    dummy, match, dummy = telnet_conn.expect([password_prompt], read_delay)
    if(match is not None):
        password = "%s\n" % device_info['password']
        telnet_conn.write(password)
        admin_prompt = device_info['admin_prompt']
        telnet_conn.expect([admin_prompt], read_delay)


def disable_paging(device_info, telnet_conn, read_delay=1):
    """
    Disable CLI paging on a remote device.
    :param dict device_info: dictionary containing information
        about target device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to a remote server.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: True on success, False otherwise
    """

    # Execute the command
    cmd = 'terminal length 0\n'
    telnet_conn.write(cmd)
    oper_prompt = "%r" % device_info['oper_prompt']
    admin_prompt = device_info['admin_prompt']
    dummy, match, dummy = telnet_conn.expect([oper_prompt, admin_prompt],
                                             read_delay)
    if(match is not None):
        return True
    else:
        return False


def check_config_mode(device_info, telnet_conn):
    """
    Check if CLI on the device is in configuration mode.
    :param dict device_info: dictionary containing information
        about target device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to the device.
    :return: True if CLI is in configuration mode, False otherwise
    Returns a boolean
    """
    cmd = '\n'
    telnet_conn.write(cmd)
    config_prompt = "(%s)%s" % ('config', device_info['admin_prompt'])
    idx, dummy, dummy = telnet_conn.expect([config_prompt], timeout=1)
    if(idx == 0):
        return True
    else:
        return False


def enter_config_mode(device_info, telnet_conn, read_delay=1):
    """
    Enter CLI configuration mode on a remote device.
    :param dict device_info: dictionary containing information
        about target device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to the device.
    :param int read_delay: time to wait for command completion
    :return: True on success, False otherwise
    """

    if(check_config_mode(device_info, telnet_conn) is True):
        return True

    cmd = "configure terminal\n"
    telnet_conn.write(cmd)
    config_prompt = "(%s)%s" % ('config', device_info['admin_prompt'])
    idx, dummy, dummy = telnet_conn.expect([config_prompt], read_delay)
    if(idx == 0):
        return True
    else:
        return True


def connect_telnet(device_info):
    """
    Establish TELNET connection to a remote device.
    :param dict device_info: dictionary containing information
        about target device.
    :return: an instance of telnetlib.Telnet class connected
        to remote TELNET server on success, None otherwise.
    """

    try:
        # Create an instance object of the 'Telnet' class
        telnet_client = telnetlib.Telnet()

        # uncomment following line to enable 'telnetlib' debug tracing
        # telnet_client.set_debuglevel(1)

        # Connect to device
        ip_addr = device_info['ip_addr']
        port = device_info['port']
        timeout = device_info['timeout']
        if(device_info['verbose']):
            print("Connecting to %s:%s" %
                  (device_info['ip_addr'], device_info['port']))
        telnet_client.open(ip_addr, port, timeout)
        if(device_info['verbose']):
            print("Connection to %s:%s has been established" %
                  (device_info['ip_addr'], device_info['port']))

        # Login to device
        uname = device_info['username']
        if uname:
            login_prompt = device_info['login_prompt']
            response = telnet_client.read_until(login_prompt, timeout)
            if login_prompt not in response:
                disconnect_telnet(device_info, telnet_client)
                err_msg = ("Failed to get expected '%s' login prompt" %
                           login_prompt)
                raise ValueError(err_msg)
            telnet_client.write('%s\n' % uname)

        pswd = device_info['password']
        if pswd:
            pswd_prompt = device_info['password_prompt']
            response = telnet_client.read_until(pswd_prompt, timeout)
            if pswd_prompt not in response:
                disconnect_telnet(device_info, telnet_client)
                err_msg = ("Failed to get expected '%s' password prompt" %
                           pswd_prompt)
                raise ValueError(err_msg)
            telnet_client.write('%s\n' % pswd)

        # Check if we got to the console prompt
        oper_prompt = device_info['oper_prompt']
        admin_prompt = device_info['admin_prompt']
        dummy, match, dummy = \
            telnet_client.expect([oper_prompt, admin_prompt], timeout)
        if(match is None):
            disconnect_telnet(device_info, telnet_client)
            err_msg = ("Login failed (uname=%s, pswd=%s)" % (uname, pswd))
            raise ValueError(err_msg)

        if(device_info['verbose']):
            print("Successfully logged on to %s:%s" %
                  (device_info['ip_addr'], device_info['port']))

        return telnet_client

    except (Exception) as e:
        print "!!!Error: %s " % e
        return None


def disconnect_telnet(device_info, telnet_client):
    """Close TELNET connection to a remote device
    :param dict device_info: dictionary containing information
        about target device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to the device.
    """
    try:
        telnet_client.close()
        if(device_info['verbose']):
            print("Connection to %s:%s has been closed" %
                  (device_info['ip_addr'], device_info['port']))
    except (Exception) as e:
        print "!!!Error: %s " % e


def execute_command(device_info, cmd_string, read_delay=1):
    """Execute a CLI command on a remote device over established TELNET channel.
    :param dict device_info: dictionary containing information
        about target device.
    :param str cmd_string: CLI command to be executed.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: output of the command on success, error message otherwise.
    """

    assert(isinstance(device_info, dict))
    output = None

    # Connect to device and execute the command
    telnet_conn = connect_telnet(device_info)
    if(telnet_conn is not None):
        # Enter privilege mode and turn off CLI paging
        enable_privileged_commands(device_info, telnet_conn, read_delay)
        disable_paging(device_info, telnet_conn, read_delay)

        # Execute command and wait for command completion
        telnet_conn.write(cmd_string)
        if((device_info['verbose'])):
            print("CLI command %r has been executed" % cmd_string)
        time.sleep(read_delay)

        # Read result from the receive buffer
        # 'expect' call returns a tuple of three items:
        # - the index in the list of the first regular expression
        #   that matches
        # - the match object returned
        # - the text read up till and including the match
        oper_prompt = device_info['oper_prompt']
        admin_prompt = device_info['admin_prompt']
        dummy, match, text = \
            telnet_conn.expect([oper_prompt, admin_prompt], read_delay)
        if match is not None:
            output = text

        # Close connection
        disconnect_telnet(device_info, telnet_conn)

    return output


def main():
    # Remote device TELNET session specific info
    device_info = {
        'ip_addr': '10.0.0.1',
        'port': 23,
        'timeout': 3,
        'username': 'cisco',
        'password': 'cisco',
        'login_prompt': 'sername:',
        'password_prompt': 'assword:',
        'oper_prompt': '>',
        'admin_prompt': '#',
        'secret': 'cisco',
        'verbose': True
    }

    cmd_string = "show ipv4 interface brief\n"
    print("\nCommand to be executed: %s" % cmd_string)
    output = execute_command(device_info, cmd_string, read_delay=1)
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
