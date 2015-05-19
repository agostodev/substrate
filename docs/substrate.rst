The ``substrate`` Command
=========================

Installation
------------

To install substrate, run::

  $ easy_install substrate

or::

  $ pip install substrate

To update your substrate installation to the newest release::

  $ easy_install --upgrade substrate

or::

  $ pip install --upgrade substrate

To install or update manually, `download the PyPI package`_,
(or to stay on the bleeding edge, clone the `substrate repository`_) and run::

  $ python setup.py install

Creating a new application
--------------------------

To create a new application, run::

  $ substrate new your-app-id

This will create a new directory ``your-app-id`` and unpack the substrate
application libraries in it. The application name in ``app.yaml`` will be
set to ``your-app-id``.

Or, if you find installing a script to do this for you tedious, you
can clone the `substrate repository`_ and copy the ``app`` directory to
create your application.

Upgrading an existing application
---------------------------------

If you have an existing application, you can upgrade it to the latest
substrate code by updating the substrate package (see `Installation`_) and then running::

   $ substrate update ~/development/your-app-id

where ``~/development/your-app-id`` is the application directory
(the one containing your ``app.yaml`` file) to upgrade.
(For example, you could run this in the current directory with ``.``)

This command will NOT touch any of your application's files. Only
"substrate files" in the ``local/substrate`` and ``lib/substrate`` directories plus
``manage.py`` and ``env_setup.py`` in the application directory will be
overwritten. You can add new files to ``local/usr`` and ``lib/usr``, but do not
edit existing "substrate files" or your changes will be lost when upgrading.

Management Console
------------------

``manage.py`` is a management console for your app. It can invoke several commands.

::

  $ ./manage.py shell

Runs a shell against your local application (requires `iPython`_).

::

  $ ./manage.py rshell

Runs a remote shell against your application on Google App
Engine. To specify a different application ID than what is in your
``app.yaml``, use ``-A``. If your remote API endpoint is not at
the default location, you can pass the path as an argument.

::

  $ ./manage.py test

Runs your application's tests. Any additional parameters are passed to the `unitetest2 discover`_ command::

  $ ./manage.py test --help
  
  Usage: unit2 discover [options]

  Options:
    -h, --help            show this help message and exit
    -v, --verbose         Verbose output
    -f, --failfast        Stop on first fail or error
    -c, --catch           Catch ctrl-C and display results so far
    -b, --buffer          Buffer stdout and stderr during tests
    -s START, --start-directory=START
                          Directory to start discovery ('.' default)
    -p PATTERN, --pattern=PATTERN
                          Pattern to match tests ('test*.py' default)
    -t TOP, --top-level-directory=TOP
                          Top level directory of project (defaults to start
                          directory)

Testing
-------

As noted above, ``manage.py`` has a ``test`` command. This runs all
the tests in the ``tests`` directory of your application using
`unittest2`_. Included with the Substrate base app is a simple "hello
world" test that you can run to verify your installation. It is
located in ``tests/handlers/test_main.py``.

.. Links

.. _download the PyPI package: http://pypi.python.org/pypi/substrate#downloads

.. _substrate repository: http://bitbucket.org/gumptioncom/substrate

.. _unittest2: http://pypi.python.org/pypi/unittest2
.. _unitetest2 discover: http://docs.python.org/library/unittest.html#test-discovery

.. _iPython: http://ipython.org/
