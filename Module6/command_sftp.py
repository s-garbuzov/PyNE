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
import socket
import functools

# third-party modules
import paramiko


def connect_ssh(device_info):
    """
    Establish SSH connection to a remote device.
    :param dict device_info: dictionary containing information
        about target device.
    :return: an instance of paramiko.SSHClient class connected
        to the device on success, None on failure.
    """

    try:
        # Create an instance object of the 'SSHClient' class
        ssh_client = paramiko.SSHClient()

        # Allow auto adding of unknown hosts to the known hosts in local
        # SSH configuration (make sure it is okay with your security
        # policy requirements)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if(device_info['verbose']):
            print("Connecting to %s:%s" %
                  (device_info['ip_addr'], device_info['port']))

        # o 'look_for_keys' is set to False to disable searching
        #   for discoverable private key files in '~/.ssh/'
        # o 'allow_agent' is set to False to disable connecting
        #   to the SSH agent on the local machine for obtaining
        #   the private key
        ssh_client.connect(hostname=device_info['ip_addr'],
                           port=device_info['port'],
                           username=device_info['username'],
                           password=device_info['password'],
                           look_for_keys=False, allow_agent=False,
                           timeout=device_info['timeout'])
        if(device_info['verbose']):
            print("Connection to %s:%s has been established" %
                  (device_info['ip_addr'], device_info['port']))
        return ssh_client
    except (paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException,
            socket.error) as e:
        print "!!!Error: %s " % e
        return None


def disconnect_ssh(device_info, ssh_conn):
    """
    Close active SSH connection to a remote device.
    :param dict device_info: dictionary containing information
        about target device.
    :param paramiko.SSHClient ssh_conn: object instance connected
        to a remote SSH server.
    :return: None
    """

    try:
        ssh_conn.close()
        if(device_info['verbose']):
            print("SSH connection to %s:%s has been closed" %
                  (device_info['ip_addr'], device_info['port']))
    except (Exception) as e:
        print "!!!Error, %s " % e


def transfer_progress(filename, transfered, total):
    """Callback function that accepts name of the file being
    transfered, the number of bytes transferred so far, the
    total bytes to be transferred and prints current transfer
    progress information.
    """
    if(transfered < total):
        print("Transfer of %r is at %d/%d bytes (%.2f%%)" %
              (filename, transfered, total, 100. * transfered / total))


def get_file(device_info, remote_path, local_path):
    """Copy a remote file ('remote_path') from SFTP server running
    on the 'device' to the 'local_path' on this machine."""

    success = False

    # Make sure that the local placeholder for the copy of the remote file
    # does already exist
    basedir = os.path.dirname(local_path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)              # create a directory for the file
    if not os.path.exists(local_path):
        with open(local_path, "w") as f:  # create a file in the directory
            f.close()

    # Connect to remote SSH server running on the device
    ssh_conn = connect_ssh(device_info)
    if ssh_conn is not None:
        sftp_session = None
        try:
            # Open an SFTP session on the SSH server
            sftp_session = ssh_conn.open_sftp()
            callback_func = None
            if(device_info['verbose']):
                print ("SFTP session started")
                callback_func = functools.partial(transfer_progress,
                                                  remote_path)
            sftp_session.get(remote_path, local_path, callback_func)
            if(device_info['verbose']):
                print("Transfer of %r has completed" % remote_path)
            success = True
        except (paramiko.SSHException, IOError) as e:
            success = False
            print "!!! Error: %s " % e
        finally:
            # Close SFTP session
            if(sftp_session is not None):
                sftp_session.close()
            # Disconnect from SSH Server
            disconnect_ssh(device_info, ssh_conn)
            if(device_info['verbose']):
                print ("SFTP session ended")

    return success


def main():
    # Remote device SFTP session specific info
    device_info = {
        'ip_addr': '10.0.0.1',
        'port': 22,
        'timeout': 3,
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'verbose': True
    }

    file_name = 'auth.log'
    remote_path = "/var/log/%s" % file_name
    local_path = "/tmp/mylogs/%s" % file_name
    success = get_file(device_info, remote_path, local_path)
    if success:
        print("Successfully loaded '%s' file to '%s'" %
              (remote_path, local_path))
    else:
        print("Failed to load '%s' file" % remote_path)

if __name__ == '__main__':
    main()
