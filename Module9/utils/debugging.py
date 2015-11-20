"""
troubleshooting/debugging utility functions
"""

# Python standard libraries
import os
import inspect


def dbg_trace_print(msg=None):
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
