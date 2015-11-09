#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via TELNET connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Cisco IOS device.

command_telnet.py

"""

from Module7.cisco_ios import CiscoIOS


def main():
    # Remote device TELNET session specific info
    device = {
        'channel': 'telnet',
        'ip_addr': '10.30.30.3',
        'port': 23,
        'timeout': 3,
        'username': 'admin',
        'password': 'cisco',
        'login_prompt': 'sername:',
        'password_prompt': 'assword:',
        'oper_prompt': '>',
        'admin_prompt': '#',
        'secret': 'cisco',
        'verbose': True
    }

    cmd_string = "show interfaces\n"
    print("\nCommand to be executed: %s" % cmd_string)
    output = None

    obj = CiscoIOS(**device)  # Allocate object representing the device
    obj.connect()             # Connect to device
    if(obj.connected()):      # Check if connected
        obj.enable_privileged_commands()  # Turn on privileged commands
        obj.disable_paging()  # Disable paging

        # Execute command and get the result
        output = obj.execute_command(cmd_string)
        if(device['verbose']):
            print("CLI command '%r' has been executed" % cmd_string)

        obj.disconnect()      # Disconnect from device

    print("\n[%s]" % obj.to_str())
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
