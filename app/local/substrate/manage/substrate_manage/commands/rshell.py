""" Connect to a remote datastore through an interactive console. """

from google.appengine.tools import os_compat

import logging
import sys
import os
import traceback
import getpass
import getopt

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s')

from google.appengine.api import yaml_errors
from google.appengine.dist import py_zipimport
from google.appengine.tools import appcfg
from google.appengine.tools import dev_appserver
from google.appengine.ext.remote_api import remote_api_stub

config = matcher = None

try:
    config, matcher, from_cache = dev_appserver.LoadAppConfig(".", {})
except yaml_errors.EventListenerError, e:
    logging.error('Fatal error when loading application configuration:\n' + str(e))
except dev_appserver.InvalidAppConfigError, e:
    logging.error('Application configuration file invalid:\n%s', e)


def auth_func():
    return raw_input('Username:'), getpass.getpass('Password:')

DEFAULT_PATH = '/_ah/remote_api'


def path():
    if not len(args):
        return DEFAULT_PATH
    else:
        return args[0]


def app_id():
    for opt in optlist:
        if opt[0] == '-A':
            return opt[1]

    return config.application

if __name__ == "__main__":
    optlist, args = getopt.getopt(sys.argv[1:], 'A:')

    remote_api_stub.ConfigureRemoteDatastore(None, path(), auth_func, "%s.appspot.com" % app_id())
    remote_api_stub.MaybeInvokeAuthentication()

    os.environ['HTTP_HOST'] = "%s.appspot.com" % app_id()

    try:
        banner = "Interactive REMOTE App Engine Shell for app-id '%s'" % app_id()
        from IPython import embed
        embed(header=banner)
    except:
        pass
