Changes
-------
* **0.7** -- 2012-09-10

  * Updated to `agar-0.7.1`

* **0.7** -- 2012-09-09

  * Changed project status from Alpha to Beta

  * Remove support for python older than 2.7

  * Renamed substrate script to back to substrate

  * Updated to `agar-0.7`_. See `agar CHANGES`_ for more information.

  * Added mysql params to shell to support cloud sql (local mysql)

  * Updated to restler 0.3

* **0.6** -- 2012-01-01

  * First support for py2.7

  * Renamed substrate script to substrate-2.5 and substrate-2.7

  * Updated to `agar-0.6`_. See `agar CHANGES`_ for more information.

  * Added django template rendering using agar templatetags to demo app

  * Added command line parameters to the 'shell' command to allow setting the local data directories.

* **0.5.1** -- 2011-11-22

  * Updated to `agar-0.5.1`_. See `agar CHANGES`_ for more information.

  * Moved manage commands to new package structure. Project specific commands should go in
    ``local/usr/manage/substrate_manage_usr/commands/``. The substrate ``update`` command has been modified to move
    ``local/usr/manage/commands/`` to ``local/usr/manage/substrate_manage_usr/commands/``.

* **0.5** -- 2011-11-15

  * Updated to `agar-0.5`_. See `agar CHANGES`_ for more information.

  * Fixed the ``shell`` command so that it uses the same local datastore as the ``dev_appserver`` command default.

  * Split the contents of ``lib/`` into ``lib/substrate`` and ``lib/usr``. Project specific libraries should go in
    ``lib/usr``. The substrate ``update`` command has been modified to move the contents of ``lib`` to the appropriate
    locations.

  * Split and relocated the contents of ``local/lib`` into ``local/substrate/lib`` and ``local/usr/lib``. Project
    specific local libraries should go in ``local/usr/lib``. The substrate ``update`` command has been modified to
    move the contents of ``local/lib`` to the appropriate locations.

  * Split and relocated the contents of ``local/commands`` into ``local/substrate/manage/commands`` and
    ``local/usr/manage/commands``. Project specific commands should go in ``local/usr/manage/commands``.
    The substrate ``update`` command has been modified to move the contents of ``local/commands`` to
    ``local/substrate/manage/commands``.

* **0.4** -- 2011-11-08

  * Updated `WebTest`_ to version 1.3.1

  * Updated to `agar-0.4`_. **This includes break fixes.** See `agar CHANGES`_ for more information.

  * Fix SDK 1.6 changes to ``dev_appserver.LoadAppConfig()``.

* **0.2** (First Public Release) -- 2011-10-14

  * Updated docs

* **0.1** (Development Version Only) -- 2011-09-21


.. Links

.. _WebTest: http://webtest.pythonpaste.org/

.. _agar-0.4: http://pypi.python.org/pypi/agar/0.4
.. _agar CHANGES: http://packages.python.org/agar/changes.html
.. _agar-0.5: http://pypi.python.org/pypi/agar/0.5
.. _agar-0.5.1: http://pypi.python.org/pypi/agar/0.5.1
.. _agar-0.6: http://pypi.python.org/pypi/agar/0.6
.. _agar-0.7: http://pypi.python.org/pypi/agar/0.7
