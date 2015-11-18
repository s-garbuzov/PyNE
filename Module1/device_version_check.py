#!/usr/bin/python

# description:
# this script does the following:
#     takes a list of device IP addresses (provided in a file)
#     logs into each device via telnet
#     gets the version of the device
#     writes the version for each device to a file


import re
import pexpect
import sys

def get_credentials():
    device_username = 'admin'
    device_password = 'cisco'
    return (device_username, device_password)


def get_telnet_session_info():
    device_prompt = '[>#]'
    telnet_timeout = 30
    return (device_prompt, telnet_timeout)


def get_device_list():
    device_list = []
    device_file_name = './device-list.txt'

    device_file_object = open(device_file_name, 'r')

    for line in device_file_object:
        device_list.append(line.rstrip())

    device_file_object.close()

    return device_list


def establish_telnet_session(device_username, device_password, device_ip, \
                             device_prompt, telnet_timeout):
    device_enable_password = device_password
    telnet_command = 'telnet ' + device_ip

    # telnet to device
    telnet_session = pexpect.spawn(telnet_command, timeout=telnet_timeout)

    result = telnet_session.expect(['Username:', pexpect.EOF, \
             pexpect.TIMEOUT])

    # if you are presented with a username prompt, do this
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

    # an EOF will indicate the telnet executable exited
    elif result==1:
        sys.exit('Telnet exited unexpectedly while trying to connect to ' + device_ip)

    # pexpect timed out waiting for another match condition
    elif result==2:
        sys.exit('Pexpect timed out waiting for a username prompt on ' + device_ip)


def get_version_info(telnet_session, device_prompt):
    version_pattern = re.compile('Version(.*?)\[')

    telnet_session.sendline('show version')
    telnet_session.expect(device_prompt)

    show_version_output = telnet_session.before

    show_version_output_lines = show_version_output.splitlines()
    for line in show_version_output_lines:
        if version_pattern.search(line):
            device_version = re.search(version_pattern, line)
            device_version = device_version.group(1).lstrip().rstrip()

    return device_version


def close_telnet_session(telnet_session):
    telnet_session.sendline('quit')
    telnet_session.kill(0)


def main():
    (device_username, device_password) = get_credentials()
    (device_prompt, telnet_timeout) = get_telnet_session_info()
    device_list = get_device_list()

    version_output_filename = 'device-version-info.txt'
    results_file_object = open(version_output_filename, 'w')

    for device_ip in device_list:
        telnet_session = establish_telnet_session(device_username, \
                    device_password, device_ip, device_prompt, telnet_timeout)
        device_version = get_version_info(telnet_session, device_prompt)
        close_telnet_session(telnet_session)
        results_file_object.write(device_ip + ',' + device_version + '\n')

    results_file_object.close()


if __name__ == '__main__':
    main ()
