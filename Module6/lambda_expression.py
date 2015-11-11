#!/usr/bin/env python

# Examples of using lambda expression
#
# NOTES:
# Like def, lambda expression creates a function object to be called later,
# but it returns the function object instead of assigning it to a name.
# Since lambda is an expression (not a statement) it can appear in places
# where a def is not allowed by Python's syntax, for example inside a list
# literal.
# The lambda's body is a single expression, not a block of statements, it is
# designed for coding simple constructs with a small bits of executable code,
# and def handles larger tasks.
# Lambdas are entirely optional, defs can always be used instead.


device1 = {'vendor': 'Cisco', 'os_type': 'IOS'}
device2 = {'vendor': 'Cisco', 'os_type': 'IOS-XR'}
device3 = {'vendor': 'Cisco', 'os_type': 'NX-OS'}
device4 = {'vendor': 'HP', 'os_type': 'Comware'}
device5 = {'vendor': 'HP', 'os_type': 'Procurve'}
device6 = {'vendor': 'Brocade', 'os_type': 'VDX'}
device7 = {'vendor': 'Brocade', 'os_type': 'ICX'}
device8 = {'vendor': 'Brocade', 'os_type': 'MLX'}

all_devices = [device1, device2, device3, device4,
               device5, device6, device7, device8]
print "\n"
print "List of all network devices:"
for device in all_devices:
    print " %s" % device

#
# Functionality implemented via use of lambda expression
#

print "\n"
print "%s" % ("-" * 70)
print " Device selection implemented with the use of lambda expression"
print "%s" % ("-" * 70)
cisco_devices = filter(lambda x: x['vendor'].lower() == 'cisco',
                       all_devices)
print "\n"
print "List of Cisco network devices:"
for device in cisco_devices:
    print " %s" % device

hp_devices = filter(lambda x: x['vendor'].lower() == 'hp',
                    all_devices)
print "\n"
print "List of HP network devices: %s"
for device in hp_devices:
    print " %s" % device

brocade_devices = filter(lambda x: x['vendor'].lower() == 'brocade',
                         all_devices)
print "\n"
print "List of Brocade network devices:"
for device in brocade_devices:
    print " %s" % device


#
# Similar functionality implemented with the use of multiple def functions
#

print "\n"
print "%s" % ("-" * 70)
print " Device selection implemented with the use of multiple def functions"
print "%s" % ("-" * 70)


def is_cisco_device(device):
    return (device['vendor'].lower() == 'cisco')


def is_hp_device(device):
    return (device['vendor'].lower() == 'hp')


def is_brocade_device(device):
    return (device['vendor'].lower() == 'brocade')


cisco_devices = filter(is_cisco_device, all_devices)
print "\n"
print "List of Cisco network devices:"
for device in cisco_devices:
    print " %s" % device

hp_devices = filter(is_hp_device, all_devices)
print "\n"
print "List of HP network devices: %s"
for device in hp_devices:
    print " %s" % device

brocade_devices = filter(is_brocade_device, all_devices)
print "\n"
print "List of Brocade network devices:"
for device in brocade_devices:
    print " %s" % device

#
# Similar functionality implemented with the use of a single def function
#

print "\n"
print "%s" % ("-" * 70)
print " Device selection implemented with the use of a single def function"
print "%s" % ("-" * 70)


def get_vendor_devices(dev_list, vendor):
    vlist = []
    for item in dev_list:
        if item['vendor'].lower() == vendor.lower():
            vlist.append(item)
    return vlist

cisco_devices = get_vendor_devices(all_devices, 'cisco')
print "\n"
print "List of Cisco network devices:"
for device in cisco_devices:
    print " %s" % device

hp_devices = get_vendor_devices(all_devices, 'hp')
print "\n"
print "List of HP network devices: %s"
for device in hp_devices:
    print " %s" % device

brocade_devices = get_vendor_devices(all_devices, 'brocade')
print "\n"
print "List of Brocade network devices:"
for device in brocade_devices:
    print " %s" % device

print "\n"
