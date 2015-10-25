#!/usr/bin/python

# description: demonstrate pexpect shell interaction, EOF and TIMEOUT conditions

# note: play with the pexpect_timeout and num_pings values to generate EOF and TIMEOUT conditions
#     the TIMEOUT condition is measured in seconds, and the ping command sends a ping once per second
#     if you set pexpect_timeout = 5 and num_pings = '10', then no match condition will occur prior to the timeout value

import pexpect

pexpect_timeout = 10
ping_target = '192.168.1.1'
num_pings = '5'

ping_cmd = 'ping -c ' + num_pings + ' ' + ping_target

ping = pexpect.spawn(ping_cmd, timeout=pexpect_timeout)

# note that multiple match conditions can be specified  in the expect method
cmd_result = ping.expect([pexpect.EOF, pexpect.TIMEOUT])

# if an EOF is reached, do the following
# note: an EOF condition indicates the command invoked by pexpect has exited
if cmd_result==0:		
	# print the output of the ping command that occurred before match condition
	# in this case, the match condition is the completion of the ping command (it exits and causes and end-of-file condition)
	ping_cmd_output = ping.before
	print ping_cmd_output

# if a pexpect match condition is not made within the timeout interval, then a timeout occurs
# it is useful to match on this condition to continue script execution when in a loop, especially with SSH sessions that may be hung
if cmd_result==1:
	print 'Pexpect did not find a match condition in the alloted time.'
