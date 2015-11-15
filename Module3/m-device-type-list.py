#!/usr/bin/python

# description:
# this script does the following:
#     reads a list of device IP types correlated with IP addresses
#     creates a list of device types
#     creates a list of device IP addresses based on device types
#     this is done in a list of lists
#     prints out the list of IP addresses by device type


def get_device_list():
    device_type_list = []

    # intialize device_type_list[0] to hold a list of nx-os devices
    device_type_list.append([])
    # intialize device_type_list[0] to hold a list of ios devices
    device_type_list.append([])
    # intialize device_type_list[0] to hold a list of ios-xr devices
    device_type_list.append([])

    device_type_list[0] = ['10.0.1.1', '10.0.2.1', '10.0.3.1']
    device_type_list[1] = ['10.1.1.1', '10.1.2.1', '10.1.3.1']
    device_type_list[2] = ['10.2.1.1', '10.2.2.1', '10.2.3.1']

    return device_type_list


def print_device_list(device_type_list):
    print
    print 'nx-os devices:'
    print device_type_list[0][0]
    print device_type_list[0][1]
    print device_type_list[0][2]
    print
    print 'ios devices:'
    print device_type_list[1][0]
    print device_type_list[1][1]
    print device_type_list[1][2]
    print
    print 'ios-xr:'
    print device_type_list[2][0]
    print device_type_list[2][1]
    print device_type_list[2][2]
    print


def main():
    device_type_list = get_device_list()
    print_device_list(device_type_list)


if __name__ == '__main__':
    main ()
