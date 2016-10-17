# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

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

During initalization two Flask extensions ``flask_assets.Environment`` and
:class:`flask_collect.Collect` are instantiated and configured. Also bundles
specified in entry point group called `'invenio_assets.bundles'` are
:ref:`automatically registered <entry-points-loading>`.

Bundles
-------
Webassets package provides class ``Bundle`` for creating collection of files
that you would like to process together by applying filters. For more
information follow `webassets documentation
<https://webassets.readthedocs.io/en/latest/bundles.html#bundles>`_.

Registering bundles
~~~~~~~~~~~~~~~~~~~
After having initialized the extension you can register bundles:

    >>> from webassets import Bundle
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

To extract the dependencies from the bundle use
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

.. code-block:: console

   $ inveniomanage npm -o package.json
   $ npm install
   $ inveniomanage assets build
   $ inveniomanage collect

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
