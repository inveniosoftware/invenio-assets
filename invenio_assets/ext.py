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

"""Media asset management for Invenio."""

from __future__ import absolute_import, print_function

from functools import partial

import pkg_resources
from flask_assets import Environment
from flask_collect import Collect

from .collect import collect_staticroot_removal

__all__ = ('InvenioAssets', )


class InvenioAssets(object):
    """Invenio asset extension."""

    def __init__(self, app=None, **kwargs):
        r"""Extension initialization.

        :param app: An instance of :class:`~flask.Flask`.
        :param \**kwargs: Keyword arguments are passed to ``init_app`` method.
        """
        self.env = Environment()
        self.collect = Collect()

        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, entry_point_group='invenio_assets.bundles',
                 **kwargs):
        """Initialize application object.

        :param app: An instance of :class:`~flask.Flask`.
        :param entry_point_group: A name of entry point group used to load
            ``webassets`` bundles.

        .. versionchanged:: 1.0.0b2
           The *entrypoint* has been renamed to *entry_point_group*.
        """
        self.init_config(app)
        self.env.init_app(app)
        self.collect.init_app(app)

        if entry_point_group:
            self.load_entrypoint(entry_point_group)
        app.extensions['invenio-assets'] = self

    def init_config(self, app):
        """Initialize configuration.

        :param app: An instance of :class:`~flask.Flask`.
        """
        app.config.setdefault('REQUIREJS_BASEURL', app.static_folder)
        app.config.setdefault('COLLECT_STATIC_ROOT', app.static_folder)
        app.config.setdefault('COLLECT_STORAGE', 'flask_collect.storage.link')
        app.config.setdefault(
            'COLLECT_FILTER', partial(collect_staticroot_removal, app))

    def load_entrypoint(self, entry_point_group):
        """Load entrypoint.

        :param entry_point_group: A name of entry point group used to load
            ``webassets`` bundles.

        .. versionchanged:: 1.0.0b2
           The *entrypoint* has been renamed to *entry_point_group*.
        """
        for ep in pkg_resources.iter_entry_points(entry_point_group):
            self.env.register(ep.name, ep.load())
