#!/usr/bin/python

# description:
# create a dictionary of device version information
# output the dictionary information to a file


import re
import pexpect
import sys


def get_device_list():
    device_list = []
    device_list_filename = 'device-ip-list.txt'
    device_list_file_object = open(device_list_filename, 'r')
    for ip_address in device_list_file_object:
        ip_address = ip_address.rstrip()
        device_list.append(ip_address)
    device_list_file_object.close()
    return device_list


def get_user_info():
    device_username = 'admin'
    device_password = 'cisco'
    return (device_username, device_password)


def get_telnet_session_info():
    device_prompt = '[>#]'
    telnet_timeout = 5
    return (device_prompt, telnet_timeout)


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


# get_version_info function assumes IOS in lab environment
def get_version_info(telnet_session, device_prompt):
    version_pattern = re.compile('Version(.*?)\[', re.MULTILINE)
    telnet_session.sendline('show version')
    telnet_session.expect(device_prompt)
    show_version_output = telnet_session.before
    try:
        device_version = re.search(version_pattern, show_version_output)
        device_version = device_version.group(1).lstrip().rstrip()
    except:
        device_version = 'unknown'
    return device_version


def close_telnet_session(telnet_session):
    telnet_session.sendline('quit')
    telnet_session.kill(0)


def write_device_information(device_version_dict):
    device_info_filename = './device_version_info.txt'
    device_info_fh = open(device_info_filename, 'w')
    print 'Device version information written to ' + device_info_filename
    print 'Device version information:'
    for device_version in device_version_dict.keys():
        for device_ip in device_version_dict[device_version]:
            device_info_fh.write(device_ip + ',' + device_version + '\n')
            print device_ip + ',' + device_version
    device_info_fh.close()


def main():
    device_version_dict = {}
    device_list = get_device_list()
    (device_username, device_password) = get_user_info()
    (device_prompt, telnet_timeout) = get_telnet_session_info()

    for device_ip in device_list:
        telnet_session = establish_telnet_session(device_ip, device_username, 
                device_password, device_prompt, telnet_timeout)
        device_version = get_version_info(telnet_session, device_prompt)
        try:
            device_version_dict[device_version].append(device_ip)
        except:
            device_version_dict[device_version] = [device_ip]
        close_telnet_session(telnet_session)

    write_device_information(device_version_dict)


if __name__ == '__main__':
    main ()
