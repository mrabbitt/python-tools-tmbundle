Python Tools TextMate Bundle
============================

Installation
------------

1. Clone the repository from GitHub.

::

    git clone https://github.com/dcramer/python-tools-tmbundle.git ~/Library/Application\ Support/TextMate/Bundles/PythonTools.tmbundle
    cd ~/Library/Application\ Support/TextMate/Bundles/PythonTools.tmbundle
    pip install --target Support/lib flake8

2. Reload TextMate or Navigate to Bundles -> Bundle Editor -> Reload Bundles.

PyFlakes
--------

* *Validate Syntax* (⇧⌥V) validates the syntax of the file using
`Flake8<http://flake8.readthedocs.org/en/latest/>`_ and shows the results in a new window.
* *Validate Syntax Quick* (⌘S) same as above except that instead of a dedicated window you simply get a tooltip showing the the errors and warnings.

Credits
-------

Based on the `JavaScript Tools Bundle <https://github.com/johnmuhl/javascript-tools-tmbundle>`_.