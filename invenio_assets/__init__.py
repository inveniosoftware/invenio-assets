# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Media assets management for Invenio.

Invenio-Assets helps you with integration of webassets, installation of NPM
packages, and process of collecting static files.

Initialization
--------------
First create a Flask application:

    >>> from flask import Flask
    >>> app = Flask('myapp')

Next, initialize your extension:

    >>> from invenio_assets import InvenioAssets
    >>> assets = InvenioAssets(app)

During initialization two Flask extensions
:class:`flask_webpackext.ext.FlaskWebpackExt` and
:class:`flask_collect.Collect` are instantiated and configured.

Bundles specified in the entry point groups called ``invenio_assets.webpack``
are automatically registered by Invenio-Assets.

.. _use-flask-webpackext:

Using Flask-WebpackExt
----------------------

Bundles
~~~~~~~
The `Flask-WebpackExt <https://flask-webpackext.readthedocs.io/en/latest/>`_
package provides a class
:class:`flask_webpackext.bundle.WebpackBundle` for declaring the needed
assets and NPM dependencies of each one of your modules.

.. code-block:: python

    from flask_webpackext import WebpackBundle
    bundle1 = WebpackBundle(
        __name__,
        './modules/module1/static',
        entry={
            'module1-app': './js/module1-app.js',
        },
        dependencies={
            'jquery': '^3.2.1'
        }
    )

The NPM dependencies defined in the bundles will be used to generate the
``package.json`` file.

Entry points loading
++++++++++++++++++++

Invenio-Assets will automatically load bundles defined by the entry point
group ``invenio_assets.webpack``. Example:

.. code-block:: python

   # setup.py
   setup(
       # ...
       entry_points={
           'invenio_assets.webpack': [
               'mybundle = mypackage.bundles:mybundle',
           ],
           # ...
        }
        # ...
    )

Command-line interface
~~~~~~~~~~~~~~~~~~~~~~

We can now build the assets:

.. code-block:: console

    $ flask webpack buildall

The command will copy all files from the src folder to the application
instance folder designated for the Webpack project, download the npm packages
and run Webpack to build our assets.

Alternatively, we can execute each build step separately with the following
flask webpack commands:

    * ``create`` - Copy all sources to the working directory.
    * ``install`` - Run npm install command and download all dependencies.
    * ``build`` - Run npm run build.

Additionally if we have some static files we should collect them:

.. code-block:: console

    $ flask collect -v
"""

from .ext import InvenioAssets
from .proxies import current_assets
from .version import __version__

__all__ = (
    '__version__',
    'InvenioAssets',
    'current_assets',
)
