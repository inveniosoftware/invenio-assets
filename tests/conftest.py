# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

import shutil
import tempfile
from os import makedirs
from os.path import dirname, exists, join

import pytest
from flask import Blueprint, Flask
from flask.cli import ScriptInfo

from invenio_assets import InvenioAssets


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.yield_fixture()
def static_dir():
    """Static file directory."""
    static_dir = join(dirname(__file__), 'static')
    if not exists(static_dir):
        makedirs(static_dir)
    yield static_dir
    shutil.rmtree(static_dir)


@pytest.yield_fixture()
def testcss(static_dir):
    """Test CSS file."""
    filepath = join(static_dir, 'test.css')
    with open(filepath, 'w') as fp:
        fp.write('* {color: white;}')
    yield filepath


@pytest.yield_fixture()
def app(instance_path):
    """Flask application fixture."""
    app = Flask(
        __name__,
        instance_path=instance_path,
        static_folder=join(instance_path, 'static')
    )
    app.config.update({
        'COLLECT_STORAGE': 'flask_collect.storage.file',
    })

    yield app


@pytest.yield_fixture()
def script_info(app):
    """Get ScriptInfo object for testing CLI."""
    InvenioAssets(app)
    yield ScriptInfo(create_app=lambda info: app)


@pytest.yield_fixture()
def script_info_assets(app, static_dir, testcss):
    """Get ScriptInfo object for testing CLI."""
    InvenioAssets(app)

    blueprint = Blueprint(
        __name__, 'test_bp', static_folder=static_dir
    )

    class Ext(object):
        def __init__(self, app):
            assets = app.extensions['invenio-assets']
            app.register_blueprint(blueprint)

    Ext(app)

    yield ScriptInfo(create_app=lambda info: app)
