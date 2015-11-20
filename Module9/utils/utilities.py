"""
Helper utility functions
"""

# Python standard library modules
import os
import inspect

# third-party library modules
import yaml


def dbg_trace_print(msg=None):
    """Prints message and caller's frame stack information in the
    "module_name:line_number" format.
    """
    frame = inspect.currentframe()
    try:
        f = os.path.basename(frame.f_back.f_code.co_filename)
        l = frame.f_back.f_lineno
        if msg:
            s = '[%s:%d] %s' % (f, l, msg)
        else:
            s = '[%s:%d]' % (f, l)
    except(Exception):
        pass
    finally:
        if s:
            print s
        del frame


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
