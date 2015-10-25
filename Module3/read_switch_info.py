#!/usr/bin/python

# description:
# this script does the following:
#     reads a list of switch information (switch name, IP, username, password)
#     add the switch name to a dictionary
#     assigne the dictionary index a tuple of (IP, username, password)


# instantiate switch dictionary variable
switch_dict = {}
# define the name of the file that contains switch list information
switch_list_filename = 'switch-dict.txt'

# open switch info source file as read-only
switch_info = open(switch_list_filename, 'r')

# grab switch information from a file and store in a dictionary for later use
for line in switch_info:
	line = line.rstrip()
	switch_parts  = line.split(',')
	
	# assign meaningful names to the line split parts
	switch_name = switch_parts[0]
	ip_address = switch_parts[1]
	username = switch_parts[2]
	password = switch_parts[3]
	
	# assign switch connection info to a tuple
	# unlike lists, the "columns" in a tuple generally have meaning separate and distinct from each other
	# whereas a list is generally just that... a list of all the same types of information (like a list of IP addresses)
	switch_connection_info = (ip_address, username, password)

	# assign the switch name to the dictionary and assign it the value of the switch_connection_info tuple
	switch_dict[switch_name] = switch_connection_info

# close the file with the switch IP address information
switch_info.close()

# print out the values in the switch_dict variable to verify you successfully assigned them
for switch in switch_dict.keys():
	print switch + ':', switch_dict[switch]
