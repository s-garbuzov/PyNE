#!/usr/bin/python

# Description:
# Demonstrate pexpect EOF and TIMEOUT conditions.
# The script will send num_pings number of pings to the ping_target value.
# The script will print the results of the ping command, if it completes
# prior to a timeout condition.
#
# An EOF (end of file) condition will occur when the ping process exits.
# This is the only match condition set other than a TIMEOUT in this script.
#
# A timeout will occur, if no other type of specified match is found prior to
# the specified timeout value. The timeout value is set in the pexpect_timeout
# variable. In this script, the only other defined match condition is an EOF,
# which will occur when the ping command is complete.
#
# The TIMEOUT condition is measured in seconds.
#
# Pings are sent once per second by default.
#
# Modify the pexpect_timeout and num_pings values to generate a TIMEOUT
# condition.
#
# If you set the pexpect_timeout value lower than the num_pings value,
# then a timeout will occur.
#
# If you do not trap for a timeout condition by listing it as one of the
# possible match conditions for pexpect, then a timeout will halt script
# execution. This is often undesirable, especially within a loop.


import pexpect


def set_ping_parameters():
    pexpect_timeout = 10
    num_pings = 5
    ping_target = '192.168.1.1'
    ping_cmd = 'ping -c ' + str(num_pings) + ' ' + ping_target
    return (ping_cmd, pexpect_timeout)


def print_results(ping):
    cmd_result = ping.expect([pexpect.EOF, pexpect.TIMEOUT])

    # if an EOF is reached, do the following
    if cmd_result==0:        

        # print the output of the ping command that occurred before match
        ping_cmd_output = ping.before
        print ping_cmd_output

    # if no other match condition is met before the expiration of the timeout
    # value, then a timeout occurs
    if cmd_result==1:
        print '\nPexpect timed out prior to matching any other condition.\n'


def main():
    (ping_cmd, pexpect_timeout) = set_ping_parameters()
    ping = pexpect.spawn(ping_cmd, timeout=pexpect_timeout)
    print_results(ping)


if __name__ == '__main__':
    main ()
