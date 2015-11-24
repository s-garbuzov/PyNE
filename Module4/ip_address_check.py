#!/usr/bin/python

# purpose:
# demonstrate multiple options for checking an IPv4 address
# simple options are easier to code and may be all that is necessary
#    depending on the quality of input
# more complex options may not be necessary, but are more thorough


import re


# checks to see if a value has four 1-3 digit numbers separated by decimals
def basic_ipv4_address_format(ipv4_candidates):
    ipv4_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
    print '\nResults of basic IPv4 pattern check (no verification of octet value):'
    for candidate in ipv4_candidates:
        if ipv4_pattern.match(candidate):
            print candidate + ': is possibly an IPv4 address.'
        else:
            print candidate + ': is not an IPv4 address.'


# checks to see if a value has four 1-3 digit numbers separated by decimals
# then verifies the value of each set of digits has a value between 0-255
def ipv4_address_8bit_check(ipv4_candidates):
    ipv4_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')  
    print '\nResults of IPv4 octet value check:'
    for candidate in ipv4_candidates:
        ipv4_valid = 'yes'
        if ipv4_pattern.match(candidate):
            ipv4_octets = ipv4_pattern.match(candidate)
            for octet in ipv4_octets.groups():
                if ((int(octet) < 0) or (int(octet) > 255)):
                    ipv4_valid = 'no'
        else:
            ipv4_valid = 'no'
        if (ipv4_valid == 'yes'):
            print candidate + ': is likely a valid IPv4 address.'
        else:
            print candidate + ': is not an IPv4 address.'

            
# checks to see if a value has four 1-3 digit numbers separated by decimals
# then verifies the first octet is:
#    > 0
#    < 224
#    not equal to 127
# then verifies the value of the second to fourth octets are between 0-255
# more checks can be made if you want to exclude additional ranges such as:
#    self-assigned addresses re RFC 3927
#    6to4 anycast
#    carrier-grade NAT
#    etc.
def ipv4_unicast_address_check(ipv4_candidates):
    ipv4_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')  
    print '\nResults of IPv4 unicast check:'
    for candidate in ipv4_candidates:
        ipv4_unicast = 'yes'
        if ipv4_pattern.match(candidate):
            ipv4_octets = ipv4_pattern.match(candidate)
            ipv4_octets = ipv4_octets.groups()
            first_octet = int(ipv4_octets[0])
            if ((first_octet < 1) or (first_octet >= 224) or (first_octet =='127')):
                ipv4_unicast = 'no'
            for octet in range(1, 3):
                if ((int(ipv4_octets[octet]) < 0) or (int(ipv4_octets[octet]) > 255)):
                    ipv4_unicast = 'no'
        else:
            ipv4_unicast = 'no'
        if (ipv4_unicast == 'yes'):
            print candidate + ': is a unicast IPv4 address.'
        else:
            print candidate + ': is not a valid unicast IPv4 address.'


def main():
    ipv4_candidates = ['192.168.0.1', '8.8.8.8', '224.0.0.251', '1.2.3.4.5', 
        'no.address', '999.888.777.666', '245.1.2.3', 'some text', '0.1.2.3']

    basic_ipv4_address_format(ipv4_candidates)
    ipv4_address_8bit_check(ipv4_candidates)
    ipv4_unicast_address_check(ipv4_candidates)


if __name__ == '__main__':
    main ()
