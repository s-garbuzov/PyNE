#!/usr/bin/python


from collections import namedtuple


def get_device_list():
    device_list = []
    Device = namedtuple('Device', ['name', 'ip_address',
                                   'username', 'password'])

    device1 = Device(name = 'device1', 
                           ip_address = '192.168.1.1', 
                           username = 'user1', 
                           password = 'password1')
    device_list.append(device1)
    
    device2 = Device(name = 'device2', 
                           ip_address = '192.168.2.1', 
                           username = 'user2', 
                           password = 'password2')
    device_list.append(device2)
    
    return device_list


def print_device_info(device_list):
    device1 = device_list[0]
    device2 = device_list[1]

    print
    print device1.name
    print device1.ip_address
    print device1.username
    print device1.password  
    print
    print device2.name
    print device2.ip_address
    print device2.username
    print device2.password
    print


def main():
    device_list = get_device_list()
    print_device_info(device_list)


if __name__ == '__main__':
    main ()
