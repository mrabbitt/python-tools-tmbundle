import re
import sys
import os
from StringIO import StringIO

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pyflakes'))
# checker = __import__('pyflakes.checker').checker

import flake8.run

_FLAKE8_MESSAGE = re.compile(r'^(?P<filename>[^:]+):(?P<lineno>\d*):((?P<col>\d*):?)? (?:(?P<level>E|W)\d+ )?(?P<message>.+?)$')

_LINE_TOO_LONG_RE = re.compile(r'line too long \((?P<length>\d+) > (?P<max_length>\d+) characters\)')
_MAX_LINE_LENGTH = 120


def filter_line_too_long(warning):
    '''Exclude "line too long" warnings for lengths than _MAX_LINE_LENGTH.
    Ideally, flake8 should be configured to use a custom max line length
    rather than using a hack like this.
    '''
    match = _LINE_TOO_LONG_RE.match(warning.message)
    if match:
        length = int(match.group('length'))
        if length < _MAX_LINE_LENGTH:
            return False
    return True


def filter_warning(warning_message):
    for afilter in _WARNING_FILTERS:
        if not afilter(warning_message):
            return False
    return True


_WARNING_FILTERS = [filter_line_too_long]


class WarningMessage(object):
    message_args = ()

    def __init__(self, filename, lineno, col, message, level):
        self.filename = filename
        self.lineno = lineno
        self.col = col
        self.message = message
        self.level = level

    def __str__(self):
        return '{0}:{1}: {2}'.format(os.path.basename(self.filename),
                                     self.lineno,
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
                if filter_warning(warning):
                    warnings.append(warning)

            else:
                warnings.append(WarningMessage(filepath, 1, 1, line, 'W'))

    # assert len(warnings) == warning_count
    return warnings
