#!/usr/bin/python

# description:
# this script does the following:
#     reads a list of device connection information
#     creates a named tuple of the information
#     creates a list of the tuples
#     prints the information out using named tuple syntax


from collections import namedtuple


def get_device_list():
    device_list = []
    device_list_filename = 'device-tuple-info.txt'
    device_list_file_object = open(device_list_filename, 'r')
    device = namedtuple('device', ['name', 'ip_address',
                                   'username', 'password'])

    for line in device_list_file_object:
        record_info = line.split(',')
        device_record = device(name = record_info[0], 
                               ip_address = record_info[1], 
                               username = record_info[2], 
                               password = record_info[3])
        device_list.append(device_record)

    device_list_file_object.close()
    return device_list


def print_device_info(device_list):
    for device_record in device_list:
        print device_record.name + ': ' + device_record.ip_address
        print '\tusername: ' + device_record.username
        print '\tpassword: ' + device_record.password


def main():
    device_list = get_device_list()
    print_device_info(device_list)


if __name__ == '__main__':
    main ()
