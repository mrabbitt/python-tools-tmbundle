from __future__ import unicode_literals, print_function
import re
import sys
import os
try:
    from StringIO import StringIO
except:
    from io import StringIO

# TODO:  Add compatility with flake8 3.0 (flake8.run no longer exists).
# For now:  pip install 'flake8>=2.0,<3.0'
try:
    import flake8.run
    assert flake8.__version__ >= '2.0'
except Exception as e:
    print('Unsatisfied dependency for validation command: flake8 >= 2.0: {0}'.format(e))
    raise SystemExit(1)

# Warning codes from:  http://flake8.readthedocs.org/en/2.0/warnings.html
_FLAKE8_MESSAGE = re.compile(r'^(?P<filename>[^:]+):(?P<lineno>\d*):((?P<col>\d*):?)? (?:(?P<level>E|W|F|C|N)\d+ )?(?P<message>.+?)$')  # noqa


class WarningMessage(object):
    '''Wrapper for warning message returned by flake8.'''
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

    backup_stdout = sys.stdout

    try:
        sys.stdout = StringIO()      # capture output
        warning_count = flake8.run.check_file(filepath)
        out = sys.stdout.getvalue()  # release output
    finally:
        sys.stdout.close()   # close the stream
        sys.stdout = backup_stdout  # restore original stdout

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

    if len(warnings) != warning_count:
        print("flake8 warnings = {0}, parsed warning count = {1}".format(
            warning_count, len(warnings)
        ), file=sys.stderr)
    return warnings
