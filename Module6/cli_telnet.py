#!/usr/bin/env python

# Example of a script that executes CLI commands on a remote
# device via TELNET connection

# built-in modules
import telnetlib


# TELNET session specific data
IP_ADDR = '172.22.17.110'
PORT_NUM = 23
USERNAME = 'vyatta'
PASSWORD = 'vyatta'

# CLI session specific data
TIMEOUT = 5
OPER_PROMPT = '$'
ADMIN_PROMPT = '#'


def cli_disable_paging(rsh):
    """Execute CLI command that disables CLI paging on a remote device"""

    # Execute the command
    cmd = 'set terminal length 0\n'
    rsh.write(cmd)

    # Read device output until one from a list of regular expressions
    # matches or until timeout
    r = rsh.expect(['Invalid command', '\%s' % OPER_PROMPT], timeout=TIMEOUT)
    if r[0] != 1:
        print "!!!Failed to execute CLI command: %s" % cmd
        # Flush out the read buffer
        rsh.read_until(match=OPER_PROMPT, timeout=TIMEOUT)
        return False
    else:
        return True


def cli_enter_cfg_mode(rsh):
    """Execute CLI command for entering the configuration mode
    on a remote device
    """

    # Execute the command
    cmd = "configure\n"
    rsh.write(cmd)

    # Read device output until one from a list of regular expressions
    # matches or until timeout
    r = rsh.expect(['Invalid command', ADMIN_PROMPT], timeout=TIMEOUT)
    if r[0] != 1:
        print "!!!Failed to execute CLI command: %s" % cmd
        # Flush out the read buffer
        rsh.read_until(OPER_PROMPT, TIMEOUT)
        return False
    else:
        return True


def cli_get_interfaces(rsh):
    """Execute CLI command that shows interface information
    on a remote device
    """

    # Execute the command
    cmd = 'show interfaces\n'
    rsh.write(cmd)

    # Read device output until one from a list of regular expressions
    # matches or until timeout
    output = None
    r = rsh.expect([r'Invalid command', r'#'], timeout=TIMEOUT)
    if r[0] != 1:
        print "!!!Failed to execute CLI command: %s" % cmd
        # Flush out the read buffer
        rsh.read_until(ADMIN_PROMPT, timeout=TIMEOUT)
    else:
        output = r[2]

    return output


def connect_telnet(ip, port=23, uname=None, pswd=None, timeout=None):
    """
    Establish TELNET connection to a remote device.

    Returns:
        On success, instance object that represents connection
        to a remote TELNET server. None on failure.
    """

    # Create an instance object of the 'Telnet' class
    rconn = telnetlib.Telnet()

    # Establish TELNET connection
    try:
        # Uncomment the following line to enable 'telnetlib' debug tracing
        # rconn.set_debuglevel(1)

        # Connect to device
        rconn.open(ip, port, timeout)
        # Login to device
        if uname:
                rconn.read_until('login:')
                rconn.write('%s\n' % uname)
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
        print "!!!Error: %s " % e
        return None


def disconnect_telnet(rconn):
    """Close TELNET connection to a remote device"""
    try:
        rconn.close()
    except (Exception) as e:
        print "!!!Error, %s " % e


# Connect to a remote TELNET server and execute few CLI commands
telnet_conn = connect_telnet(ip=IP_ADDR, port=PORT_NUM,
                             uname=USERNAME, pswd=PASSWORD, timeout=TIMEOUT)
if telnet_conn:
    print "Established TELNET connection to %s\n" % IP_ADDR

    # Turn off CLI paging
    cli_disable_paging(telnet_conn)

    # Enter configuration mode
    cli_enter_cfg_mode(telnet_conn)

    # Read and show list of interfaces
    output = cli_get_interfaces(telnet_conn)
    print "%s\n" % output

    # Terminate TELNET session
    disconnect_telnet(telnet_conn)
    print "Closed TELNET connection to %s\n" % IP_ADDR
else:
    print "TELNET connection to %s has failed\n" % IP_ADDR
