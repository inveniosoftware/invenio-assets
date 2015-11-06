# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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

"""Media asset management for Invenio."""

from __future__ import absolute_import, print_function

import pkg_resources
from flask_assets import Environment
from flask_collect import Collect

from .cli import assets as assets_cmd
from .cli import bower, collect


class InvenioAssets(object):
    """Invenio asset extension."""

    def __init__(self, app=None, entrypoint='invenio_assets.bundles',
                 **kwargs):
        """Extension initialization."""
        self.env = Environment()
        self.collect = Collect()
        self.entrypoint = entrypoint

        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        """Initialize application object."""
        self.init_config(app)
        self.env.init_app(app)
        self.collect.init_app(app)
        self.init_cli(app.cli)
        if self.entrypoint:
            self.load_entrypoint(self.entrypoint)
        app.extensions['invenio-assets'] = self

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault("REQUIREJS_BASEURL", app.static_folder)
        app.config.setdefault('COLLECT_STATIC_ROOT', app.static_folder)
        app.config.setdefault('COLLECT_STORAGE', 'flask_collect.storage.link')

    def init_cli(self, cli):
        """Initialize CLI."""
        cli.add_command(assets_cmd)
        cli.add_command(bower)
        cli.add_command(collect)

    def load_entrypoint(self, entrypoint):
        """Load entrypoint."""
        for ep in pkg_resources.iter_entry_points(entrypoint):
            self.env.register(ep.name, ep.load())
