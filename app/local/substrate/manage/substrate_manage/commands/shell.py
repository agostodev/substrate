""" Run an interactive console after including AppEngine and project libraries. """

import getopt
import logging
import sys
import os


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s')

from google.appengine.api import yaml_errors
import dev_appserver


def usage():
    print """{}

Usage: python manage.py shell

Options:
  -b DIR, --blobstore_path=DIR          Path to directory to use for storing Blobstore file stub data.
  -d DS_FILE, --datastore_path=DS_FILE  Path to file to use for storing Datastore file stub data.
  -mu USER --mysql_user=USER            The MySQL user
  -mp USER --mysql_password=PASSWORD    The MySQL password
  -h, --help                            Show this help.
""".format(__doc__)



if __name__ == "__main__":
    config_paths = ['.']
    app_id_override = None
    datastore_path = '/dev/null'
    #blobstore_path = '/dev/null'
    #mysql_user = None
    #mysql_password = None

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
            datastore_path = arg
        #elif opt in ("-b", "--blobstore_path"):
        #    blobstore_path = arg
        #elif opt in ("-mu", "--mysql_user"):
        #    mysql_user = arg
        #elif opt in ("-mp", "--mysql_password"):
        #    mysql_password = arg

    from google.appengine.tools.devappserver2 import application_configuration
    configuration = application_configuration.ApplicationConfiguration(config_paths, app_id_override)
    os.environ['APPLICATION_ID'] = configuration.app_id

    from google.appengine.api import apiproxy_stub_map, datastore_file_stub
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

    #datastore
    stub = datastore_file_stub.DatastoreFileStub(configuration.app_id, datastore_path, '/')
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    #memcache
    from google.appengine.api.memcache import memcache_stub
    stub = memcache_stub.MemcacheServiceStub()
    apiproxy_stub_map.apiproxy.RegisterStub('memcache', stub)

    banner = "Interactive App Engine Shell for app '{}'".format(configuration.app_id)
    from IPython import embed
    embed(header=banner)

