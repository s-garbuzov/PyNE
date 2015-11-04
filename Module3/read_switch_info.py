#!/usr/bin/python

# description:
# this script does the following:
#    reads a list of switch information (switch name, IP, username, password)
#    add the switch name to a dictionary
#    assigns the dictionary index a tuple of (IP, username, password)
#    prints the information for each switch


def get_switch_info():
    switch_dict = {}
    switch_info_filename = 'switch-dict.txt'
    switch_info_file_object = open(switch_info_filename, 'r')

    for line in switch_info_file_object:
        line = line.rstrip()
        switch_info  = line.split(',')
    
        switch_name = switch_info[0]
        ip_address = switch_info[1]
        username = switch_info[2]
        password = switch_info[3]
    
        switch_connection_info = (ip_address, username, password)
        switch_dict[switch_name] = switch_connection_info

    switch_info_file_object.close()
    
    return switch_dict


def print_switch_info(switch_dict):
    for switch in switch_dict.keys():
        print switch + ':', switch_dict[switch]


def main():
    switch_dict = get_switch_info()
    print_switch_info(switch_dict)


if __name__ == '__main__':
    main ()
