#!/usr/bin/python

# purpose:
# split provided input using the provided pattern
# and print out something useful for reference


import re


def main():
    input_parts = []

    print 'Script splits input using provided pattern and prints result.\n'
    input = raw_input('Text: ')
    pattern = raw_input('Regular Expression Pattern: ')
    list = re.split(pattern, input)

    print '\nOriginal text:\n' + input
    print '\nResulting list:'
    print list

    print '\nList positions:\n'
    position = 0
    for part in list:
        print str(position) + ': ' + list[position]
        position += 1


if __name__ == '__main__':
    main ()
