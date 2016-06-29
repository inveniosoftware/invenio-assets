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

First make sure you have Flask application with Click support (meaning
Flask 0.11+ or alternatively use the Flask-CLI extension):

    >>> from flask import Flask
    >>> app = Flask('myapp')
    >>> if not hasattr(app, 'cli'):
    ...     from flask_cli import FlaskCLI
    ...     FlaskCLI(app)

Next, initialize your extension:

    >>> from invenio_assets import InvenioAssets
    >>> assets = InvenioAssets(app)


Registering bundles
~~~~~~~~~~~~~~~~~~~
After having initialized the extension you can register bundles:

    >>> from webassets import Bundle
    >>> assets.env.register('mybundle', Bundle())
    <Bundle ...>


Command-line interface
~~~~~~~~~~~~~~~~~~~~~~
Invenio Assets installs three commands on your application:

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
from .filters import CleanCSSFilter, RequireJSFilter
from .npm import NpmBundle
from .proxy import current_assets
from .version import __version__

__all__ = (
    '__version__', 'CleanCSSFilter', 'InvenioAssets', 'NpmBundle',
    'RequireJSFilter', 'current_assets')
