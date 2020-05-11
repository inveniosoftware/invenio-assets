# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default Webpack project for Invenio."""

from __future__ import absolute_import, print_function

import os

project = WebpackBundleProject(
    __name__,
    project_folder='assets',
    config_path='build/config.json',
    bundles=bundles_from_entry_point('invenio_assets.webpack'),
)


class WebpackThemeBundle(object):
    """Webpack themed bundle."""

    def __init__(self, import_name, folder, default=None, themes=None):
        """Initialize webpack bundle.

        :param import_name: Name of the module where the WebpackBundle class
            is instantiated.
        :param folder: Relative path to the assets.
        :param default: The default theme to be used when ``APP_THEME`` is not
            set.
        :param themes: Dictionary where the keys are theme names and the values
            are the keyword arguments passed to the ``WebpackBundle`` class.

        """
        assert default and default in themes
        self.default = default
        self.themes = {}
        for theme, bundle in themes.items():
            self.themes[theme] = WebpackBundle(
                import_name,
                os.path.join(folder, theme),
                **bundle
            )

    @property
    def _active_theme_bundle(self):
        themes = current_app.config.get('APP_THEME', [])
        if not themes:
            return self.themes[self.default]
        for theme in themes:
            if theme in self.themes:
                return self.themes[theme]

    @property
    def path(self):
        """Proxy to the active theme's bundle path."""
        return self._active_theme_bundle.path

    @property
    def entry(self):
        """Proxy to the active theme's bundle entry."""
        return self._active_theme_bundle.entry

    @property
    def dependencies(self):
        """Proxy to the active theme's bundle dependencies."""
        return self._active_theme_bundle.dependencies

