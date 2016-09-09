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

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import shutil
import tempfile
from os import makedirs
from os.path import dirname, exists, join

import pytest
from flask import Blueprint, Flask
from flask.cli import ScriptInfo

from invenio_assets import InvenioAssets
from invenio_assets.npm import NpmBundle


@pytest.yield_fixture()
def instance_path():
    """Instance path."""
    instance_path = tempfile.mkdtemp()

    yield instance_path

    shutil.rmtree(instance_path)


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
            assets.env.register(
                'testbundle',
                NpmBundle('test.css', output='testbundle.css')
            )
            app.register_blueprint(blueprint)

    Ext(app)

    yield ScriptInfo(create_app=lambda info: app)
