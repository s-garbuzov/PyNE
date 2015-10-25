#!/usr/bin/python

# import the regular expression module
import re

# define empty list to stuff switch names into
# it is not strictly necessary to do this, but declaring variables at the beginning of a script is helpful
#     as it gives you a quick reference point when the list of global variables is long
switch_list = []

# regular expression describing switch naming convention used to determine if a line in the file represents a switch name
# note: the "^" is implied, so not strictly necessary
#     and the \n ensures that the switch name is followed by a newline, and thus on a line by itself
switch_name_format = re.compile (r'^[a-z0-9]+\-[0-9]+\.switch\.virl-lab\.cisco\.com\n')

# create file object pointing to the file containing our list of switches and set to read only
switch_file_object = open('./switch-file.txt', 'r')

# iterate through each line read into the file object
for line in switch_file_object:
	
	#check to see if the current line of input matches the regular expression defined in switch_name_format	
	if switch_name_format.match(line):

		# rstrip() removes all white space at the end of a line, including carriage returns
		line = line.rstrip()

		# add the current line, which has matched the switch name regular expression, to the list of switches in switch_list
		switch_list.append(line)

# close the file object
switch_file_object.close()

# print the list of switches that were added to the switch_list variable to verify the script worked
for switch_name in switch_list:
	print switch_name
