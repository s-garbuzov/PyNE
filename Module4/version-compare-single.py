#!/usr/bin/python

# description:
# this script does the following:
#     logs into an IOS device via telnet
#     gets the version of the device
#     compares the version to an expected version
#     prints whether version correctly compares to the expected version


import re
import pexpect
import sys


def get_user_info():
    device_ip = raw_input('Device IP: ')
    device_username = 'admin'
    device_password = 'cisco'
    return (device_ip, device_username, device_password)


def get_telnet_session_info():
    device_prompt = '[>#]'
    telnet_timeout = 5
    version_pattern = re.compile('.*Version(.*?)\[')
    version_expected = '15.2(20150630:022638)'
    return (device_prompt, telnet_timeout, version_pattern, version_expected)


def establish_telnet_session(device_ip, device_username, device_password,
                             device_prompt, telnet_timeout):
    device_enable_password = device_password
    telnet_command = 'telnet ' + device_ip

    # telnet to device
    telnet_session = pexpect.spawn(telnet_command, timeout=telnet_timeout)

    result = telnet_session.expect(['Username:', pexpect.EOF, pexpect.TIMEOUT])

    # if you are presented with a username prompt, login and prep session
    if result==0:
        telnet_session.sendline(device_username)
        telnet_session.expect('Password:')
        telnet_session.sendline(device_password)
        telnet_session.expect(device_prompt)
        telnet_session.sendline('enable')
        telnet_session.expect('Password:')
        telnet_session.sendline(device_enable_password)
        telnet_session.expect(device_prompt)
        telnet_session.sendline('terminal length 0')
        telnet_session.expect(device_prompt)
        return telnet_session

    # an EOF indicates the telnet executable exited
    elif result==1:
        sys.exit('Telnet exited unexpectedly while trying to connect to ' + device_ip)

    # pexpect timed out waiting for another match condition
    elif result==2:
        sys.exit('Pexpect timed out waiting for a username prompt on ' + device_ip)


def compare_version_info(telnet_session, device_prompt, version_pattern):
    telnet_session.sendline('show version')
    telnet_session.expect(device_prompt)

    show_version_output = telnet_session.before

    show_version_output_lines = show_version_output.splitlines()
    for line in show_version_output_lines:
        if version_pattern.match(line):
            device_version = re.search(version_pattern, line)
            device_version = device_version.group(1).lstrip().rstrip()
            break

    return device_version


def send_message (device_ip, device_version, version_expected):
    if device_version == version_expected:
        print device_ip + ' version correct: ' + device_version + '\n'
    else:
        print device_ip + ' version incorrect: ' + device_version + \
              ', expected version: ' + version_expected + '\n'


def close_telnet_session(telnet_session):
    telnet_session.sendline('quit')
    telnet_session.kill(0)


def main():
    (device_ip, device_username, device_password) = get_user_info()
    
    (device_prompt, telnet_timeout, version_pattern, version_expected) = \
            get_telnet_session_info()
    
    telnet_session = establish_telnet_session(device_ip, device_username,
            device_password, device_prompt, telnet_timeout)
    
    device_version = compare_version_info(telnet_session, device_prompt,
            version_pattern)
    
    send_message (device_ip, device_version, version_expected)

    close_telnet_session(telnet_session)


if __name__ == '__main__':
    main ()
