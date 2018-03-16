# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Media assets management for Invenio.

Invenio-Assets helps you with integration of webassets, installation of NPM
packages, and process of collecting static files.

If you want to learn details about package dependencies, please see:

 * `Flask-Assets <https://flask-assets.readthedocs.io/en/latest/>`_
 * `Flask-Collect <https://flask-collect.readthedocs.io/en/latest/>`_
 * `NPM <https://nodejs.org/en/download/>`_

Initialization
--------------
First create a Flask application:

    >>> from flask import Flask
    >>> app = Flask('myapp')

Next, initialize your extension:

    >>> from invenio_assets import InvenioAssets
    >>> assets = InvenioAssets(app)

During initalization two Flask extensions :class:`flask_assets.Environment` and
:class:`flask_collect.Collect` are instantiated and configured. Also bundles
specified in the entry point group called ``invenio_assets.bundles`` are
:ref:`automatically registered <entry-points-loading>`.

Bundles
-------
The Flask-Assets package provides (via webassets) a class
:class:`flask_assets.Bundle` for creating collection of files that you would
like to process together by applying filters. For more information see the
`webassets documentation
<https://webassets.readthedocs.io/en/latest/bundles.html#bundles>`_.

Registering bundles
~~~~~~~~~~~~~~~~~~~
After having initialized the extension you can register bundles:

    >>> from flask_assets import Bundle
    >>> assets.env.register('mybundle', Bundle())
    <Bundle ...>

.. _entry-points-loading:

Entry points loading
~~~~~~~~~~~~~~~~~~~~
Invenio-Assets will automatically load bundles defined by the entry point
groups ``invenio_assets.bundles``.

Example:

.. code-block:: python

   # setup.py
   setup(
       # ...
       entry_points={
           'invenio_assets.bundles': [
               'mybundle = mypackage.bundles:mybundle',
           ],
           # ...
        }
        # ...
    )

Above is equivalent to:

.. code-block:: python

   from mypackage.bundles import mybundle
   assets.env.register('mybundle', mybundle)

NPM dependencies
~~~~~~~~~~~~~~~~
There is a special bundle extension where you can define NPM dependencies
used to generate ``package.json`` file:

    >>> from invenio_assets import NpmBundle
    >>> mycss = NpmBundle(
    ...     filters='scss, cleancss',
    ...     output='my.css',
    ...     npm={
    ...         'almond': '~0.3.1',
    ...         'bootstrap-sass': '~3.3.5',
    ...         'font-awesome': '~4.4.0',
    ...     }
    ... )
    >>> assets.env.register('mycss', mycss)
    <NpmBundle ...>

To extract the dependencies from the bundles use
:func:`~invenio_assets.npm.extract_deps` and pass an instance of webassets
environment:

    >>> from invenio_assets.npm import extract_deps
    >>> deps = extract_deps(assets.env)
    >>> deps['bootstrap-sass']
    '~3.3.5'

Command-line interface
----------------------
Invenio-Assets makes sure that following three Flask commands are available
on your application:

 * ``assets`` - Assets building commands.
 * ``npm`` - Generation of package.json.
 * ``collect`` - Collect static files.

Usually you use above commands to install and build your assets in the
following manner:

.. code-block:: console

   $ inveniomanage npm -o package.json
   $ npm install
   $ inveniomanage assets build
   $ inveniomanage collect


Customize RequireJS
-------------------

.. note::

   This section assumes prior working knowledge with RequireJS.


In more advanced use cases you may need to override the RequireJS configuration
in order to define e.g a custom shim config to integrate non-AMD ready modules
with RequireJS.

First overwrite the ``REQUIREJS_CONFIG`` config variable, so it points to your
new RequireJS config file. E.g. in your instance's ``config.py`` file:

.. code-block:: python

    # The RequireJS options file. The path is taken to be relative to
    # the Enviroment.directory (by defualt is /static).
    REQUIREJS_CONFIG = "js/myinstance-build.js"

Put your RequireJS config in the build file ``static/js/myinstance-build.js``:

.. code-block:: javascript

    ({
      preserveLicenseComments: false,
      optimize: 'uglify2',
      uglify2: {
        output: {
          beautify: false,
          comments: false
        },
        compress: {
          drop_console: true,
          sequences: true,
          dead_code: true,
          conditionals: true,
          booleans: true,
          unused: true,
          if_return: true,
          join_vars: true
        },
        warnings: true,
        mangle: true
      },
      mainConfigFile: ['./myinstance-settings.js']
    });

Note, that the build file specifies a new settings file
``myinstance-settings.js`` (path relative to build file).

Now, add your settings file ``static/js/myinstance-settings.js`` where you can
define the custom shims:

.. code-block:: javascript

    require.config({
      baseUrl: "/static/",
      paths: {
        angular: "node_modules/angular/angular"
      },
      shim: {
        angular: {
          exports: 'angular'
        }
      }
    });

That's all for the configuration. Now you can create a bundle that uses
RequireJS as a filter for a file ``myinstance.js`` like this:

.. code-block:: python

    js = NpmBundle(
        'js/myinstance.js',
        filters='requirejs',
        output="gen/myinstance.%(version)s.js",
        npm={
            'angular': '~1.4.9'
        }
    )

And then in your ``myinstance.js`` script that uses RequireJS:

.. code-block:: javascript

    require([
      "angular",
      ], function(angular) {
        // ....
      }
    );
"""

from __future__ import absolute_import, print_function

from .ext import InvenioAssets
from .filters import AngularGettextFilter, CleanCSSFilter, RequireJSFilter
from .glob import GlobBundle
from .npm import LazyNpmBundle, NpmBundle
from .proxies import current_assets
from .version import __version__

__all__ = (
    '__version__',
    'AngularGettextFilter',
    'CleanCSSFilter',
    'GlobBundle',
    'InvenioAssets',
    'LazyNpmBundle',
    'NpmBundle',
    'RequireJSFilter',
    'current_assets',
)
