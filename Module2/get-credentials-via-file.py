#!/usr/bin/python

# description: getting credentials from a file

# open the credentials file in read-only mode
# note: if you use a file to store passwords, you will need to do the following in production
#     keep usernames/password credentials in a different directory than the script
#     use file permissions to restrict access to the information
#     run the script as a different user (or possibly sudo) that has access to the credentials
credential_file = open('./credentials.txt', 'r')

for line in credential_file:
	line_parts = line.split(':')
	if (line_parts[0] == 'username'):
		username = line_parts[1].rstrip()
	elif (line_parts[0] == 'password'):
		password = line_parts[1].rstrip()

print '\nThe password for', username, 'is', password
print '\nPrinting passwords is a bad idea, but is done here for demonstration purposes.\n'
