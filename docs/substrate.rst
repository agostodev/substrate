The ``substrate-exogorth`` Command
=========================

Installation
------------

To install substrate-exogorth, run::

  $ easy_install substrate-exogorth

or::

  $ pip install substrate-exogorth

To update your substrate-exogorth installation to the newest release::

  $ easy_install --upgrade substrate-exogorth

or::

  $ pip install --upgrade substrate-exogorth

To install or update manually, `download the PyPI package`_,
(or to stay on the bleeding edge, clone the `substrate-exogorth repository`_) and run::

  $ python setup.py install

Creating a new application
--------------------------

To create a new application, run::

  $ substrate new your-app-id

This will create a new directory ``your-app-id`` and unpack the substrate-exogorth
application libraries in it. The application name in ``app.yaml`` will be
set to ``your-app-id``.

Or, if you find installing a script to do this for you tedious, you
can clone the `substrate repository`_ and copy the ``app`` directory to
create your application.

Upgrading an existing application
---------------------------------

If you have an existing application, you can upgrade it to the latest
substrate-exogorth code by updating the substrate-exogorth package (see `Installation`_) and then running::

   $ substrate-exogorth update ~/development/your-app-id

where ``~/development/your-app-id`` is the application directory
(the one containing your ``app.yaml`` file) to upgrade.
(For example, you could run this in the current directory with ``.``)

This command will NOT touch any of your application's files. Only
"substrate-exogorth files" in the ``local/substrate-exogorth`` and ``lib/substrate-exogorth`` directories plus
``manage.py`` and ``env_setup.py`` in the application directory will be
overwritten. You can add new files to ``local/usr`` and ``lib/usr``, but do not
edit existing "substrate-exogorth files" or your changes will be lost when upgrading.

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

   $./manage.py snapdeploy

Tries to deploy you app and modules to Google AppEngine. Relies on your local git or hg repo to conduct a deploy.
Creates a version with the SHA-1 of the current repo / branch in the cloud and updates a ``snapdeploy.yaml`` file to
commit. Very useful for deploying to multiple app ids and modules with consistent codebases. Supports most options you
can pass to ``appcfg.py``

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

::

  $ ./manage.py pytest

Runs your application's tests. Any additional parameters are passed to the `py.test`_ command::

  $ ./manage.py pytest --help

    usage: pytest [options] [file_or_dir] [file_or_dir] [...]

    positional arguments:
      file_or_dir

    general:
      -k EXPRESSION         only run tests which match the given substring
                            expression. An expression is a python evaluatable
                            expression where all names are substring-matched
                            against test names and their parent classes. Example:
                            -k 'test_method or test other' matches all test
                            functions and classes whose name contains
                            'test_method' or 'test_other'. Additionally keywords
                            are matched to classes and functions containing extra
                            names in their 'extra_keyword_matches' set, as well as
                            functions which have names assigned directly to them.
      -m MARKEXPR           only run tests matching given mark expression.
                            example: -m 'mark1 and not mark2'.
      --markers             show markers (builtin, plugin and per-project ones).
      -x, --exitfirst       exit instantly on first error or failed test.
      --maxfail=num         exit after first num failures or errors.
      --strict              run pytest in strict mode, warnings become errors.
      -c file               load configuration from `file` instead of trying to
                            locate one of the implicit configuration files.
      --fixtures, --funcargs
                            show available fixtures, sorted by plugin appearance
      --pdb                 start the interactive Python debugger on errors.
      --capture=method      per-test capturing method: one of fd|sys|no.
      -s                    shortcut for --capture=no.
      --runxfail            run tests even if they are marked xfail

    reporting:
      -v, --verbose         increase verbosity.
      -q, --quiet           decrease verbosity.
      -r chars              show extra test summary info as specified by chars
                            (f)ailed, (E)error, (s)skipped, (x)failed, (X)passed
                            (w)warnings.
      -l, --showlocals      show locals in tracebacks (disabled by default).
      --report=opts         (deprecated, use -r)
      --tb=style            traceback print mode (long/short/line/native/no).
      --full-trace          don't cut any tracebacks (default is to cut).
      --color=color         color terminal output (yes/no/auto).
      --durations=N         show N slowest setup/test durations (N=0 for all).
      --pastebin=mode       send failed|all info to bpaste.net pastebin service.
      --junit-xml=path      create junit-xml style report file at given path.
      --junit-prefix=str    prepend prefix to classnames in junit-xml output
      --result-log=path     path for machine-readable result log.

    collection:
      --collect-only        only collect tests, don't execute them.
      --pyargs              try to interpret all arguments as python packages.
      --ignore=path         ignore path during collection (multi-allowed).
      --confcutdir=dir      only load conftest.py's relative to specified dir.
      --doctest-modules     run doctests in all .py modules
      --doctest-glob=pat    doctests file matching pattern, default: test*.txt

    test session debugging and configuration:
      --basetemp=dir        base temporary directory for this test run.
      --version             display pytest lib version and import information.
      -h, --help            show help message and configuration info
      -p name               early-load given plugin (multi-allowed). To avoid
                            loading of plugins, use the `no:` prefix, e.g.
                            `no:doctest`.
      --trace-config        trace considerations of conftest.py files.
      --debug               store internal tracing debug information in
                            'pytestdebug.log'.
      --assert=MODE         control assertion debugging tools. 'plain' performs no
                            assertion debugging. 'reinterp' reinterprets assert
                            statements after they failed to provide assertion
                            expression information. 'rewrite' (the default)
                            rewrites assert statements in test modules on import
                            to provide assert expression information.
      --no-assert           DEPRECATED equivalent to --assert=plain
      --no-magic            DEPRECATED equivalent to --assert=plain
      --genscript=path      create standalone pytest script at given target path.

    distributed and subprocess testing:
      -f, --looponfail      run tests in subprocess, wait for modified files and
                            re-run failing test set until all pass.
      -n numprocesses       shortcut for '--dist=load --tx=NUM*popen'
      --boxed               box each test run in a separate process (unix)
      --dist=distmode       set mode for distributing tests to exec environments.
                            each: send each test to each available environment.
                            load: send each test to available environment.
                            (default) no: run tests inprocess, don't distribute.
      --tx=xspec            add a test execution environment. some examples: --tx
                            popen//python=python2.5 --tx socket=192.168.1.102:8888
                            --tx ssh=user@codespeak.net//chdir=testcache
      -d                    load-balance tests. shortcut for '--dist=load'
      --rsyncdir=DIR        add directory for rsyncing to remote tx nodes.
      --rsyncignore=GLOB    add expression for ignores when rsyncing to remote tx
                            nodes.


    [pytest] ini-options in the next pytest.ini|tox.ini|setup.cfg file:

      markers (linelist)       markers for test functions
      norecursedirs (args)     directory patterns to avoid for recursion
      usefixtures (args)       list of default fixtures to be used with this project
      python_files (args)      glob-style file patterns for Python test module discovery
      python_classes (args)    prefixes for Python test class discovery
      python_functions (args)  prefixes for Python test function and method discovery
      addopts (args)           extra command line options
      minversion (string)      minimally required pytest version
      rsyncdirs (pathlist)     list of (relative) paths to be rsynced for remote distributed testing.
      rsyncignore (pathlist)   list of (relative) glob-style paths to be ignored for rsyncing.
      looponfailroots (pathlist) directories to check for changes


    to see available markers type: py.test --markers
    to see available fixtures type: py.test --fixtures
    (shown according to specified file_or_dir or current dir if not specified)


Testing
-------

As noted above, ``manage.py`` has a ``test`` and a ``pytest`` command.

Included with the Substrate base app is a simple "hello world" test that you can run to verify your installation. It is
located in ``tests/test_main.py``.

.. Links

.. _download the PyPI package: http://pypi.python.org/pypi/substrate-exogorth#downloads

.. _substrate-exogorth repository: http://bitbucket.org/gumptioncom/substrate-exogorth

.. _unittest2: http://pypi.python.org/pypi/unittest2
.. _unitetest2 discover: http://docs.python.org/library/unittest.html#test-discovery

.. _py.test: http://pytest.org/latest/

.. _iPython: http://ipython.org/
