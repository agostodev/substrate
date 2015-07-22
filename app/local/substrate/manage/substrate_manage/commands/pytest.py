""" Run tests using pytest test runner """
import sys
import os
import logging


def usage():
    print """
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


[pytest] ini-options in the next pytest.ini|tox.ini|setup.cfg file:

  markers (linelist)       markers for test functions
  norecursedirs (args)     directory patterns to avoid for recursion
  usefixtures (args)       list of default fixtures to be used with this project
  python_files (args)      glob-style file patterns for Python test module discovery
  python_classes (args)    prefixes for Python test class discovery
  python_functions (args)  prefixes for Python test function and method discovery
  addopts (args)           extra command line options
  minversion (string)      minimally required pytest version


to see available markers type: py.test --markers
to see available fixtures type: py.test --fixtures
(shown according to specified file_or_dir or current dir if not specified)
    """


if __name__ == '__main__':
    if 'APPENGINE_SDK' not in os.environ:
        logging.error('APPENGINE_SDK environment variable is not set; exiting...')
    sdk_path = os.environ['APPENGINE_SDK']

    sys.path.insert(0, sdk_path)
    import dev_appserver

    dev_appserver.fix_sys_path()
    import pytest

    # argv = ['-x', 'tests']
    argv = []
    argv.extend(sys.argv[1:])

    sys.exit(pytest.main(argv))
