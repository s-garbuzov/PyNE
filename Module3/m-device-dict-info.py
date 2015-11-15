#!/usr/bin/python


from collections import namedtuple


def get_device_info():
    device_type_dict = {}
    device_connect = namedtuple('device_connect', ['ip_address', 'username',
                                                   'password'])

    
    device1 = device_connect (ip_address = '10.1.1.1', username = 'user1', 
                              password = 'password1')
    device2 = device_connect (ip_address = '10.2.2.2', username = 'user2', 
                              password = 'password2')
    device3 = device_connect (ip_address = '10.3.3.3', username = 'user3', 
                              password = 'password3')
    device4 = device_connect (ip_address = '10.4.4.4', username = 'user4', 
                              password = 'password4')
    device5 = device_connect (ip_address = '10.5.5.5', username = 'user5', 
                              password = 'password5')
    device6 = device_connect (ip_address = '10.6.6.6', username = 'user6', 
                              password = 'password6')

    device_type_dict['ios'] = [device1, device2]
    device_type_dict['nx-os'] = [device3, device4]
    device_type_dict['ios-xr'] = [device5, device6]

    return device_type_dict


def print_device_info(device_type_dict):
    device1 = device_type_dict['ios'][0]
    device2 = device_type_dict['ios'][1]
    device3 = device_type_dict['nx-os'][0]
    device4 = device_type_dict['nx-os'][1]
    device5 = device_type_dict['ios-xr'][0]
    device6 = device_type_dict['ios-xr'][1]

    print
    print 'ios devices:'
    print
    print 'device 1:'
    print device1.ip_address
    print device1.username
    print device1.password
    print
    print 'device 2:'
    print device2.ip_address
    print device2.username
    print device2.password
    print
    print '-----\nnx-os devices:'
    print
    print 'device 3:'
    print device3.ip_address
    print device3.username
    print device3.password
    print
    print 'device 4:'
    print device4.ip_address
    print device4.username
    print device4.password
    print
    print '-----\nios-xr devices:'
    print
    print 'device 5:'
    print device5.ip_address
    print device5.username
    print device5.password
    print
    print 'device 6:'
    print device6.ip_address
    print device6.username
    print device6.password
    print


def main():
    device_type_dict = get_device_info()
    print_device_info(device_type_dict)


if __name__ == '__main__':
    main ()
