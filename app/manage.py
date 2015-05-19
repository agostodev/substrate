#! /usr/bin/env python

import os, sys


LOCAL_SUBSTRATE_LIB_PATH = [
    os.path.join('.', 'local', 'substrate', 'lib'),
]
sys.path = LOCAL_SUBSTRATE_LIB_PATH + sys.path

from management import *

if __name__ == '__main__':
    run_command(__file__, globals())
