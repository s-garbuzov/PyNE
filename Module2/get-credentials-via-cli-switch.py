#!/usr/bin/python

# description: demonstrate using cli switches to grab input
# printing help works by typing running the script with -h
#     python get-info-via-cli-switch.py -h
#
# usage:
# python get-info-via-cli-switch.py -u [username] -p [password]

import argparse

cli_switches = argparse.ArgumentParser(description='This script demonstrates using command line switches.')
cli_switches.add_argument('-u',default='admin', dest='user', help='Specify the username.')
cli_switches.add_argument('-p',default='cisco', dest='pw', help='Specify the password.')
returned_cli_switches = cli_switches.parse_args()

username = returned_cli_switches.user
password = returned_cli_switches.pw

print '\nThe password for', username, 'is', password
print '\nPrinting passwords is a bad idea, but is done here for demonstration purposes.'
