#!/usr/bin/python

# description:
# this script does the following:
#     reads a list of switch IP addresses contained in a file
#     adds the IP addresses to a list
#     prints each member of the list to standard out

# instantiate switch list variable
switch_list = []
# define the name of the file that contains switch list information
switch_list_filename = 'switch-list.txt'

# open switch list source file as read-only
switch_info = open(switch_list_filename, 'r')

# append each IP address in the switch list file to the switch_list list variable
for ip_address in switch_info:
	ip_address = ip_address.rstrip()
	switch_list.append(ip_address)

# close the file with the switch IP address information
switch_info.close()

# print out the values in the switch_list list to verify you successfully read them
for ip_address in switch_list:
	print ip_address

