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

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile

import pytest
from flask import Flask
from flask_cli import FlaskCLI, ScriptInfo

from invenio_assets import InvenioAssets
from invenio_assets.npm import NpmBundle


@pytest.fixture()
def app():
    """Flask application fixture."""
    app = Flask(__name__)
    FlaskCLI(app)
    return app


@pytest.fixture()
def script_info(request):
    """Get ScriptInfo object for testing CLI."""
    initial_dir = os.getcwd()
    instance_path = tempfile.mkdtemp()
    app = Flask(__name__, instance_path=instance_path)
    FlaskCLI(app)
    InvenioAssets(app)
    os.chdir(instance_path)

    def teardown():
        shutil.rmtree(instance_path)
        os.chdir(initial_dir)

    request.addfinalizer(teardown)
    return ScriptInfo(create_app=lambda info: app)


@pytest.fixture()
def script_info_assets(request):
    """Get ScriptInfo object for testing CLI."""
    initial_dir = os.getcwd()
    instance_path = tempfile.mkdtemp()
    app = Flask(__name__, instance_path=instance_path)
    FlaskCLI(app)
    InvenioAssets(app)
    os.chdir(instance_path)

    class Ext(object):
        def __init__(self, app):
            assets = app.extensions['invenio-assets']
            assets.env.register('testbundle', NpmBundle(
                'test.css',
                output='testbundle.css'))
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    test_css = open(os.path.join(static_dir, 'test.css'), 'w+')
    test_css.write("Test")

    Ext(app)

    def teardown():
        shutil.rmtree(instance_path)
        os.chdir(initial_dir)

    request.addfinalizer(teardown)
    return ScriptInfo(create_app=lambda info: app)
