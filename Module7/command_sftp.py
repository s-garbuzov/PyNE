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

from sftp_session import SFTPSession


def transfer_progress(filename, transfered, total):
    """Callback function that accepts name of the file being
    transfered, the number of bytes transferred so far, the
    total bytes to be transferred and prints current transfer
    progress information.
    """
    if(transfered < total):
        print("Transfer of %r is at %d/%d bytes (%.2f%%)" %
              (filename, transfered, total, 100. * transfered / total))


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
    local_path = "/tmp/mylogs/%s" % file_name

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
