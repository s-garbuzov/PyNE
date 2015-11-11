#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via TELNET connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Brocade vRouter device.

command_telnet.py

"""

from Module7.brocade_vrouter import BrocadeVRouter


def main():
    # Remote device TELNET session specific info
    device_info = {
        'channel': 'telnet',
        'ip_addr': '172.22.17.110',
        'port': 23,
        'timeout': 3,
        'username': 'vyatta',
        'password': 'vyatta',
        'login_prompt': 'login:',
        'password_prompt': 'assword:',
        'oper_prompt': '$',
        'admin_prompt': '#',
        'secret': 'secret',
        'verbose': True
    }

    cmd_string = "show interfaces\n"
    print("\nCommand to be executed: %s" % cmd_string)
    output = None

    # Allocate object representing the device
    device = BrocadeVRouter(**device_info)
    device.connect()                   # Connect to device
    if(device.connected()):            # Check if connected
        device.disable_paging()        # Disable paging
        device.enter_cfg_mode()        # Enter configuration mode

        # Execute command and get the result
        output = device.execute_command(cmd_string)
        if(device_info['verbose']):
            print("CLI command %r has been executed" % cmd_string)

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
