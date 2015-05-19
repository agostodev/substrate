.. Substrate documentation master file, created by
   sphinx-quickstart on Fri May 20 23:04:53 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Substrate Documentation
=======================

Substrate is a base application and set of libraries for making
`Google App Engine python`_ development easier. It includes a base app with management
script, testing already set up, a set of common helper functions
(:ref:`agar`), and a serialization library (:ref:`restler`). It also comes with
common libraries like `webapp2`_ and `pytz`_ ready to go.

Substrate is based on best practices for `Google App Engine python`_ learned in
developing several real-world applications with many users.

We are tired of seeing App Engine frameworks languish unsupported. For
that reason, Substrate is **NOT** a framework. It is a base
application with a set of libraries and helpers. No more, no less.

Resources
---------

* `Documentation`_
* `PyPI Package`_
* `Bitbucket Mercurial Repository`_

License
-------

Substrate is mostly a packaging of other libraries, which have their
own licenses. Original code in Substrate is under the `MIT License`_.

Contents
--------

.. toctree::
   :maxdepth: 2

   changes
   substrate
   env_setup
   appengine_config
   agar
   restler

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. Links

.. _PyPI Package: http://pypi.python.org/pypi/substrate
.. _Bitbucket Mercurial Repository: http://bitbucket.org/gumptioncom/substrate
.. _Documentation: http://packages.python.org/substrate

.. _Google App Engine python: http://code.google.com/appengine/docs/python/overview.html

.. _webapp2: http://code.google.com/p/webapp-improved/

.. _pytz: http://pytz.sourceforge.net/

.. _MIT License: http://www.opensource.org/licenses/mit-license.php
