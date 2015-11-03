#!/usr/bin/python

# description: getting credentials from a file

# open the credentials file in read-only mode
# note: if you use a file to store passwords,
# you will need to do the following in production
#    1. keep the credential file in a different directory than the script
#    2. use file permissions to restrict access to credentials
#    3. run the script as a user with privileges to the credential file


def read_credential_file():
    credential_file_name = './credentials.txt'
    credential_file_object = open(credential_file_name, 'r')
    
    # "parse" the credential file to find credentials
    # iterate over each line in the credential file
    for line in credential_file_object:
        # split the contents of the line into components
        # create individual components separated by colons
        line_components = line.split(':')
        if (line_components[0] == 'username'):
            username = line_components[1].rstrip()
        elif (line_components[0] == 'password'):
            password = line_components[1].rstrip()
    
    return (username, password)


def main():
    (username, password) = read_credential_file()
    print '\nThe password for', username, 'is', password


if __name__ == '__main__':
    main ()
