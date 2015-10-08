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


"""Test Invenio Assets module."""

from __future__ import absolute_import, print_function

from webassets import Bundle

from invenio_assets import InvenioAssets


def test_version():
    """Test version import."""
    from invenio_assets import __version__
    assert __version__


def test_init(app):
    """Test module initialization."""
    InvenioAssets(app)
    assets = app.extensions['invenio-assets']
    assert assets.env
    assert assets.collect
    assert app.config['REQUIREJS_BASEURL'] == app.static_folder
    assert app.config['REQUIREJS_CONFIG']
    assert app.config['COLLECT_STATIC_ROOT'] == app.static_folder


def test_init_post(app):
    """Test module initialization using init_app."""
    assets = InvenioAssets()
    assert assets.env
    assert assets.collect
    assert 'REQUIREJS_BASEURL' not in app.config
    assert 'COLLECT_STATIC_ROOT' not in app.config
    assets.init_app(app)
    assert 'REQUIREJS_BASEURL' in app.config
    assert 'COLLECT_STATIC_ROOT' in app.config


def test_init_cli(app):
    """Test cli registration."""
    assets = InvenioAssets(app)
    assert len(app.cli.commands) == 0
    assets.init_cli(app.cli)
    assert len(app.cli.commands) == 3


def test_assets_usage(app):
    """Test assets usage."""
    class Ext(object):
        def __init__(self, app):
            assets = app.extensions['invenio-assets']
            assets.env.register('testbundle', Bundle())

    assets = InvenioAssets(app)
    Ext(app)
    assert len(assets.env) == 1
