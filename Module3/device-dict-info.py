#!/usr/bin/python

# description:
# this script does the following:
#    reads a list of device information (name, type, IP, username, password)
#    creates a device list in a dictionary indexed by type
#    creates an additional dictionary with device connection info 
#        (IP, username, password)
#    prints the information collected


from collections import namedtuple


def get_device_info():
    device_type_dict = {}
    devices = {}
    device_connect = namedtuple('device_connect', ['ip_address', 'username',
                                                   'password'])
    
    device_info_filename = 'device-dict-info.txt'
    device_info_file_object = open(device_info_filename, 'r')

    for line in device_info_file_object:
        line = line.rstrip()
        device_info  = line.split(',')
        
        device_name = device_info[0]
        device_type = device_info[1]
        device_connect_info = device_connect (ip_address = device_info[2],
                                              username = device_info[3], 
                                              password = device_info[4])

        if device_type in device_type_dict.keys():
            device_type_dict[device_type].append(device_name)
        else:
            device_type_dict[device_type] = []
            device_type_dict[device_type].append(device_name)

        devices[device_name] = device_connect_info

    device_info_file_object.close()
    return (device_type_dict, devices)


def print_device_info(device_type_dict, devices):
    for device_type in device_type_dict.keys():
        print '\n-----\n' + device_type + ' devices:\n'
        for device in device_type_dict[device_type]:
            print device
            device_connect_info = devices[device]
            print '\tipaddress: ' + device_connect_info.ip_address
            print '\tusername: ' + device_connect_info.username
            print '\tpassword: ' + device_connect_info.password


def main():
    (device_type_dict, devices) = get_device_info()
    print_device_info(device_type_dict, devices)


if __name__ == '__main__':
    main ()
