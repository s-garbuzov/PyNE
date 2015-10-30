
from cisco_ios import CiscoIOS
from cisco_eos import CiscoEOS
from cisco_xr import CiscoXR
from brocade_vrouter import BrocadeVRouter

CLASS_MAP = {
    'cisco_ios': CiscoIOS,
    'cisco_eos': CiscoEOS,
    'cisco_xr': CiscoXR,
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
