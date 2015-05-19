#!/usr/bin/env python
""" Substrate management interface. Fixes up appengine and substrate paths and runs substrate commands."""

from glob import glob
import os
import sys

# Only works for UNIXy style OSes.
# Find App Engine SDK
dev_appserver = None
DIR_PATH = ""
for d in os.environ["PATH"].split(":"):
    dev_appserver_path = os.path.join(d, "dev_appserver.py")
    if os.path.isfile(dev_appserver_path):
        DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(dev_appserver_path)))
        sys.path.append(DIR_PATH)
        import dev_appserver
        sys.path.pop()


if not hasattr(sys, 'version_info'):
    sys.stderr.write('Very old versions of Python are not supported. Please '
                     'use version 2.5 or greater.\n')
    sys.exit(1)
version_tuple = tuple(sys.version_info[:2])

if version_tuple != (2, 5) and version_tuple != (2, 7):
    sys.stderr.write('Warning: Python %d.%d is not supported. Please use '
                     'version 2.5 or 2.7.\n' % version_tuple)

if not DIR_PATH:
    sys.stderr.write("Could not find SDK path.  Make sure dev_appserver.py is in your PATH")
    sys.exit(1)

# local 'helper' scripts
SCRIPT_DIR = os.path.join(DIR_PATH, 'google', 'appengine', 'tools')

EXTRA_PATHS = dev_appserver.EXTRA_PATHS[:]
SUBSTRATE_PATHS = [
    os.path.join('.', 'lib', 'substrate'),
    os.path.join('.', 'local', 'substrate', 'lib'),
    os.path.join('.', 'local', 'substrate', 'manage'),
]
USR_PATHS = [
    os.path.join('.', 'lib', 'usr'),
    os.path.join('.', 'local', 'usr', 'lib'),
    os.path.join('.', 'local', 'usr', 'manage'),
]

COMMAND_FILE_PATTERN = '[a-z]*.py'
SUBSTRATE_COMMAND_DIR=os.path.join('.', 'local', 'substrate', 'manage', 'substrate_manage', 'commands')
USR_COMMAND_DIR=os.path.join('.', 'local', 'usr', 'manage', 'substrate_manage_usr', 'commands')


substrate_commands = []
usr_commands = []

def fix_sys_path():
    """Fix the sys.path to include our extra paths."""
    sys.path = EXTRA_PATHS + SUBSTRATE_PATHS + USR_PATHS + sys.path

def print_command_doc(cmd, cmd_width):
    doc = open(cmd).read().split('"""')[1]
    cmd_name = os.path.splitext(os.path.basename(cmd))[0]
    print "  ", cmd_name.ljust(cmd_width), "-" if doc else "" ,  doc or ""

def print_subcommand_overviews(substrate_commands, usr_commands):
    import logging
    logging.basicConfig(level=logging.ERROR)
    cmd_width = max(len(os.path.splitext(os.path.basename(command))[0]) 
                    for command in (substrate_commands + usr_commands))

    print "manage.py built-in commands: "
    for command in substrate_commands:
        print_command_doc(command, cmd_width)
    if usr_commands:
        print "manage.py project commands: "
        for command in usr_commands:
            print_command_doc(command, cmd_width)


def run_command(command, globals_, script_dir=SCRIPT_DIR):
    """Execute the file at the specified path with the passed-in globals."""
    fix_sys_path()
    global substrate_commands, usr_commands 
    substrate_commands = glob(os.path.join(SUBSTRATE_COMMAND_DIR, COMMAND_FILE_PATTERN))
    usr_commands = glob(os.path.join(USR_COMMAND_DIR, COMMAND_FILE_PATTERN))

    command_names = [os.path.splitext(os.path.basename(command))[0]  for command in substrate_commands + usr_commands]
    for arg in sys.argv:
        if arg in command_names:
            break
    else:
        print_subcommand_overviews(substrate_commands , usr_commands)
        sys.exit(1)
    command_idx = sys.argv.index(arg)
    script_name = sys.argv[command_idx]
    management_args = sys.argv[:command_idx]
    script_path = (glob(os.path.join(SUBSTRATE_COMMAND_DIR, arg + '.py')) 
            or glob(os.path.join(USR_COMMAND_DIR, arg + '.py')))[0]

    command_args = sys.argv[command_idx:]
    sys.argv = command_args
    execfile(script_path, globals_)


if __name__ == '__main__':
    run_command(__file__, globals())

