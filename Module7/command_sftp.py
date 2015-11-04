#!/usr/bin/env python


"""

Example of a script that downloads a file from a remote device
to the local machine over SFTP session.

NOTES: Requires installation of the 'paramiko' Python package
          pip install paramiko
       The 'paramiko' package is documented at:
          http://docs.paramiko.org
       Complete set of SFTP client operations is available at:
         http://docs.paramiko.org/en/1.15/api/sftp.html

command_sftp.py

"""

# built-in modules
import os

from sftp_session import SFTPSession


def main():
    # Remote device SFTP session specific info
    device = {
        'ip_addr': '172.22.17.110',
        'port': 830,
        'timeout': 3,
        'username': 'vyatta',
        'password': 'vyatta',
        'secret': 'secret',
        'max_bytes': 9000,  # The maximum amount of data to be received at once
        'verbose': True
    }

    file_name = 'auth.log'
    remote_path = "/var/log/%s" % file_name
    local_path = "/tmp/mylogs1/%s" % file_name

    # Make sure that the local placeholder for the copy of the remote file
    # does already exist
    basedir = os.path.dirname(local_path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)              # create a directory for the file
    if not os.path.exists(local_path):
        with open(local_path, "w") as f:  # create a file in the directory
            f.close()

    # Establish SFTP session with the device
    sftp = SFTPSession(**device)
    if(sftp.open()):
        if(device['verbose']):
            print ("SFTP session to %s:%s started" %
                   (device['ip_addr'], device['port']))

        # Execute SFTP 'get' command and display execution result
        success = sftp.get(remote_path, local_path, device['verbose'])
        if success:
            print("Successfully loaded '%s' file to '%s'" %
                  (remote_path, local_path))
        else:
            print("!!!Error, failed to load '%s' file" % remote_path)

        sftp.close()
        if(device['verbose']):
            print ("SFTP session to %s:%s ended" %
                   (device['ip_addr'], device['port']))
    else:
        print("!!!Error, SFTP session to %s:%s has failed" %
              (device['ip_addr'], device['port']))


if __name__ == '__main__':
    main()
