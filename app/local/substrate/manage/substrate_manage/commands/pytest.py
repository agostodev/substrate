import sys
import os
import logging 

if __name__ == '__main__':
    if 'APPENGINE_SDK' not in os.environ:
        logging.error('APPENGINE_SDK environment variable is not set; exiting...')
    sdk_path = os.environ['APPENGINE_SDK']

    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    import pytest

    #argv = ['-x', 'tests']
    argv = []
    argv.extend(sys.argv[1:])

    sys.exit(pytest.main(argv))
