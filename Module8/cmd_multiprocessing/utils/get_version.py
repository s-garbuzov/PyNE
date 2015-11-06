#!/usr/bin/env python


import logging
import multiprocessing as mp

from datetime import datetime
from Module8.cmd_multiprocessing.common.utils import cfg_load

logging.basicConfig(level=logging.DEBUG, format='')
logger = logging.getLogger(__name__)


def get_version(device, msg_queue):
    """TBD"""

    pass
    """
    # Allocate object representing the device
    obj = device_class_factory(device)

    # Execute device specific method for
    # retrieving version information
    status, version = obj.get_version()

    # Prepare result information to be returned
    dev_info = {'ip_addr': obj.get_ipaddr(),
                'vendor': obj.get_vendor(),
                'os_type': obj.get_os_type(),
                'os_version': version}
    result = {'status': status, 'dev_info': dev_info}

    # Place the result on the queue for reading by the parent process
    msg_queue.put(result)
   """


def show_results(results):
    """TBD"""

    logger.info("\n")
    for r in results:
        dev_info = r['dev_info']
        logger.info(" Device %s\n" % dev_info['ip_addr'])
        if r['status'] is True:
            logger.info("   Manufacturer: %s" % dev_info['vendor'])
            logger.info("   OS Type     : %s" % dev_info['os_type'])
            logger.info("   OS Version  : %s" % dev_info['os_version'])
        else:
            logger.debug("   Failed to obtain information")
        logger.info("\n")


def main():

    f = "../device_list.yml"
    devices = cfg_load(f)
    if(devices is None):
        logger.error("Config file '%s' read error " % f)
        exit(1)

    logger.debug("\nStarted: %s" % (datetime.now()))

    # Create a queue for communication with child processes
    msg_queue = mp.Queue()

    # To execute command in parallel on multiple devices
    # create a separate (child) process for each device
    jobs = []
    for device in devices:
        p = mp.Process(target=get_version, args=(device, msg_queue))
        jobs.append(p)
        p.start()  # Start the process

    # Get sub-process results from the output queue
    results = []
    for p in jobs:
        results.append(msg_queue.get())

    # Wait until all processes have terminated (making sure all
    # child processes have been terminated, no zombies left)
    for p in jobs:
        p.join()

    show_results(results)

    logger.debug("\nEnded: %s" % (datetime.now()))

if __name__ == '__main__':
    main()
