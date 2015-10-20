#!/usr/bin/env python

# Examples of user-defined functions and making calls for them.


def device_info_params(vendor, os, fw, ip, name='testname', pswd='testpswd'):
    """Example of function that handles a fixed mandatory arguments list.
    Two last function arguments are allowed to have default values,
    if function called without these arguments they get assigned
    with default value.
    """
    print "manufacturer=%s" % vendor
    print "os_type=%s" % os
    print "fw_version=%s" % fw
    print "ip_addr=%s" % ip
    print "admin_name=%s" % name
    print "admin_password=%s" % pswd


def device_info_args(*args):
    """Example of function that handles variable list of positional parameters
    passed with *args argument, which is treated as a tuple containing
    list of parameter values.
    Usage of *args as the argument name is just a convention, e.g it
    can be named as *var
    """
    if args is not None:
        i = 0
        for arg in args:
            print "arg[%s]=%s" % (i, arg)
            i += 1


def device_info_keywords(**kwargs):
    """Example of function that handles variable list of named (keyworded)
    parameters passed with **kwargs argument, which is treated as a
    dictionary containing key-value pairs.
    Usage of **kwargs as the argument name is just a convention, e.g. it
    can be named as **vars
    """
    if kwargs is not None:
        for k, v in kwargs.items():
            print "key=%s, val=%s" % (k, v)


def device_info_params_args_keywords(ip, *args, **kwargs):
    """ Example of function that handles one explicit mandatory argument,
    variable list of positional arguments and variable list of named
    (keyworded) arguments"""

    print "ip_addr=%s" % ip
    if args is not None:
        i = 0
        for arg in args:
            print "arg[%s]=%s" % (i, arg)
            i += 1
    if kwargs is not None:
        for k, v in kwargs.items():
            print "key=%s, val=%s" % (k, v)


print ("'dev_info_params' function call "
       "(arguments passed as a list of positional parameters)")
device_info_params('cisco', 'ios', '2.1.1', '192.0.2.168')
print "\n"


print ("'dev_info_params' function call "
       "(arguments passed as a list of named parameters)")
device_info_params(ip='192.0.2.168', vendor='cisco', os='ios', fw='2.1.1')
print "\n"


print ("'dev_info_args' function call "
       "(arguments passed via tuple with the list of positional parameters)")
device_tuple = (
    'cisco',
    'ios',
    '2.1.1',
    '192.0.2.168',
    'testname',
    'testpswd'
)
device_info_args(*device_tuple)
print "\n"


# Script that demonstrates how to make calls for the function examples
# defined in this module

print ("'dev_info_args' function call "
       "(arguments passed as a list of positional parameters)")
device_info_args('cisco', 'ios', '2.1.1', '192.0.2.168',
                 'testname', 'testpswd')
print "\n"


print ("'dev_info_keywords' function call "
       "(arguments passed via dictionary with the keyworded parameters)")
device_dict = {
    'manufacturer': 'cisco',
    'os_type': 'ios',
    'fw_version': '2.1.1',
    'ip_addr': '192.0.2.168',
    'admin_name': 'testname',
    'admin_password': 'testpswd'
}
device_info_keywords(**device_dict)
print "\n"


print ("'dev_info_keywords' function call "
       "(arguments passed as a keyworded parameters list)")
device_info_keywords(manufacturer='cisco', os_type='ios',
                     fw_version='2.1.1', ip_addr='192.0.2.168',
                     admin_name='testname', admin_password='testpswd')
print "\n"


print ("'device_info_params_args_keywords' function call "
       "(mixed argument styling)")
os_tuple = ('cisco', 'ios', '2.1.1')
admin_dict = {'admin_name': 'testname', 'admin_password': 'testpswd'}
device_info_params_args_keywords('192.0.2.168', *os_tuple, **admin_dict)
print "\n"
