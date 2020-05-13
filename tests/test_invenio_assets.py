# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Test Invenio Assets module."""

from mock import patch
from pywebpack.storage import FileStorage, LinkStorage

from invenio_assets import InvenioAssets


def test_version():
    """Test version import."""
    from invenio_assets import __version__
    assert __version__


def test_init(app):
    """Test module initialization."""
    InvenioAssets(app)
    assets = app.extensions['invenio-assets']
    assert assets.collect
    assert assets.webpack
    assert app.config['COLLECT_STATIC_ROOT'] == app.static_folder
    assert 'WEBPACKEXT_PROJECT' in app.config


def test_init_post(app):
    """Test module initialization using init_app."""
    assets = InvenioAssets()
    assert 'COLLECT_STATIC_ROOT' not in app.config
    assets.init_app(app)
    assert assets.collect
    assert assets.webpack
    assert 'COLLECT_STATIC_ROOT' in app.config
    assert 'WEBPACKEXT_PROJECT' in app.config
    assert app.config['WEBPACKEXT_STORAGE_CLS'] == FileStorage


def test_init_cli(app):
    """Test cli registration."""
    from flask.cli import cli
    cli._load_plugin_commands()
    assert 'collect' in cli.commands
    assert 'webpack' in cli.commands


def test_init_debug(app):
    """Test module initialization with debug enabled."""
    app.debug = True
    InvenioAssets(app)
    # Storage class changed to LinkStorage when in debug mode.
    assert app.config['WEBPACKEXT_STORAGE_CLS'] != FileStorage
