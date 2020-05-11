# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Media asset management for Invenio."""

from __future__ import absolute_import, print_function

from functools import partial

import pkg_resources
from flask_assets import Environment
from flask_collect import Collect
from flask_webpackext import FlaskWebpackExt

from .collect import collect_staticroot_removal
from .webpack import UniqueJinjaManifestLoader

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
        self.webpack = FlaskWebpackExt()

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
        self.webpack.init_app(app)

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

        # Flask-WebpackExt config
        app.config.setdefault(
            'WEBPACKEXT_PROJECT', 'invenio_assets.webpack:project')
        app.config.setdefault(
            'WEBPACKEXT_MANIFEST_LOADER', UniqueJinjaManifestLoader)
        if app.debug:  # for development use 2-level deep symlinking
            from pywebpack.storage import LinkStorage
            app.config.setdefault(
                'WEBPACKEXT_STORAGE_CLS', partial(LinkStorage, depth=2))

    def load_entrypoint(self, entry_point_group):
        """Load entrypoint.

        :param entry_point_group: A name of entry point group used to load
            ``webassets`` bundles.

        .. versionchanged:: 1.0.0b2
           The *entrypoint* has been renamed to *entry_point_group*.
        """
        for ep in pkg_resources.iter_entry_points(entry_point_group):
            self.env.register(ep.name, ep.load())
