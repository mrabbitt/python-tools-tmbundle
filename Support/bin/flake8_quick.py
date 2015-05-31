"""
Implementation of the command-line I{flake8} tool.
"""
from __future__ import print_function
import sys
import flake8parser

# Max number of messages to be displayed in tooltip.
MAX_WARNINGS = 10


def main(args):
    warnings = flake8parser.flake8_warnings(args[0])
    for warning in warnings[0:MAX_WARNINGS]:
        print(warning)
    if len(warnings) > MAX_WARNINGS:
        more_count = len(warnings) - MAX_WARNINGS
        print('...{0} more messages...'.format(more_count))


if __name__ == '__main__':
    main(sys.argv[1:])
