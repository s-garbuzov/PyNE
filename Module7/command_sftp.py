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

from Module7.sftp_session import SFTPSession


def get_file(device_info, remote_path, local_path):
    """Copy a remote file ('remote_path') from SFTP server running
    on a target device to the 'local_path' on this machine."""

    # Make sure that the local placeholder for the copy of the remote file
    # does already exist
    basedir = os.path.dirname(local_path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)              # create a directory for the file
    if not os.path.exists(local_path):
        with open(local_path, "w") as f:  # create a file in the directory
            f.close()

    success = False
    # Establish SFTP session with the device and execute 'get' command
    sftp = SFTPSession(**device_info)
    if(sftp.open()):
        success = sftp.get(remote_path, local_path)
        sftp.close()  # Close SFTP session

    return success


def main():
    # Remote device SFTP session specific info
    device_info = {
        'ip_addr': '172.22.17.110',
        'port': 830,
        'timeout': 3,
        'username': 'vyatta',
        'password': 'vyatta',
        'verbose': True
    }

    file_name = 'auth.log'
    remote_path = "/var/log/%s" % file_name
    local_path = "/tmp/mylogs1/%s" % file_name
    success = get_file(device_info, remote_path, local_path)
    if success:
        print("Successfully loaded '%s' file to '%s'" %
              (remote_path, local_path))
    else:
        print("Failed to load '%s' file" % remote_path)


if __name__ == '__main__':
    main()
