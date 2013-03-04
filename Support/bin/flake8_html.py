
"""
Implementation of the command-line I{flake8} tool.
"""

import sys
import os

import flake8parser

HTML = """
<html>
  <head>
    <title>Flake8 Results</title>
    <style type="text/css">
      body {
        font-size: 13px;
      }

      pre {
        background-color: #eee;
        color: #400;
        margin: 3px 0;
      }

      h1, h2 { margin: 0 0 5px; }

      h1 { font-size: 20px; }
      h2 { font-size: 16px;}

      span.warning {
        color: #c90;
        text-transform: uppercase;
        font-weight: bold;
      }

      span.error {
        color: #900;
        text-transform: uppercase;
        font-weight: bold;
      }

      ul {
        margin: 10px 0 0 20px;
        padding: 0;
      }

      li {
        margin: 0 0 10px;
      }
    </style>
  </head>
  <body>
    <h1>Python Lint</h1>
    <h2>%(results)s</h2>

    <ul>
      %(output)s
    </ul>
  </body>
</html>
"""


def main(args):
    # import re
    # lineno = re.compile(r'^(\d+)\:')
    results = {'E': 0, 'W': 0}
    output, warnings = [], []

    filepath = args[0]

    warnings += flake8parser.flake8_warnings(filepath)

    for warning in warnings:
        # line = lineno.sub('' % dict(
        #     filepath=warning.filename,
        #     lineno=warning.lineno,
        #     col=warning.col,
        # ), str(warning))
        output.append('<li><a href="txmt://open?url=file://%(filepath)s&line=%(lineno)s&column=%(col)s">%(filename)s:%(lineno)s</a><pre><code>%(message)s</code></pre></li>' % dict(  # NOQA
            col=warning.col,
            lineno=warning.lineno,
            filepath=warning.filename,
            filename=os.path.basename(warning.filename),
            message=warning.message % warning.message_args,
        ))
        results[warning.level] += 1

    output = "\n\n".join(output)

    print HTML % dict(
        output=output,
        results='%d error(s), %d warning(s)' % (results['E'], results['W']),
    )

if __name__ == '__main__':
    main(sys.argv[1:])
