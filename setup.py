import os
import re
from setuptools import setup, find_packages
from shutil import copytree, rmtree


def package_data():
    """
    package_data is incredibly stupid and no wildcard can match a
    directory or it will break. This provides a list of all files in
    the data directory to circumvent that.
    """

    this_dir, this_filename = os.path.split(os.path.abspath(__file__))
    data_dir = os.path.join(this_dir, "substrate", "data")
    data_dir_prefix = os.path.dirname(data_dir)

    data = []

    for root, dirs, files in os.walk(data_dir):
        for f in files:
            path_without_prefix = os.path.join(root, f)[len(data_dir_prefix) + 1:]
            data.append(path_without_prefix)

    return data


def build():
    root_dir, this_filename = os.path.split(__file__)
    app_dir = os.path.join(root_dir, "app")
    data_dir = os.path.join(root_dir, "substrate", "data")

    if os.path.exists(data_dir):
        rmtree(data_dir)

    copytree(app_dir, data_dir)


def extract_version():
    """
    Find the version without importing the package. Via zooko:
    http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package/7071358#7071358
    """

    version_str_line = open("substrate/_version.py", "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, version_str_line, re.M)
    if mo:
        version = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in substrate/_version.py.")

    return version

build()
setup(name='substrate',
      version=extract_version(),
      description='A base application with a collection of libraries for making Google App Engine development easier.',
      long_description=open("README.rst").read(),
      license="MIT",
      author='Thomas Bohmbach, Jr.',
      author_email='thomas@gumption.com',
      url='http://bitbucket.org/gumptioncom/substrate',
      zip_safe=False,
      packages=find_packages(exclude=['tests', 'tests.*']),
      package_data={'': package_data()},
      scripts=['bin/substrate'],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License"
          ]
      )
