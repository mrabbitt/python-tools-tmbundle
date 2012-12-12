
"""
Implementation of the command-line I{flake8} tool.
"""

import sys
import flake8parser


def main(args):
    warnings = flake8parser.flake8_warnings(args[0])
    for warning in warnings:
        print warning

if __name__ == '__main__':
    main(sys.argv[1:])
