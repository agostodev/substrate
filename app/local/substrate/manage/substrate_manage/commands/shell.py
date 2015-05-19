""" Run an interactive console after including AppEngine and project libraries. """

import getopt
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s')

from google.appengine.api import yaml_errors
from google.appengine.tools import dev_appserver
from google.appengine.tools import dev_appserver_main

config = matcher = None

try:
    config, matcher, from_cache = dev_appserver.LoadAppConfig(".", {}, default_partition='dev')
except yaml_errors.EventListenerError, e:
    logging.error('Fatal error when loading application configuration:\n' +
                  str(e))
except dev_appserver.InvalidAppConfigError, e:
    logging.error('Application configuration file invalid:\n%s', e)

appserver_args = dev_appserver_main.DEFAULT_ARGS.copy()


def usage():
    print """%s

Usage: python manage.py shell

Options:
  -b DIR, --blobstore_path=DIR          Path to directory to use for storing Blobstore file stub data.
  -d DS_FILE, --datastore_path=DS_FILE  Path to file to use for storing Datastore file stub data.
                                        (Default %s)
  -mu USER --mysql_user=USER            The MySQL user
  -mp USER --mysql_password=PASSWORD    The MySQL password
  -h, --help                            Show this help.
""" % (__doc__, appserver_args[dev_appserver_main.ARG_DATASTORE_PATH])

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:b:mu:mp:", ["help", "datastore_path=", "blobstore_path=", "mysql_user=", "mysql_password="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--datastore_path"):
            appserver_args[dev_appserver_main.ARG_DATASTORE_PATH] = arg
        elif opt in ("-b", "--blobstore_path"):
            appserver_args[dev_appserver_main.ARG_BLOBSTORE_PATH] = arg
        elif opt in ("-mu", "--mysql_user"):
            appserver_args[dev_appserver_main.ARG_MYSQL_USER] = arg
        elif opt in ("-mp", "--mysql_password"):
            appserver_args[dev_appserver_main.ARG_MYSQL_PASSWORD] = arg

    dev_appserver.SetupStubs(config.application, **appserver_args)

    try:
        banner = "Interactive App Engine Shell for app-id '%s'" % config.application
        from IPython import embed
        embed(header=banner)
    except:
        pass
