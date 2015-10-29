#!/usr/bin/env python

from cmd_multiprocessing.common.utils import cfg_load


def check_status():
    pass
    """
    try:
        ssh.connect(ip, username=user, key_filename=key_file)
        return True
    except (BadHostKeyException, AuthenticationException, 
            SSHException, socket.error) as e:
        print e
        sleep(interval)
    """
    






def main():

    f = "../device_list.yml"
    devices = cfg_load(f)
    if(devices is None):
        print("Config file '%s' read error: " % f)
        exit()

    print "TBD"


if __name__ == '__main__':

    main()
