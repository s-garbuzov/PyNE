

# third-party library modules
import yaml


def get_controller_cfg():
    path = "./ctrl.yml"
    data = yaml_cfg_load(path)
    return data


def get_netconf_cfg(self, path):
    path = "./netconf.yml"
    data = yaml_cfg_load(path)
    return data


def yaml_cfg_load(f):
    """Loads file containing YAML encoded configuration data
    and converts it to the corresponding Python object."""
    try:
        with open(f, 'r') as f:
            cfg = yaml.load(f)
        return cfg
    except IOError:
        print("Error: failed to read file '%s'" % f)
        return None
