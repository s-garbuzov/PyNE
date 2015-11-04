
# built-in modules
import socket
import functools

# third-party modules
import paramiko


class SFTPSession(object):
    """SFTP session with a remote device."""

    def __init__(self, **kwargs):
        """Allocate and return a new instance object."""
        self._channel = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def open(self):
        try:
            # Create an instance object of the 'SSHClient' class
            rconn = paramiko.SSHClient()
            rconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rconn.connect(self.ip_addr, self.port,
                          self.username, self.password,
                          look_for_keys=False, allow_agent=False,
                          timeout=self.timeout)
            # Open an SFTP session on the SSH server
            self._sftp_client = rconn.open_sftp()
            self._channel = rconn
            return True
        except (paramiko.BadHostKeyException,
                paramiko.AuthenticationException,
                paramiko.SSHException,
                socket.error) as e:
            print "!!!Error: %s " % e
            return False

    def close(self):
        """Close the SFTP session and its underlying channel."""
        assert(self._channel is not None)
        assert(self._sftp_client is not None)
        try:
            self._sftp_client.close()
        except (Exception) as e:
            print "!!!Error: %s " % e

    def _transfer_progress(self, filename, transfered, total):
        """Callback function that accepts name of the file being
        transfered, the number of bytes transferred so far, the
        total bytes to be transferred and prints current transfer
        progress information.
        """
        if(transfered < total):
            print("Transfer of %r is at %d/%d bytes (%.2f%%)" %
                  (filename, transfered, total, 100. * transfered / total))

    def get(self, remote_path, local_path, verbose=False):
        """Copy a remote file (remote_path) from the SFTP server
        to the local host as local_path
        """
        assert(self._channel is not None)
        assert(self._sftp_client is not None)
        try:
            callback = None
            if(verbose):
                callback = functools.partial(self._transfer_progress,
                                             remote_path)
            self._sftp_client.get(remote_path, local_path, callback)
            return True
        except (Exception) as e:
            print "!!!Error: %s " % e
            return False
