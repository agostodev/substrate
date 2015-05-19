"""
Functions to initialize environment settings.
"""

def get_project_root():
    """
    Returns the project root path.

    Starts in current working directory and traverses up until app.yaml is found.
    Assumes app.yaml is in project root.
    """
    import os
    start_path = os.path.abspath('.')
    search_path = start_path
    while search_path:
        app_yaml_path = os.path.join(search_path, 'app.yaml')
        if os.path.exists(app_yaml_path):
            break
        search_path, last_dir = os.path.split(search_path)
    else:
        raise os.error('app.yaml not found for env_setup.get_project_root().%sSearch started in: %s' % (os.linesep, start_path))
    return search_path


def setup():
    """Adds <project_root>/lib/substrate and <project_root>/lib/usr to the python path."""
    import os
    import sys
    project_root = get_project_root()
    if os.path.exists(project_root):
        lib_substrate_path = os.path.join(project_root, 'lib', 'substrate')
        if lib_substrate_path not in sys.path:
            sys.path.insert(0, lib_substrate_path)
        lib_usr_path = os.path.join(project_root, 'lib', 'usr')
        if lib_usr_path not in sys.path:
            sys.path.insert(0, lib_usr_path)


def setup_django(settings='settings', version='1.3', ):
    """
    Sets up the django libraries.

    :param settings: The name of the settings file. Default: ``'settings'``.
    :param version: The django version to set up. Default: ``'1.3'``.
    """
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = settings
    from google.appengine.dist import use_library
    use_library('django', version)
    from django.conf import settings
    _ = settings.TEMPLATE_DIRS


def setup_tests():
    """Fix the sys.path to include our extra paths."""
    import os
    import sys
    # Only works for UNIXy style OSes.
    # Find App Engine SDK
    dev_appserver = None
    dir_path = ""
    for d in os.environ["PATH"].split(":"):
        dev_appserver_path = os.path.join(d, "dev_appserver.py")
        if os.path.isfile(dev_appserver_path):
            dir_path = os.path.abspath(os.path.dirname(os.path.realpath(dev_appserver_path)))
            sys.path.append(dir_path)
            import dev_appserver
            sys.path.pop()
    if not hasattr(sys, 'version_info'):
        sys.stderr.write('Very old versions of Python are not supported. Please '
                         'use version 2.7 or greater.\n')
        sys.exit(1)
    version_tuple = tuple(sys.version_info[:2])
    if version_tuple != (2, 7):
        sys.stderr.write('Warning: Python %d.%d is not supported. Please use '
                         'version 2.7.\n' % version_tuple)
    if not dir_path:
        sys.stderr.write("Could not find SDK path.  Make sure dev_appserver.py is in your PATH")
        sys.exit(1)
    extra_paths = dev_appserver.EXTRA_PATHS[:]
    substrate_paths = [
        os.path.join('.', 'lib', 'substrate'),
        os.path.join('.', 'local', 'substrate', 'lib'),
        os.path.join('.', 'local', 'substrate', 'manage'),
        ]
    usr_paths = [
        os.path.join('.', 'lib', 'usr'),
        os.path.join('.', 'local', 'usr', 'lib'),
        os.path.join('.', 'local', 'usr', 'manage'),
        ]
    sys.path = extra_paths + substrate_paths + usr_paths + sys.path
