#!/usr/bin/python

# description:
# this script does the following:
#     takes a list of switch IP addresses (provided in a file)
#     logs into each switch via telnet
#     gets the version of the switch
#     compares the version to an expected version
#     prints whether version correctly compares to the expected version


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
    #version_line_pattern = re.compile('Cisco\ IOS\ Software')
    version_pattern = re.compile('.*Version(.*?)\[')
    version_expected = '15.2(20150630:022638)'
    return (switch_prompt, telnet_timeout, version_pattern, version_expected)


def get_switch_list():
    switch_list = []
    switch_file_name = './switch-list.txt'
    switch_file_object = open(switch_file_name, 'r')

    for line in switch_file_object:
        switch_ip = line.rstrip()
        switch_list.append(switch_ip)

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


def compare_version_info(telnet_session, switch_prompt, version_pattern):
    telnet_session.sendline('show version')
    telnet_session.expect(switch_prompt)

    show_version_output = telnet_session.before

    show_version_output_lines = show_version_output.splitlines()
    for line in show_version_output_lines:
        if version_pattern.match(line):
            switch_version = re.search(version_pattern, line)
            switch_version = switch_version.group(1).lstrip().rstrip()
            break

    return switch_version


def send_message (switch_ip, switch_version, version_expected):
    if switch_version == version_expected:
        print switch_ip + ' version correct: ' + switch_version
    else:
        print switch_ip + ' version incorrect: ' + switch_version + \
              ', expected version: ' + version_expected


def close_telnet_session(telnet_session):
    telnet_session.sendline('quit')
    telnet_session.kill(0)


def main():
    (switch_username, switch_password) = get_credentials()
    (switch_prompt, telnet_timeout, version_pattern, version_expected) = \
            get_telnet_session_info()
    switch_list = get_switch_list()

    for switch_ip in switch_list:
        telnet_session = establish_telnet_session(switch_username, \
                switch_password, switch_ip, switch_prompt, telnet_timeout)
        switch_version = compare_version_info(telnet_session, switch_prompt, \
                version_pattern)
        send_message (switch_ip, switch_version, version_expected)
        close_telnet_session(telnet_session)


if __name__ == '__main__':
    main ()
