#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via SSH connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Cisco IOS device.

command_ssh.py

"""

from Module7.cisco_ios import CiscoIOS


def main():
    # Remote device SSH session specific info
    device_info = {
        'channel': 'ssh',
        'ip_addr': '10.30.30.3',
        'port': 22,
        'timeout': 3,
        'username': 'admin',
        'password': 'cisco',
        'login_prompt': 'sername:',
        'password_prompt': 'assword:',
        'oper_prompt': '>',
        'admin_prompt': '#',
        'secret': 'secret',
        'max_bytes': 9000,  # The maximum amount of data to be received at once
        'verbose': True
    }

    cmd_string = "show interfaces | include line protocol\n"
    print("\nCommand to be executed: %s" % cmd_string)
    output = None

    device = CiscoIOS(**device_info)  # Allocate object representing the device
    device.connect()                   # Connect to device
    if(device.connected()):            # Check if connected
        device.enable_privileged_commands()  # Turn on privileged commands
        device.disable_paging()        # Disable paging

        # Execute command and get the result
        output = device.execute_command(cmd_string)
        if(device_info['verbose']):
            print("CLI command '%r' has been executed" % cmd_string)

        device.disconnect()            # Disconnect from device

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
