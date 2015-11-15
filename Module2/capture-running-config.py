#!/usr/bin/python

# description:
# this script does the following:
#     logs into a single device
#     captures the output of the running config
#     writes the output of the running config to a file


import getpass
import pexpect
import sys


def get_user_credentials():
    device_username = raw_input('Enter username: ')
    # getpass allows getting the username without echoing characteers
    device_password = getpass.getpass(prompt='Enter password for ' + device_username + ': ')
    return (device_username, device_password)


def get_device_info():
    print 'Getting device information.'
    device_ip = '10.30.30.1'
    device_prompt = '[>#]'
    return (device_ip, device_prompt)


def establish_telnet_session(device_ip, device_prompt,
        device_username, device_password):
    print 'Establishing telnet session to device.'
    # set timeout for pexpect (i.e., how long to wait for match conditions)
    pexpect_timeout = 10
    # set the enable password to the same value as password for lab exercise
    device_enable_password = device_password

    # establish a telnet session to the device using pexpect
    # by "matching" on a possible timeout, you can trap for a timeout condition
    telnet_cmd = 'telnet ' + device_ip
    telnet_session = pexpect.spawn(telnet_cmd, timeout=pexpect_timeout)
    result = telnet_session.expect(['Username:', pexpect.EOF, pexpect.TIMEOUT])

    # if you are presented with a username prompt, do this
    if result==0:
        telnet_session.sendline(device_username)
        telnet_session.expect('Password:')
        telnet_session.sendline(device_password)
        telnet_session.expect(device_prompt)
        telnet_session.sendline('enable')
        telnet_session.expect('Password:')
        telnet_session.sendline(device_enable_password)
        telnet_session.expect(device_prompt)
        return telnet_session

    # an EOF will indicate the telnet executable exited
    elif result==1:
        sys.exit('Telnet exited unexpectedly while trying to connect to ' + device_ip)

    # pexpect timed out waiting for another match condition
    elif result==2:
        sys.exit('Pexpect timed out waiting for a username prompt for ' + device_ip)


def setup_session(telnet_session, device_prompt):
    print 'Preforming telnet session setup.'
    telnet_session.sendline('terminal length 0')
    telnet_session.expect(device_prompt)


def show_config(telnet_session, device_prompt):
    print 'Capturing the output of "show running-config".'
    telnet_session.sendline('show running-config')
    telnet_session.expect(device_prompt)
    show_run_output = telnet_session.before
    return show_run_output


def write_config(config_filename, config):
    print 'Writing the output of "show running-config" to a file.'
    config_file = open(config_filename, 'w')
    print >> config_file, config
    config_file.close()


def telnet_logout(telnet_session):
    telnet_session.sendline('exit')
    telnet_session.kill(0)


def main():
    # set the name of the config file to write output to
    config_filename = 'config_output.txt'

    # get credentials for logging into device
    (device_username, device_password) = get_user_credentials()
    # get device information: ip address, port, and prompt
    (device_ip, device_prompt) = get_device_info()
    # establish a telnet session
    telnet_session = establish_telnet_session(device_ip, device_prompt,
            device_username, device_password)
    # setup any desired session parameters (minimally, term len 0)
    setup_session(telnet_session, device_prompt)
    # get the running config of the device
    config = show_config(telnet_session, device_prompt)
    # write the running config out to a file
    write_config(config_filename, config)
    # logout of the device
    telnet_logout(telnet_session)


if __name__ == '__main__':
    main ()
