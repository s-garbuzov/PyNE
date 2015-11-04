#!/usr/bin/env python

"""

Example of a script that executes a CLI command on a remote
device via SSH connection.

Administrator login options and CLI commands are device specific,
thus this script needs to be adapted to a concrete device specifics.
Current script assumes interaction with Brocade vRouter device.

command_ssh.py

"""

from brocade_vrouter import BrocadeVRouter


def main():
    # Remote device SSH session specific info
    device = {
        'channel': 'ssh',
        'ip_addr': '172.22.17.110',
        'port': 830,
        'timeout': 3,
        'username': 'vyatta',
        'password': 'vyatta',
        'oper_prompt': '$',
        'config_prompt': '#',
        'secret': 'secret',
        'max_bytes': 1000,  # The maximum amount of data to be received at once
        'verbose': True
    }

    cmd_string = "show interfaces\n"
    print("\nCommand to be executed: %s" % cmd_string)

    obj = BrocadeVRouter(**device)  # Allocate object representing the device
    obj.connect()                   # Connect to device
    if(obj.connected()):            # Check if connected
        obj.disable_paging()        # Disable paging
        obj.enter_cfg_mode()        # Enter configuration mode

        # Execute command and get the result
        output = obj.execute_command(cmd_string)
        if(device['verbose']):
            print("CLI command '%r' has been executed" % cmd_string)

        obj.disconnect()            # Disconnect from device

    if(output is not None):
        print("\nCommand execution result:\n")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print output
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("\n")
    else:
        print("Failed to execute command")


if __name__ == '__main__':
    main()
