#!/usr/bin/python
# description: this script demonstrates reading a list of switches from a file


# import regular expression module
import re


def get_switch_list():
    # instantiate a list to append switch names to
    switch_list = []
    # define regular expression to match on a switch name
    switch_name_format = \
            re.compile(r'^[a-z0-9]+\-[0-9]+\.switch\.cml-lab\.cisco\.com\n')

    switch_list_file_name = './switch-file.txt'
    switch_list_file_object = open(switch_list_file_name, 'r')

    # iterate through each line in the switch list file
    for line in switch_list_file_object:
        # if the line matches regex format, then name append to switch_list
        if switch_name_format.match(line):
            # remove white space on the right (including newlines)
            line = line.rstrip()
            switch_list.append(line)

    # close the file object
    switch_list_file_object.close()
    # return the contents of the switch_list variable to main()
    return switch_list


def show_switch_list(switch_list):
    # iterate over each list element in the switch_list variable
    # and print it out
    for switch_name in switch_list:
        print switch_name


def main():
    switch_list = get_switch_list()
    show_switch_list(switch_list)


if __name__ == '__main__':
    main ()
