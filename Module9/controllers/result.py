from collections import namedtuple



def func():
    success = False
    data = "error message"

    return success, data



a, b = func()
print "%s, %s" % (a, b)


exit(0)
    


Result = namedtuple('Result', ['success', 'data'])

#r = Result(False, "error message")
r = Result()
print r.success
print r.data

r.success = True
r.data = "something"

print r.success
print r.data


'''
#import collections
from collections import namedtuple

class CtrlResponse(object):
    pass


class Result(object):
    def __init__(self, success=False, data=None):
        self.success = success
        self.data = data


class ReturnValue(object):
    def __init__(self, success=False, data=None):
        self.success = success
        self.data = data

Result = namedtuple('Result', ['success', 'data'])
print Result
r = Result(False, "error message")
print r.success
print r.data

"""
point = namedtuple('Point', ['x', 'y'])
p = point(1, y=2)
print "%s, %s" % (p.x, p.y)


   >>> Point = namedtuple('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
"""
'''
