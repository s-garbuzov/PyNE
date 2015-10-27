#!/usr/bin/env python

from cmd_multiprocessing.common.utils import cfg_load


def main():

    f = "../device_list.yml"
    devices = cfg_load(f)
    if(devices is None):
        print("Config file '%s' read error: " % f)
        exit()

    print "TBD"


if __name__ == '__main__':

    main()
