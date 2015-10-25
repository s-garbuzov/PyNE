#!/usr/bin/python

# description: demonstrate using getpass to prevent viewing input

import getpass

username = raw_input('Enter username: ')
password = getpass.getpass(prompt='Enter password for ' + username + ': ')

print '\nThe password for', username, 'is', password
print '\nPrinting passwords is a bad idea, but is done here for demonstration purposes.'
