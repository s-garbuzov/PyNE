#!/usr/bin/env python

"""
cli_command_telnet.py

Example of a script that executes CLI commands on a remote
device via TELNET connection.
NOTE: CLI commands are device specific, so this script
      needs to be adapted to a concrete device.
"""

# built-in modules
import telnetlib


# Remote device TELNET session specific info
device = {
    'ip_addr': '172.22.17.110',
    'port': 23,
    'timeout': 3,
    'username': 'vyatta',
    'password': 'vyatta',
    'verbose': True
}

# CLI specific data
OPER_PROMPT = '$'
ADMIN_PROMPT = '#'


def disable_cli_paging(telnet_conn, read_delay=1):
    """
    Disable CLI paging on a remote device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to a remote server.
    :param int timeout: TELNET session timeout
    :return: True on success, False otherwise
    """

    # Execute the command
    cmd = 'set terminal length 0\n'
    telnet_conn.write(cmd)

    # Read device output until one from a list of regular expressions
    # matches or until timeout
    r = telnet_conn.expect(['Invalid command', '\%s' % OPER_PROMPT],
                           read_delay)
    if r[0] != 1:
        # Flush out the read buffer
        telnet_conn.read_until(OPER_PROMPT, read_delay)
        return False
    else:
        return True


def enter_cli_cfg_mode(telnet_conn, read_delay=1):
    """
    Enter CLI configuration mode on a remote device.
    :param telnetlib.Telnet telnet_conn: an instance of TELNET client
        connected to a remote server.
    :param int timeout: TELNET session timeout
    :return: True on success, False otherwise
    """

    # Execute the command
    cmd = "configure\n"
    telnet_conn.write(cmd)

    # Read device output until one from a list of regular expressions
    # matches or until timeout
    r = telnet_conn.expect(['Invalid command', ADMIN_PROMPT], read_delay)
    if r[0] != 1:
        # Flush out the read buffer
        telnet_conn.read_until(OPER_PROMPT, read_delay)
        return False
    else:
        return True


def connect_telnet(device, verbose=False):
    """
    Establish TELNET connection to a remote device.

    :param dict device: dictionary containing information for establishing
                        TELNET session to a target device.
    :param bool verbose: enables code execution trace log.
    :return: an instance of telnetlib.Telnet class connected
             to remote TELNET server on success, None otherwise.
    """

    try:
        # Create an instance object of the 'Telnet' class
        rconn = telnetlib.Telnet()

        # uncomment following line to enable 'telnetlib' debug tracing
        # rconn.set_debuglevel(1)

        # Connect to device
        ip_addr = device['ip_addr']
        port = device['port']
        timeout = device['timeout']
        rconn.open(ip_addr, port, timeout)
        # Login to device
        uname = device['username']
        if uname:
                rconn.read_until('login:')
                rconn.write('%s\n' % uname)
        pswd = device['password']
        if pswd:
            rconn.read_until('assword:')
            rconn.write('%s\n' % pswd)

        # Read device output until one from a list of regular expressions
        # matches or until timeout
        r = rconn.expect(['Login incorrect', '\%s' % OPER_PROMPT], timeout)
        if r[0] == -1:
            return None
        else:
            return rconn
    except (Exception) as e:
        if(verbose):
            print "!!!Error: %s " % e
        return None


def disconnect_telnet(rconn):
    """Close TELNET connection to a remote device"""
    try:
        rconn.close()
    except (Exception) as e:
        print "!!!Error, %s " % e


def execute_command(device, cli_command, read_delay=1):
    """Execute a CLI command on a remote device over established TELNET channel.
    :param dict device: dictionary containing information for establishing
                        TELNET session to a target device.
    :param str cli_command: CLI command to be executed.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: output of the command on success, error message otherwise.
    """

    assert(isinstance(device, dict))

    verbose = device['verbose']
    # Connect to device and execute the command
    telnet_conn = connect_telnet(device, verbose)
    if telnet_conn:
        if(verbose):
            print("Established TELNET connection to %s:%s\n" %
                  (device['ip_addr'], device['port']))

        # Turn off CLI paging and enter configuration mode
        disable_cli_paging(telnet_conn, read_delay)
        enter_cli_cfg_mode(telnet_conn, read_delay)

        # Execute and wait for command completion,
        # then read result from the receive buffer
        telnet_conn.write(cli_command)

        # Returns a tuple of three items: the index in the list of the
        # first regular expression that matches; the match object
        # returned; and the text read up till and including the match.
        dummy, match, text = \
            telnet_conn.expect(['Invalid command', ADMIN_PROMPT], read_delay)
        if match is None:
            output = "Failed to execute command"
            # Flush out the read buffer
            telnet_conn.read_until(ADMIN_PROMPT, read_delay)
        else:
            output = text

        # Terminate TELNET session
        disconnect_telnet(telnet_conn)
        if(verbose):
            print("Closed TELNET connection to %s:%s\n" %
                  (device['ip_addr'], device['port']))
    else:
        output = "Failed to execute command"
        if(verbose):
            print("TELNET connection to %s:%s has failed\n" %
                  (device['ip_addr'], device['port']))

    return output

if __name__ == '__main__':
    cmd_string = "show interfaces\n"
    output = execute_command(device, cmd_string, read_delay=1)
    print output
