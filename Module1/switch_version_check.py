#!/usr/bin/python

# description:
# this script does the following:
#     takes a list of switch IP addresses (provided in a file)
#     logs into each switch via telnet
#     gets the version of the switch
#     writes the version for each switch to a file


import re
import pexpect
import sys

def get_credentials():
    switch_username = 'admin'
    switch_password = 'cisco'
    return (switch_username, switch_password)


def get_telnet_session_info():
    switch_prompt = '[>#]'
    telnet_timeout = 30
    #version_pattern = re.compile('\s*system\:\s+.*')
    version_pattern = re.compile('Cisco\ IOS\ Software')
    return (switch_prompt, telnet_timeout, version_pattern)


def get_switch_list():
    switch_list = []
    switch_file_name = './switch-list.txt'

    switch_file_object = open(switch_file_name, 'r')

    for line in switch_file_object:
        switch_list.append(line)

    switch_file_object.close()

    return switch_list


def establish_telnet_session(switch_username, switch_password, switch_ip, \
                             switch_prompt, telnet_timeout):
    switch_enable_password = switch_password
    telnet_command = 'telnet ' + switch_ip

    # telnet to switch
    telnet_session = pexpect.spawn(telnet_command, timeout=telnet_timeout)

    result = telnet_session.expect(['Username:', pexpect.EOF, \
             pexpect.TIMEOUT])

    # if you are presented with a username prompt, do this
    if result==0:
        telnet_session.sendline(switch_username)
        telnet_session.expect('Password:')
        telnet_session.sendline(switch_password)
        telnet_session.expect(switch_prompt)
        telnet_session.sendline('enable')
        telnet_session.expect('Password:')
        telnet_session.sendline(switch_enable_password)
        telnet_session.expect(switch_prompt)
        telnet_session.sendline('terminal length 0')
        telnet_session.expect(switch_prompt)
        return telnet_session

    # an EOF will indicate the telnet executable exited
    elif result==1:
        sys.exit('Telnet exited unexpectedly while trying to connect to ' + switch_ip)

    # pexpect timed out waiting for another match condition
    elif result==2:
        sys.exit('Pexpect timed out waiting for a username prompt on ' + switch_ip)


def get_version_info(telnet_session, switch_prompt, version_pattern):

    telnet_session.sendline('show version')
    telnet_session.expect(switch_prompt)

    show_version_output = telnet_session.before

    show_version_output_lines = show_version_output.splitlines()
    for line in show_version_output_lines:
        if version_pattern.match(line):
            switch_version = line

    return switch_version


def close_telnet_session(telnet_session):
    telnet_session.sendline('quit')
    telnet_session.kill(0)


def main():
    (switch_username, switch_password) = get_credentials()
    (switch_prompt, telnet_timeout, version_pattern) = \
            get_telnet_session_info()
    switch_list = get_switch_list()

    version_output_filename = 'switch-version-info.txt'
    results_file_object = open(version_output_filename, 'w')

    for switch_ip in switch_list:
        telnet_session = establish_telnet_session(switch_username, \
                    switch_password, switch_ip, switch_prompt, telnet_timeout)
        switch_version = get_version_info(telnet_session, switch_prompt, \
                    version_pattern)
        close_telnet_session(telnet_session)
        results_file_object.write(switch_ip + ',' + switch_version)

    results_file_object.close()


if __name__ == '__main__':
    main ()
