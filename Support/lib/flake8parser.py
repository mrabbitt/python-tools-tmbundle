import re
import sys
import os
from StringIO import StringIO

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pyflakes'))
# checker = __import__('pyflakes.checker').checker

import flake8.run

_FLAKE8_MESSAGE = re.compile(r'^(?P<filename>[^:]+):(?P<lineno>\d*):(?P<col>\d*):? (?:(?P<level>E|W)\d+ )?(?P<message>.+?)$')

class WarningMessage(object):
    message_args = ()

    def __init__(self, filename, lineno, col, message, level):
        """docstring for __init__"""
        self.filename = filename
        self.lineno = lineno
        self.col = col
        self.message = message
        self.level = level

    def __str__(self):
        return '%s:%s: %s' % (os.path.basename(self.filename), self.lineno,
                              self.message % self.message_args)


def flake8_warnings(filepath):
    flake8.run._initpep8()

    backup_stdout = sys.stdout

    try:
        sys.stdout = StringIO()      # capture output
        warning_count = flake8.run.check_file(filepath)
        out = sys.stdout.getvalue()  # release output
    finally:
        sys.stdout.close()   # close the stream
        sys.stdout = backup_stdout  # restore original stdout

    out  # captured output wrapped in a string
    warnings = []
    if out:
        for line in out.splitlines():
            match = _FLAKE8_MESSAGE.match(line.strip())
            if match:
                level = match.group('level')
                if not match.group('level') in ('E', 'W'):
                    level = 'W'

                warning = WarningMessage(match.group('filename'),
                                         match.group('lineno'),
                                         match.group('col'),
                                         match.group('message'), level)
                warnings.append(warning)

            else:
                warnings.append(WarningMessage(filepath, 1, 1, line, 'W'))

    # assert len(warnings) == warning_count
    return warnings
