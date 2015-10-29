#!/usr/bin/env python

"""

Example of a script that asynchronously executes a CLI command
on multiple remote devices via SSH connection.
NOTE: CLI commands are device specific, so this package
      needs to be adapted to concrete devices.

cli_command_ssh.py
"""

import multiprocessing as mp

from datetime import datetime
from cmd_multiprocessing.common.utils import cfg_load
from cmd_multiprocessing.devices.factory import device_class_factory


def execute_command(device, cli_command, read_delay, msg_queue):
    """
    Execute a CLI command on a remote device over established SSH channel.
    This function is asynchronously executed in a context of submitted process.
    :param dict device: dictionary containing information for establishing
        SSH session to a target device.
    :param str cli_command: CLI command to be executed.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: output of the command on success, error message otherwise.
    """

    # Allocate object representing the device
    obj = device_class_factory(device)
    # Request object to execute the command
    output = obj.exec_cmd_ssh(cli_command, read_delay)
    # Return the result
    msg_queue.put("[%s %s %s] %s" %
                  (obj.get_vendor(), obj.get_os_type(),
                   obj.get_ipaddr(), output))


def show_results(results):
    """Display results of command execution collected form all devices"""

    print("\n")
    print("Results:\n")
    for result in results:
        print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        print("%s" % result)
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print("\n")


def dispatch_command(cfg_file, cmd_string, read_delay=1):
    """
    Dispatch command execution on multiple devices, collect and return results.
    :param str cfg_file: path to the configuration file containing
        list of target devices.
    :param str cli_command: CLI command to be executed.
    :param int read_delay: time to wait for the CLI command to complete.
    :return: command execution results collected from all the devices
    """

    devices = cfg_load(cfg_file)
    if(devices is None):
        print("Config file '%s' read error " % cfg_load)
        exit(1)

    print("\nStarted: %s" % (datetime.now()))

    # Create a queue for communication with child processes
    msg_queue = mp.Queue()

    # To execute command in parallel on multiple devices
    # create a separate (child) process for each device
    jobs = []
    for device in devices:
        p = mp.Process(target=execute_command,
                       args=(device, cmd_string, read_delay, msg_queue))
        jobs.append(p)
        p.start()  # Start the process

    # Get sub-process results from the output queue
    results = []
    for p in jobs:
        results.append(msg_queue.get())

    # Wait until all processes have terminated (making sure all
    # child processes have been terminated, no zombies left)
    for p in jobs:
        p.join()

    print("\nEnded: %s" % (datetime.now()))
    return results


if __name__ == '__main__':
    cfg_file = "../device_list.yml"
    cmd_string = "show interfaces\n"
    results = dispatch_command(cfg_file, cmd_string, read_delay=1)
    show_results(results)
