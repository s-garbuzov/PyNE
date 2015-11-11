#!/usr/bin/env python

from Module8.sample_project.common.utils import cfg_load


def check_status():
    pass


def main():

    f = "../device_list.yml"
    devices = cfg_load(f)
    if(devices is None):
        print("Config file '%s' read error: " % f)
        exit()

    print "TBD"


if __name__ == '__main__':

    main()
