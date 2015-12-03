"""
utils.py: Helper utilities
"""

import yaml


def cfg_load(f):
    try:
        with open(f, 'r') as f:
            cfg = yaml.load(f)
        return cfg
    except IOError:
        print("Error: failed to read file '%s'" % f)
        return None
