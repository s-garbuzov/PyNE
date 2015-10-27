"""
utils.py: Helper utilities
"""

import os
import yaml
import inspect


def cfg_load(f):
    try:
        with open(f, 'r') as f:
            cfg = yaml.load(f)
        return cfg
    except IOError:
        print("Error: failed to read file '%s'" % f)
        return None


def dbg_print(msg=None):
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
