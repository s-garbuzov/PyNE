#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via TELNET connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Cisco IOS-XR device.

command_telnet.py

"""

from Module7.cisco_iosxr import CiscoIOSXR


def main():
    # Remote device TELNET session specific info
    device_info = {
        'channel': 'telnet',
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

#    cmd_string = "show interfaces\n"
    cmd_string = "show ipv4 interface brief\n"
    print("\nCommand to be executed: %s" % cmd_string)
    output = None

    device = CiscoIOSXR(**device_info)  # Allocate object representing device
    device.connect()                    # Connect to device
    if(device.connected()):             # Check if connected
        device.enable_privileged_commands()  # Turn on privileged commands
        device.disable_paging()         # Disable paging

        # Execute command and get the result
        output = device.execute_command(cmd_string)
        if(device_info['verbose']):
            print("CLI command '%r' has been executed" % cmd_string)

        device.disconnect()             # Disconnect from device

    print("\n[%s]" % device.to_str())
    if(output is not None):
        print("Command execution result:\n")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print output
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("\n")
    else:
        print("Failed to execute command")


if __name__ == '__main__':
    main()
