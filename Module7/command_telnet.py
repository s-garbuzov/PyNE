#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via TELNET connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Cisco IOS device.

command_telnet.py

"""

from cisco_ios import CiscoIOS


def main():
    # Remote device TELNET session specific info
    device = {
        'ip_addr': '172.22.17.111',
        'port': 23,
        'channel': 'telnet',
        'timeout': 3,
        'username': 'testuser',
        'password': 'testpassword',
        'login_prompt': 'sername:',
        'password_prompt': 'assword:',
        'oper_prompt': '$',
        'admin_prompt': '#',
        'secret': 'secret',
        'verbose': True
    }

    cmd_string = "show interfaces\n"
    print("\nCommand to be executed: %s" % cmd_string)

    # Allocate object representing the device
    obj = CiscoIOS(**device)

    # Connect to device
    obj.connect()
    if(obj.connected()):
        if(device['verbose']):
            print("TELNET connection to %s:%s has been established" %
                  (device['ip_addr'], device['port']))

        # Disable paging
        obj.disable_paging()

        # Enter configuration mode
        # obj.enter_cfg_mode()

        # Execute command and get the result
        output = obj.execute_command(cmd_string)
        if((device['verbose'])):
            print("CLI command %r has been executed" % cmd_string)

        # Disconnect from device (close management session)
        obj.disconnect()
        if(device['verbose']):
            print("TELNET connection to %s:%s has been closed" %
                  (device['ip_addr'], device['port']))

        # Display the command execution result
        print("\nCommand execution result:\n")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print output
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("\n")
    else:
        print("!!!Error, failed to connect to device %s:%s" %
              (device['ip_addr'], device['port']))


if __name__ == '__main__':
    main()
