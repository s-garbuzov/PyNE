#!/usr/bin/python

# description:
# this script does the following:
#     reads a list of switch IP addresses contained in a file
#     adds the IP addresses to a list
#     prints each member of the list to standard out


def get_switch_list():
    switch_list = []
    switch_list_filename = 'switch-list.txt'
    switch_list_file_object = open(switch_list_filename, 'r')

    for ip_address in switch_list_file_object:
        ip_address = ip_address.rstrip()
        switch_list.append(ip_address)

    switch_list_file_object.close()

    return switch_list


def print_switch_list(switch_list):
    for ip_address in switch_list:
        print ip_address


def main():
    switch_list = get_switch_list()
    print_switch_list(switch_list)


if __name__ == '__main__':
    main ()
