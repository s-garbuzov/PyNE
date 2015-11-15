#!/usr/bin/python

# description:
# this script does the following:
#     reads a list of device IP addresses contained in a file
#     adds the IP addresses to a list
#     prints each member of the list to standard out


def get_device_list():
    device_list = []
    device_list_filename = 'device-ip-list.txt'
    device_list_file_object = open(device_list_filename, 'r')

    for ip_address in device_list_file_object:
        ip_address = ip_address.rstrip()
        device_list.append(ip_address)

    device_list_file_object.close()

    return device_list


def print_device_list(device_list):
    for ip_address in device_list:
        print ip_address


def main():
    device_list = get_device_list()
    print_device_list(device_list)


if __name__ == '__main__':
    main ()
