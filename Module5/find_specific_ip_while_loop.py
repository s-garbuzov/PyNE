#!/usr/bin/python

# description:


import re
import pexpect
from collections import namedtuple


def get_device_list():
    device_list = []
    device_list_filename = 'device-tuple-info.txt'
    device_list_file_object = open(device_list_filename, 'r')
    Device = namedtuple('Device', ['name', 'ip_address',
                                   'username', 'password'])
    for line in device_list_file_object:
        record_info = line.split(',')
        device_record = Device(name = record_info[0],
                               ip_address = record_info[1],
                               username = record_info[2],
                               password = record_info[3])
        device_list.append(device_record)
    device_list_file_object.close()
    return device_list


def get_telnet_session_info():
    device_prompt = '[>#]'
    telnet_timeout = 5
    return (device_prompt, telnet_timeout)


def establish_telnet_session(device_ip, device_username, device_password,
                             device_prompt, telnet_timeout):
    device_enable_password = device_password
    telnet_command = 'telnet ' + device_ip

    telnet_session = pexpect.spawn(telnet_command, timeout=telnet_timeout)
    result = telnet_session.expect(['Username:', pexpect.EOF, pexpect.TIMEOUT])

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
    elif result==1:
        print 'Telnet exited unexpectedly when connecting to ' + device_ip
    elif result==2:
        print 'Pexpect timed out waiting for a username prompt on ' + device_ip


def verify_ip_address(ip_candidate):
    ipv4_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
    if ipv4_pattern.match(ip_candidate):
        return True
    else:
        return False


def get_ip_interfaces(telnet_session, device_prompt):
    interface_ip_dict = {}
    telnet_session.sendline('show ip interface brief')
    telnet_session.expect(device_prompt)
    telnet_session.sendline('\n')
    telnet_session.expect(device_prompt)
    show_ip_output = telnet_session.before
    show_ip_output_lines = show_ip_output.splitlines()
    for line in show_ip_output_lines:
        interface_info = re.split('\s+', line)
        if len(interface_info) > 1:
            ip_candidate = interface_info[1]
            is_ip_address = verify_ip_address(ip_candidate)
            if is_ip_address == True:
                interface = interface_info[0]
                interface_ip_dict[interface] = ip_candidate
    return interface_ip_dict


def check_interface_ip_addresses(interface_ip_dict, target_ip):
    for interface in interface_ip_dict.keys():
        if (interface_ip_dict[interface] == target_ip):
            return (True, interface)
    return (False, None)


def close_telnet_session(telnet_session):
    telnet_session.sendline('quit')
    telnet_session.kill(0)


def main():
    target_ip = raw_input('Enter IP address to find: ')
    device_list = get_device_list()
    (device_prompt, telnet_timeout) = get_telnet_session_info()

    number_of_devices = len(device_list)
    record_number = 0
    while record_number < number_of_devices:
        device_record = device_list[record_number]
        device_ip = device_record.ip_address
        device_username = device_record.username
        device_password = device_record.password
        record_number += 1

        try:
            telnet_session = establish_telnet_session(device_ip,
                    device_username, device_password, device_prompt,
                    telnet_timeout)

            # you can avoid the reason for the try statement by testing
            # if (telnet_session != None):
            interface_ip_dict = get_ip_interfaces(telnet_session,
                    device_prompt)
            close_telnet_session(telnet_session)
            (ip_found, interface) = \
                    check_interface_ip_addresses(interface_ip_dict, target_ip)

            if ip_found == True:
                print 'IP address ' + target_ip + ' found on this interface.'
                print device_record.name + ' (' + device_ip + '): ' + \
                        interface + ', ' + interface_ip_dict[interface]
                break
        except:
            continue

    if ip_found != True:
        print 'IP address ' + target_ip + ' not found.'


if __name__ == '__main__':
    main ()