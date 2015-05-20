""" Run tests using unittest2 'discover' """
import os
import sys
import getopt

import env_setup
env_setup.setup_django()


def usage():
    print """{}
Usage: python manage.py test

Options:
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output
  -f, --failfast   Stop on first failure
  -c, --catch      Catch control-C and display results
  -b, --buffer     Buffer stdout and stderr during test runs

""".format(__doc__)

__unittest = True
try:
    from unittest2.main import main_ as main
except ImportError:
    from unittest.main import main

try:
    opts, args = getopt.getopt(sys.argv[1:], "hvqfcbs", ["help", "verbose", "quiet", "failfast", "catch", "buffer", "start-directory"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

dir = False
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    if opt in ("-s", "--start-directory"):
	dir = arg

sys.path.insert(0, os.path.abspath(os.path.curdir))

if __name__ == "__main__":
    argv = ['unit2', 'discover', '--start-directory', dir] if dir else ['unit2', 'discover', '--start-directory', 'tests'] 
    argv.extend(sys.argv[1:])
    sys.argv = argv
    main()
