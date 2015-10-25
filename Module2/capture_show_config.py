#!/usr/bin/python

# description:
# this script does the following:
#     logs into a single switch
#     copies the config to a file
#     captures the output of the running config
#     writes the output of the running config to a file


import getpass, pexpect

# assign variables
switch = '10.3.21.5'
user = raw_input('Enter username: ')
pwd = getpass.getpass(prompt='Enter password for ' + user + ': ')
enable_pwd = pwd # set the enable password to the same value as password for the lab exercis
prompt = '#'
pexpect_timeout = 30 # set timeout for pexpect (i.e., how long to wait for match conditions)
switch_config = [] # create global list to hold config

# open file to write configuration to
config_output_filename = 'config_output.txt'
config_output = open(config_output_filename, 'w')


# telnet to switch using pexpect
telnet_cmd = 'telnet ' + switch
telnet_session = pexpect.spawn(telnet_cmd, timeout=pexpect_timeout)
result = telnet_session.expect(['Username:', pexpect.EOF, pexpect.TIMEOUT])

# proceed given the condition you are immediately presented with a user prompt
elif result==0:
	telnet_session.sendline(user)
	telnet_session.expect('Password:')
	telnet_session.sendline(pwd)
	telnet_session.expect('>')
	telnet_session.sendline('enable')
	telnet_session.expect('Password:')
	telnet_session.sendline(enable_pwd)
	telnet_session.expect(prompt)
	telnet_session.sendline('terminal length 0')
	telnet_session.expect(prompt)
	telnet_session.sendline('show running-config')
	telnet_session.expect(prompt)
	show_run_output = telnet_session.before

	# set the switch_config list to contain the output of "show run", by converting into list elements by newlines in the raw show_run_output info
	switch_config = show_run_output.splitlines()

	for line in switch_config:
		print >> config_output, line

	telnet_session.kill(0)

# an EOF will indicate the telnet executable exited
elif result==1:
	print 'Telnet exited unexpectedly while trying to connect to', switch

# pexpect timed out waiting for a match condition
elif result==2:
	print 'Pexpect timed out waiting for a match condition while connecting to', switch

# close the config file
config_output.close()
