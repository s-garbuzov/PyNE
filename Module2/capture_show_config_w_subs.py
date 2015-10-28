#!/usr/bin/python

# description:
# this script does the following:
#     logs into a single switch
#     captures the output of the running config
#     writes the output of the running config to a file


import getpass, pexpect, sys


def get_user_credentials():
	# get user input
	user = raw_input('Enter username: ')
	pwd = getpass.getpass(prompt='Enter password for ' + user + ': ')
	return (user, pwd)


def establish_telnet_session(switch, switch_prompt, user, pwd):
	pexpect_timeout = 30 # set timeout for pexpect (i.e., how long to wait for match conditions)
	enable_pwd = pwd # set the enable password to the same value as password for this lab exercise

	# telnet to switch, get config, and write config to file
	telnet_cmd = 'telnet ' + switch
	telnet_session = pexpect.spawn(telnet_cmd, timeout=pexpect_timeout)
	result = telnet_session.expect(['Username:', pexpect.EOF, pexpect.TIMEOUT])

	# proceed given the condition you are presented with a username prompt
	if result==0:
		telnet_session.sendline(user)
		telnet_session.expect('Password:')
		telnet_session.sendline(pwd)
		telnet_session.expect('>')
		telnet_session.sendline('enable')
		telnet_session.expect('Password:')
		telnet_session.sendline(enable_pwd)
		telnet_session.expect(prompt)
		return telnet_session

	# an EOF will indicate the telnet executable exited
	elif result==1:
		sys.exit('Telnet exited unexpectedly while trying to connect to', switch) 

	# pexpect timed out waiting for a match condition
	elif result==2:
		sys.exit('Pexpect timed out waiting for a username prompt for', switch) 


def setup_session(telnet_session, switch_prompt):
	telnet_session.sendline('terminal length 0')
	telnet_session.expect(prompt)


def show_config (switch):
	telnet_session.sendline('show running-config')
	telnet_session.expect(prompt)
	show_run_output = telnet_session.before
	return show_run_output


def write_config (config_filename, config):
	config_file = open(config_filename, 'w')
	print >> config_file, config
	config_output.close()


def main():
	# declare variables
	switch = '10.3.21.5'
	switch_prompt = '#'
	config_filename = 'config_output.txt'

	(user, pwd) = get_user_credentials()
	telnet_session = establish_telnet_session(switch, switch_prompt, user, pwd)
	setup_session(telnet_session, switch_prompt)
	config = show_config(switch)
	write_config(config_filename, config)
	telnet_session.kill(0)


if __name__ == '__main__':
	main ()
