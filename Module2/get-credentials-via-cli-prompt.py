#!/usr/bin/python

# description: demonstrate using getpass to prevent viewing input


import getpass


def get_credentials():
    username = raw_input('Enter username: ')
    password = getpass.getpass(prompt='Enter password for ' + username + ': ')
    return (username, password)


def main():
    (username, password) = get_credentials()
    # print credentials to verify information
    # note: never do this in a production script
    print '\nThe password for', username, 'is', password


if __name__ == '__main__':
    main ()
