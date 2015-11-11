#!/usr/bin/env python

"""

Example of a script that synchronously executes a CLI command
on multiple remote devices, going one by one through the device list.
CLI commands are device specific, so this package needs to be adapted
to concrete devices.
Current script assumes interaction with Cisco IOS devices.

NOTES: This package requires installation of the 'paramiko' Python package
          pip install paramiko
       The 'paramiko' package is documented at:
          http://docs.paramiko.org

async_command.py

"""

# This package local modules
from Module8.sample_project.common.utils import cfg_load
from Module8.sample_project.devices.device_factory import DeviceFactory


def execute_command(device_info, cmd_string, read_delay):
    """
    Execute a CLI command on a remote device over established
    management channel.
    :param dict device_info: dictionary containing information
        about target device.
    :param str cmd_string: CLI command to be executed.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: output of the command on success, error message otherwise.
    """

    output = None

    # Allocate object representing the device
    device = DeviceFactory.create(device_info)
    device.connect()                   # Connect to device
    if(device.connected()):            # Check if connected
        device.enable_privileged_commands()  # Turn on privileged commands
        device.disable_paging()        # Disable paging

        # Execute command and get the result
        output = device.execute_command(cmd_string)
        if((device_info['verbose'])):
            print("[%s] CLI command %r has been executed" %
                  (device.to_str(), cmd_string))

        device.disconnect()            # Disconnect from device
    else:
        output = "Failed to connect"

    # Return the result
    return ("[%s] %s" % (device.to_str(), output))


def show_results(results):
    """Display results of a command execution collected from all devices"""

    for result in results:
        print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        print("%s" % result)
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print "\n"


def dispatch_command(cfg_file, cmd_string, read_delay=1):
    """
    Execute command on multiple devices, going one by one,
    collect and returns results.
    :param str cfg_file: path to the configuration file containing
        list of target devices.
    :param str cmd_string: CLI command to be executed.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: command execution results collected from all the devices
    """

    devices_info = cfg_load(cfg_file)
    if(devices_info is None):
        print("Config file '%s' read error " % cfg_load)
        exit(1)

    results = []
    for item in devices_info:
        output = execute_command(item, cmd_string, read_delay)
        results.append(output)

    return results


if __name__ == '__main__':
    cfg_file = "../device_list.yml"
    cmd_string = "show interfaces | include line protocol\n"
    print("\nCommand to be executed: %s" % cmd_string)
    results = dispatch_command(cfg_file, cmd_string, read_delay=1)
    print("\nCommand execution results:\n")
    show_results(results)
    print("\n")
