# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test Webpack module."""

import pytest
from flask_webpackext import WebpackBundle
from pywebpack import UnsupportedExtensionError

from invenio_assets.webpack import UniqueJinjaManifestEntry, \
    UniqueJinjaManifestLoader, WebpackThemeBundle


def test_webpack_theme_bundle_outside_app():
    """Access a bundle property outside app context."""
    # Test that bundles are created for each theme.
    bundle = WebpackThemeBundle(
        'tests',
        'assets',
        default='semantic-ui',
        themes={
            'semantic-ui': dict(
                entry={
                    'theme': './theme-semantic-ui.css',
                }
            ),
        }
    )
    pytest.raises(AttributeError, getattr, bundle, 'path')


def test_webpack_theme_bundle(app):
    """Test WebpackThemeBundle."""
    themes = {
        'bootstrap3': dict(
            entry={
                'theme': './theme-bootstrap3.css',
            }
        ),
        'semantic-ui': dict(
            entry={
                'theme': './theme-semantic-ui.css',
            }
        ),
    }

    # Test that bundles are created for each theme.
    bundle = WebpackThemeBundle(
        'tests', 'assets', default='semantic-ui', themes=themes)
    assert isinstance(bundle.themes['bootstrap3'], WebpackBundle)
    assert isinstance(bundle.themes['semantic-ui'], WebpackBundle)

    # Test that default theme is used.
    with app.app_context():
        assert bundle._active_theme_bundle == bundle.themes['semantic-ui']
        assert bundle.path == bundle.themes['semantic-ui'].path
        assert bundle.entry == bundle.themes['semantic-ui'].entry
        assert bundle.dependencies == bundle.themes['semantic-ui'].dependencies

    # Test that APP_THEME overrides default theme.
    app.config['APP_THEME'] = ['bootstrap3']
    with app.app_context():
        assert bundle._active_theme_bundle == bundle.themes['bootstrap3']
        assert bundle.path == bundle.themes['bootstrap3'].path
        assert bundle.entry == bundle.themes['bootstrap3'].entry
        assert bundle.dependencies == bundle.themes['bootstrap3'].dependencies

    # Test that an invalid APP_THEME
    app.config['APP_THEME'] = ['invalid']
    with app.app_context():
        assert bundle._active_theme_bundle is None


def test_unique_jinja_manifest_entry(app):
    """Test UniqueJinjaManifestEntry."""
    # b.js is only output once, despite being twice in manifest
    m = UniqueJinjaManifestEntry('manifestname', ['/a.js', '/b.js', '/b.js'])
    with app.test_request_context():
        assert m.__html__() == \
            '<script src="/a.js"></script>\n' \
            '<script src="/b.js"></script>'

    # b.js is only output once, despite being twice in manifest
    app.debug = True
    with app.test_request_context():
        assert m.__html__() == \
            '<!-- manifestname -->\n' \
            '<script src="/a.js"></script>\n' \
            '<script src="/b.js"></script>'

    # Unsupported file extension
    m = UniqueJinjaManifestEntry('script', ['/a.less'])
    with app.test_request_context():
        pytest.raises(UnsupportedExtensionError, m.__html__)


def test_unique_jinja_manifest_loader(app):
    """Test UniqueJinjaManifestLoader."""
    loader = UniqueJinjaManifestLoader()
    assert loader.entry_cls == UniqueJinjaManifestEntry
