from cisco_ios import CiscoIOS
from cisco_eos import CiscoEOS
from cisco_xr import CiscoXR

#  Mapping of supported devices
CLASS_MAP = {
    'cisco_ios': CiscoIOS,
    'cisco_eos': CiscoEOS,
    'cisco_xr': CiscoXR
}


def device_class_factory(device):
    """ TBD"""
    try:
        dev_type = device['device_type']
        aclass = CLASS_MAP[dev_type](**device)
        return aclass
    except(Exception) as e:
        print "!!!Error: %s\n" % e
        return None
