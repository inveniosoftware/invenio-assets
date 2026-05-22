..
    SPDX-FileCopyrightText: 2015-2020 CERN.
    SPDX-License-Identifier: MIT

Configuration
=============

Default values are set for following configuration variables:

* ``COLLECT_STATIC_ROOT`` - path to folder where static files will be
  collected to (see
  `Flask-Collect <http://flask-collect.readthedocs.io/en/latest/config.html>`_
  for details). Default: ``app.static_folder``.
* ``COLLECT_STORAGE`` - import path to Flask-Collect storage implementation
  (see
  `Flask-Collect <http://flask-collect.readthedocs.io/en/latest/config.html>`_
  for details). Default: ``'flask_collect.storage.link'`` (i.e. symlinking of
  files from source code into ``COLLECT_STATIC_ROOT``).

Note, normally in a production environment you should change
``COLLECT_STORAGE`` to ``flask_collect.storage.file`` in order to copy files
instead of symlinking them.

For Webpack related configuration please see `Flask-WebpackExt
<https://flask-webpackext.readthedocs.io/en/latest/configuration.html>`_
