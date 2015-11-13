#!/usr/bin/python

# purpose:
# test if a pattern matches an input string


import re


def main():
    print 'Script tests if a regular expression will match provided text.\n'
    input = raw_input('Text: ')
    pattern = raw_input('Regular Expression Pattern: ')
    search_pattern = re.compile(pattern)

    if search_pattern.match(input):
        print '\nThe regular expression matches the provided text.\n'
    else:
        print '\nThe regular expression does not match the provided text.\n'


if __name__ == '__main__':
    main ()
