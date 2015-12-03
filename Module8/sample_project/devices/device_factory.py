"""
Class DeviceFactory
"""


from Module8.sample_project.devices.cisco_iosxr import CiscoIOSXR
from Module8.sample_project.devices.brocade_vrouter import BrocadeVRouter

CLASS_MAP = {
    'cisco_iosxr': CiscoIOSXR,
    'brocade_vrouter': BrocadeVRouter
}


class DeviceFactory(object):
    """Creates an object instance based on a device type"""

    # Decorate 'create' function as a static method (a one that
    # does not require an implicit 'self' as a first argument)
    @staticmethod
    def create(device):
        try:
            dev_type = device['device_type']
            aclass = CLASS_MAP[dev_type](**device)
            return aclass
        except(Exception) as e:
            print "!!!Error: %s\n" % e
            assert(False)
            return None

    # Convert 'create' function to be a static method
    # (a one that does not require an implicit 'self'
    # as a first argument)
    # factory = staticmethod(factory)
