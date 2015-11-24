#!/usr/bin/python

# purpose:
# check format of a MAC address
# show an example of normalized MAC address output


import re


# checks to see if a value has four 1-3 digit numbers separated by decimals
def basic_mac_address_check(mac_candidates):
    # pattern based on colon or dash delimited bytes
    mac_pattern_bytes = re.compile(r'^[0-9a-f]{1,2}([\:\-][0-9a-f]{1,2}){5}$', re.IGNORECASE)
    # patter based on two byte words separated by decimals, common on Cisco equipment
    mac_pattern_3words = re.compile(r'^[0-9a-f]{4}(\.[0-9a-f]{4}){2}$', re.IGNORECASE)
    print '\nResults of basic MAC address pattern check:'
    for candidate in mac_candidates:
        if (mac_pattern_bytes.match(candidate) or mac_pattern_3words.match(candidate)):
            print candidate + ' -> is a valid MAC address.'
        else:
            print candidate + ' -> is not a MAC address.'


# normalizing MAC address to a common format is useful
#    - it allows using MAC addresses as keys in dictionaries and external databases
#    - it allows for easy comparison when MAC sources provide input in different formats
# note: these values would normally be added to lists or dictionaries
#       or simply return a single value to a function call on a singular basis prior to 
#           prior to comparison (rather than a list as shown here)
#       they are printed here only for demonstration purposes...
#       i.e., this is just a demo
def normalize_mac_address(mac_candidates):
    mac_pattern_bytes = re.compile(r'^([0-9a-f]{1,2})[\:\-]([0-9a-f]{1,2})[\:\-]([0-9a-f]{1,2})[\:\-]([0-9a-f]{1,2})[\:\-]([0-9a-f]{1,2})[\:\-]([0-9a-f]{1,2})$', re.IGNORECASE)
    mac_pattern_3words = re.compile(r'^([0-9a-f]{4})\.([0-9a-f]{4})\.([0-9a-f]{4})$', re.IGNORECASE)
    print '\nResults of normalizing MAC address values:'
    for candidate in mac_candidates:
        normalized_mac = ''
        if (mac_pattern_bytes.match(candidate)):
            mac_bytes = mac_pattern_bytes.match(candidate)
            mac_bytes = mac_bytes.groups()
            for byte in mac_bytes:
                if len(byte) == 1:
                    normalized_mac = normalized_mac + '0' + byte
                else:
                    normalized_mac = normalized_mac + byte
            normalized_mac = normalized_mac.lower()
            print candidate + ' -> ' + normalized_mac
        elif (mac_pattern_3words.match(candidate)):
            mac_words = mac_pattern_3words.match(candidate)
            mac_words = mac_words.groups()
            for word in mac_words:
                normalized_mac = normalized_mac + word
            normalized_mac = normalized_mac.lower()
            print candidate + ' -> ' + normalized_mac
        else:
            print candidate + ' -> is not a MAC address.'


def main():
    mac_candidates = ['0:1:2:3:4:5', '00:01:02:03:04:05', '00:1e:d0:12:34:56', 
        'ff:ff:ff:ff:ff:ff', '20:C9:D0:C4:AB:CD', '0001.0203.0405', '0201.ABCD.EEFF',
        '245.1.2.3', 'some.kinda.text', '00:ze:bg:ac:11:22']

    basic_mac_address_check(mac_candidates)
    normalize_mac_address(mac_candidates)


if __name__ == '__main__':
    main ()
