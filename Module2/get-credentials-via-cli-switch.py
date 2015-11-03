#!/usr/bin/python

# description: demonstrate using cli switches to grab input
# printing help works by typing running the script with -h
#     python get-info-via-cli-switch.py -h
#
# usage:
# python get-info-via-cli-switch.py -u [username] -p [password]


import argparse


def get_cli_switch_values():
    cli_switches = argparse.ArgumentParser(description= \
            'This script demonstrates using command line switches.')
    cli_switches.add_argument('-u',default='admin', dest='username', \
            help='Specify the username.')
    cli_switches.add_argument('-p',default='cisco', dest='password', \
            help='Specify the password.')
    cli_switch_values = cli_switches.parse_args()
    return (cli_switch_values.username, cli_switch_values.password)


def main ():
    (username, password) = get_cli_switch_values()
    print '\nThe password for', username, 'is', password


if __name__ == '__main__':
    main ()
