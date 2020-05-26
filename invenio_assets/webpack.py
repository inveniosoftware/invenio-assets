# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default Webpack project for Invenio."""

import os
from collections import OrderedDict

from flask import current_app, request
from flask_webpackext import WebpackBundle, WebpackBundleProject
from flask_webpackext.manifest import JinjaManifest, JinjaManifestLoader
from markupsafe import Markup
from pywebpack import ManifestEntry, UnsupportedExtensionError, \
    bundles_from_entry_point

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

    def __getattr__(self, attr):
        """Proxy all attributes to the active theme bundle."""
        try:
            return getattr(self._active_theme_bundle, attr)
        except RuntimeError:
            raise AttributeError(
                '{}.{} is invalid because you are working outside an '
                'application context.'.format(self.__class__.__name__, attr)
            )


class UniqueJinjaManifestEntry(ManifestEntry):
    """Manifest entry which avoids double output of chunks."""

    def __html__(self):
        """Output chunk HTML tags that haven't been yet output."""
        if not hasattr(request, '_jinja_webpack_entries'):
            setattr(request, '_jinja_webpack_entries', {
                '.js': OrderedDict(),
                '.css': OrderedDict(),
            })

        output = []

        # For debugging add from which entry the chunk came
        if current_app.debug:
            output.append('<!-- {} -->'.format(self.name))
        for p in self._paths:
            _, ext = os.path.splitext(p.lower())
            # If we haven't come across the chunk yet, we add it to the output
            if ext not in request._jinja_webpack_entries:
                raise UnsupportedExtensionError(p)
            if p not in request._jinja_webpack_entries[ext]:
                tpl = self.templates.get(ext)
                if tpl is None:
                    raise UnsupportedExtensionError(p)
                output.append(tpl.format(p))

            # Mark the we have already output the chunk
            request._jinja_webpack_entries[ext][p] = None
        return Markup('\n'.join(output))


class UniqueJinjaManifestLoader(JinjaManifestLoader):
    """Factory which uses the Jinja manifest entry."""

    def __init__(self, manifest_cls=JinjaManifest,
                 entry_cls=UniqueJinjaManifestEntry):
        """Initialize manifest loader."""
        super(UniqueJinjaManifestLoader, self).__init__(
            manifest_cls=manifest_cls,
            entry_cls=entry_cls
        )
