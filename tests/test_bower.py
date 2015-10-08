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

"""Test BowerBundle."""

from __future__ import absolute_import, print_function

import json
import os

from click.testing import CliRunner

from invenio_assets import BowerBundle
from invenio_assets.cli import bower


def test_init():
    """Test version import."""
    bundle = BowerBundle(
        'testfile.css',
        bower={
            "bootstrap": "3.0.0"
        }
    )
    assert bundle.bower == {"bootstrap": "3.0.0"}


def test_cli(script_info):
    """Test bower CLI."""
    deps = {"boostrap": "3.0.0"}

    runner = CliRunner()
    app = script_info.load_app()
    assets = app.extensions['invenio-assets']
    assets.env.register('test1', BowerBundle(bower=deps))
    assert len(assets.env) == 1

    expected = {
        "name": app.name,
        "dependencies": {
            "boostrap": "3.0.0",
        },
        "version": "",
    }

    # Test default output
    with runner.isolated_filesystem():
        result = runner.invoke(bower, obj=script_info)
        assert result.exit_code == 0

        filepath = os.path.join(app.instance_path, 'bower.json')
        assert os.path.exists(filepath)

        with open(filepath) as f:
            bower_json = json.loads(f.read())
        assert bower_json == expected

    # Test writing bower.json file.
    with runner.isolated_filesystem():
        result = runner.invoke(bower, ['-o', 'bower.json'], obj=script_info)
        assert result.exit_code == 0

        filepath = os.path.join('bower.json')
        assert os.path.exists(filepath)

        with open('bower.json') as f:
            bower_json = json.loads(f.read())
        assert bower_json == expected

    # Test merging a base another file.
    newdep = {'font-awesome': '4.0'}
    expected['dependencies'].update(newdep)
    with runner.isolated_filesystem():
        with open('base.json', 'wt') as f:
            f.write(json.dumps({'dependencies': newdep}))

        result = runner.invoke(
            bower, ['-i', 'base.json', '-o', 'bower.json'], obj=script_info)
        assert result.exit_code == 0

        filepath = os.path.join('bower.json')
        assert os.path.exists(filepath)

        with open('bower.json') as f:
            bower_json = json.loads(f.read())
        assert bower_json == expected
