""" Perform application deployment on App Engine.

This script does the following:
 - Ensure the working directory is on the default branch with no local changes.
 - Determine a version string for the current source code based on the hg revision ID
 - Update version setting in snapdeploy.yaml
 - Deploy to App Engine via appcfg.py
 - Notify user that he/she must commit/push the snapdeploy.yaml changes.

By automating these steps, the aim is to reduce human error where the person deploying forgets to bump the version
number in snapdeploy.yaml/app.yaml so that the versions deployed to app engine have consistent names.  This allows
versions to be tracked so that the exact same version that gets deployed/tested on Int can later be pushed to Stage.


Usage:

    python manage.py snapdeploy [options for appcfg.py ...]

Any number of options can be specified and are passed as-is to 'appcfg.py update'. For example:

    python manage.py snapdeploy -A proactiveservices-stage --oauth2


Older versions may be redeployed in a deterministic manner.  To do so, update your working directory to the desired
changeset ID (which can be found by looking at the right-hand side of a version string, such as in "34-4db0243959fa"),
make sure there are no local changes, and run the script in exactly the same manner.  snapdeploy.yaml will be updated
with the appropriate version number, but since the snapdeploy.yaml changes were already committed they can safely be
discarded when you reset your working directory to tip.
"""
import re
import sys
import argparse
import subprocess
from subprocess import Popen, PIPE
from collections import namedtuple
import yaml
import os

CONFIG_FILE = 'snapdeploy.yaml'
GIT_PATH = ".git"
HG_PATH = ".hg"
VC_TYPE_GIT = "git"
VC_TYPE_HG = "hg"

parser = argparse.ArgumentParser(description='Perform application deployment on App Engine.',
    epilog='Any additional arguments are passed verbatim to appcfg.py')
parser.add_argument('-V', dest='version', help='override version setting in snapdeploy.yaml')
parser.add_argument('--ignore-unclean', action='store_true', help='ignore dirty workarea')
parser.add_argument('--ignore-branch', action='store_true', help='allow deploy from any branch')

ChangesetInfo = namedtuple('ChangesetInfo', ['branch', 'hash', 'dirty'])


def git_get_current_changeset_info(vc_type):
    proc = Popen(["git", "branch", "--color=never"], stdout=PIPE)
    proc2 = Popen(["git", "rev-parse", "HEAD"], stdout=PIPE)
    proc3 = Popen(["git", "status", "--porcelain"], stdout=PIPE)

    match = re.search('\\* (.*)\n', proc.communicate()[0])
    if match is None:
        print("Unrecognized 'git branch' output")
        sys.exit(1)
    branch = match.group(1)
    hash = proc2.communicate()[0].strip()[:10]
    dirty = len(proc3.communicate()[0].split('\n')) != 1

    return ChangesetInfo(branch=branch, hash=hash, dirty=dirty)


def git_revert_file(filename):
    Popen(["git", "checkout", "--", filename]).wait() == 0


def hg_get_current_changeset_info(vc_type):
    proc = Popen(["hg", "branch"], stdout=PIPE)
    branch = proc.communicate()[0].rstrip()
    proc2 = Popen(["hg", "id", "-i"], stdout=PIPE)
    id_text = proc2.communicate()[0].rstrip()

    if proc.returncode != 0 or proc2.returncode != 0:
        branch = None
        hash = None
        dirty = False
    elif id_text[-1] == '+':
        branch = branch
        hash = id_text[:-1]
        dirty = True
    else:
        branch = branch
        hash = id_text
        dirty = False
    return ChangesetInfo(branch=branch, hash=hash, dirty=dirty)


def hg_revert_file(filename):
    return Popen(['hg', 'revert', './{}'.format(filename)], stdout=PIPE).wait() == 0


def get_version_control_type():
    # Figure out what type of vc is being used.
    if os.path.exists(GIT_PATH) == True:
        vc_type = VC_TYPE_GIT
    elif os.path.exists(HG_PATH) == True:
        vc_type = VC_TYPE_HG

    return vc_type


def get_current_changeset_info(vc_type):
    if vc_type == VC_TYPE_HG:
        return hg_get_current_changeset_info(vc_type)
    else:
        return git_get_current_changeset_info(vc_type)


def revert_file(vc_type, filename):
    if vc_type == VC_TYPE_HG:
        hg_revert_file(filename)
    else:
        git_revert_file(filename)


def get_default_branch_name(vc_type):
    if vc_type == VC_TYPE_HG:
        return 'default'
    else:
        return 'master'


def make_default_config():
    return {'module_yaml_files': ['app.yaml']}


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.load(f.read())
    else:
        config = make_default_config()
    if 'module_yaml_files' not in config:
        config['module_yaml_files'] = ['app.yaml']
    return config


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        f.write(yaml.dump(config, default_flow_style=False))


if __name__ == "__main__":
    args = parser.parse_known_args(sys.argv[1:])
    vc_type = get_version_control_type()
    if vc_type is None:
        print("No version control detected. Snapdeploy requires the use of Git or Mercurial.")
        sys.exit(1)

    changeset_info = get_current_changeset_info(vc_type)
    default_branch_name = get_default_branch_name(vc_type)
    if changeset_info.hash is None:
        print('Failed to find changeset info; aborting...')
        sys.exit(1)
    if not args[0].ignore_branch and changeset_info.branch != default_branch_name:
        print('Must be on {} branch in order to deploy (or use --ignore-branch).'.format(default_branch_name))
        sys.exit(1)
    if not args[0].ignore_unclean and changeset_info.dirty:
        print('The working directory is dirty; please shelve changes before deploying (or use --ignore-unclean).')
        sys.exit(1)

    config = load_config()

    if 'version' in config:
        old_version = str(config['version'])
        print('Previously deployed version: {}'.format(old_version))
        if re.match('\d+$', old_version):
            new_version = int(old_version) + 1
        else:
            new_version = old_version
    else:
        old_version = None
        new_version = 1
    if args[0].version is not None:
        new_version = args[0].version

    if 'pre-deploy-script' in config:
        if subprocess.call(config['pre-deploy-script'], shell=True) != 0:
            print('Pre-deploy script failed; aborting deployment...')
            sys.exit(1)

    if new_version != old_version:
        config['version'] = new_version
        config['hash'] = changeset_info.hash
        save_config(config)

    full_version = '{}-{}'.format(new_version, changeset_info.hash)
    print('New version: {}'.format(full_version))

    print('=== Deploying...')
    for yaml_filename in config['module_yaml_files'] + ['.']:
        if subprocess.call(['appcfg.py', 'update', yaml_filename] + args[1] + ['-V', '{}'.format(full_version)]) != 0:
            print('Deployment failed!')
            revert_file(vc_type, 'snapdeploy.yaml')
            sys.exit(1)

    print("=== Output of '{} status':".format(vc_type))
    cmd_output = Popen(['{}'.format(vc_type), 'status'], stdout=PIPE).communicate()[0]
    print(cmd_output)

    print("=== Output of '{} diff {}':".format(vc_type, CONFIG_FILE))
    cmd_output = Popen(['{}'.format(vc_type), 'diff', 'snapdeploy.yaml'], stdout=PIPE).communicate()[0]
    print(cmd_output)

    print('YOUR WORK IS NOT DONE YET, HUMAN.  YOUR NEXT ASSIGNMENT IS AS FOLLOWS:')
    if new_version != old_version:
        print(" - Run '{} commit' and '{} push' to save snapdeploy.yaml changes.".format(vc_type, vc_type))
    print(" - Make version '{}' the default version on app engine console (https://appengine.google.com).".format(full_version))

    # Direct web browser to version management page on app engine console.
    #Popen(['open', 'https://appengine.google.com/deployment?&app_id=s~{}'.format(APPLICATION_ID)])

