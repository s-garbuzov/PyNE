#!/usr/bin/python


def get_device_list():
    device_list = []

    device_list.append('10.3.21.1')
    device_list.append('10.3.21.2')
    device_list.append('10.3.21.3')

    return device_list


def print_device_list(device_list):
    print
    print device_list[0]
    print device_list[1]
    print device_list[2]
    print

def main():
    device_list = get_device_list()
    print_device_list(device_list)


if __name__ == '__main__':
    main ()
