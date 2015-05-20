""" Connect to a remote datastore through an interactive console. """

import getopt
import logging
import sys
import os
import getpass

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s')

from google.appengine.api import yaml_errors
import dev_appserver


def usage():
    print """{}

Usage: python manage.py rshell

Options:
  -A APP_ID, --application=APP_ID       Set the application, overriding the application value from app.yaml file.
  -h, --help                            Show this help.
""".format(__doc__)


def auth_func():
    return raw_input('Username:'), getpass.getpass('Password:')

DEFAULT_PATH = '/_ah/remote_api'


if __name__ == "__main__":
    config_paths = ['.']
    app_id_override = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hA:", ["help", "application="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-A", "--application"):
            app_id_override = arg

    from google.appengine.tools.devappserver2 import application_configuration
    configuration = application_configuration.ApplicationConfiguration(config_paths, app_id_override)
    app_id = '~'.join(configuration.app_id.split('~')[1:])

    from google.appengine.api import apiproxy_stub_map, datastore_file_stub
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

    from google.appengine.ext.remote_api import remote_api_stub
    remote_api_stub.ConfigureRemoteDatastore(None, DEFAULT_PATH, auth_func, "{}.appspot.com".format(app_id))
    #remote_api_stub._ConfigureRemoteApiWithOAuthCredentials(None, DEFAULT_PATH, auth_func, "{}.appspot.com".format(app_id))
    remote_api_stub.MaybeInvokeAuthentication()


    banner = "Interactive REMOTE App Engine Shell for app '{}'".format(app_id)
    from IPython import embed
    embed(header=banner)

