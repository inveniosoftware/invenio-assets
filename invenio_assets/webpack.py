# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default Webpack project for Invenio."""

import os
from collections import OrderedDict, defaultdict

import pkg_resources
from flask import current_app, request
from flask_webpackext import WebpackBundle, WebpackBundleProject
from flask_webpackext.manifest import JinjaManifest, JinjaManifestLoader
from markupsafe import Markup
from pywebpack import ManifestEntry, UnsupportedExtensionError, bundles_from_entry_point


def _load_ep(ep):
    mod = ep.load()
    return mod() if callable(mod) else mod


def theme_bundles_from_entry_point(group):
    """Load bundles from entry point group."""

    # TODO: refactor this to minimize code duplication done for entries/aliases
    def _bundle_gen():
        entry_themes = defaultdict(dict)
        aliases_themes = defaultdict(dict)
        bundles = {
            ep.name: _load_ep(ep)
            for ep in pkg_resources.iter_entry_points(group)
        }
        for name, b in bundles.items():
            if isinstance(b, WebpackThemeBundle):
                for theme, theme_bundle in b.themes.items():
                    for entry, path in theme_bundle.entry.items():
                        entry_themes[entry][theme] = (name, path)
                        if theme == b.default:
                            # Store the default entry using the `None` key
                            entry_themes[entry][None] = (name, path)
                    for alias, path in theme_bundle.aliases.items():
                        aliases_themes[alias][theme] = (name, path)
                        if theme == b.default:
                            # Store the default alias using the `None` key
                            aliases_themes[alias][None] = (name, path)

            else:
                for entry, path in b.entry.items():
                    # Store the default entry using the `None` key
                    entry_themes[entry][None] = (name, path)

                for alias, path in b.aliases.items():
                    # Store the default aliases using the `None` key
                    aliases_themes[alias][None] = (name, path)

        result = {}
        result_aliases = {}
        app_themes = current_app.config.get('APP_THEME', [])
        if not app_themes:
            result = {
                # Just pick the default entry
                entry: themes[None]
                for entry, themes in entry_themes.items()
            }
            result_aliases = {
                # Just pick the default alias
                alias: themes[None]
                for alias, themes in aliases_themes.items()
            }
        else:
            for entry, themes in entry_themes.items():
                for theme in app_themes:
                    if theme in themes:
                        result[entry] = (theme, *themes[theme])
                        break
                if entry not in result and None in themes:
                    result[entry] = (None, *themes[None])

            for alias, themes in aliases_themes.items():
                for theme in app_themes:
                    if theme in themes:
                        result_aliases[alias] = (theme, *themes[theme])
                        break
                if alias not in result_aliases and None in themes:
                    result[alias] = (None, *themes[None])

        for name, b in bundles.items():
            entries_to_remove = []
            for entry in b.entry:
                if entry in result:
                    theme, res_name, path = result[entry]
                    if name != res_name:
                        entries_to_remove.append(entry)
            for entry in entries_to_remove:
                del b.entry[entry]

            aliases_to_remove = []
            for alias in b.aliases:
                if alias in result_aliases:
                    theme, res_name, path = result_aliases[alias]
                    if name != res_name:
                        aliases_to_remove.append(alias)
            for alias in aliases_to_remove:
                del b.aliases[alias]

        for b in bundles.values():
            yield b

    return (b for b in _bundle_gen())


project = WebpackBundleProject(
    __name__,
    project_folder='assets',
    config_path='build/config.json',
    bundles=theme_bundles_from_entry_point('invenio_assets.webpack'),
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
    def aliases(self):
        """Proxy to the active theme's bundle aliases."""
        return self._active_theme_bundle.aliases


    @property
    def dependencies(self):
        """Proxy to the active theme's bundle dependencies."""
        return self._active_theme_bundle.dependencies


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
