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
    device_list = []
    device_list_filename = 'device-list-mutli-type.txt'
    device_list_file_object = open(device_list_filename, 'r')

    for line in device_list_file_object:
        (os_type, ip_address) = line.split(',')
        ip_address = ip_address.rstrip()
        
        try:
            device_list_index = device_type_list.index(os_type)
            device_list[device_list_index].append(ip_address)
        
        except:
            device_type_list.append(os_type)
            device_list.append([])
            device_list_index = device_type_list.index(os_type)
            device_list[device_list_index].append(ip_address)

    device_list_file_object.close()
    return (device_type_list, device_list)


def print_device_list(device_type_list, device_list):
    for device_type in device_type_list:
        print device_type + ' devices:'
        device_list_index = device_type_list.index(device_type)
        
        for ip_address in device_list[device_list_index]:
            print '\t' + ip_address    


def main():
    (device_type_list, device_list) = get_device_list()
    print_device_list(device_type_list, device_list)


if __name__ == '__main__':
    main ()
