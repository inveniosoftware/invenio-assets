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

"""Test NpmBundle."""

from __future__ import absolute_import, print_function

import json
import os

from click.testing import CliRunner
from flask_assets import Bundle
from speaklater import make_lazy_string

from invenio_assets import LazyNpmBundle, NpmBundle
from invenio_assets.cli import npm
from invenio_assets.npm import extract_deps, make_semver


def test_init():
    """Test version import."""
    bundle = NpmBundle(
        'testfile.css',
        npm={
            'bootstrap': '3.0.0'
        }
    )
    assert bundle.npm == {'bootstrap': '3.0.0'}


def test_cli(script_info):
    """Test npm CLI."""

    deps = {'bootstrap': '3.0.0'}
    bundle = Bundle(
        NpmBundle(
            npm=deps
        )
    )

    runner = CliRunner()
    app = script_info.load_app()
    assets = app.extensions['invenio-assets']
    assets.env.register('test1', bundle)
    assert len(assets.env) == 1

    expected = {
        'name': app.name,
        'dependencies': {
            'bootstrap': '3.0.0',
        },
        'version': '',
    }

    # Test default output
    with runner.isolated_filesystem():
        result = runner.invoke(npm, obj=script_info)
        assert result.exit_code == 0

        filepath = os.path.join(app.static_folder, 'package.json')
        assert os.path.exists(filepath)

        with open(filepath) as f:
            package_json = json.loads(f.read())
        assert package_json == expected

    # Test writing package.json file.
    with runner.isolated_filesystem():
        result = runner.invoke(npm, ['-o', 'package.json'], obj=script_info)
        assert result.exit_code == 0

        filepath = os.path.join('package.json')
        assert os.path.exists(filepath)

        with open('package.json') as f:
            package_json = json.loads(f.read())
        assert package_json == expected

    # Test merging a base another file.
    newdep = {'font-awesome': '4.0'}
    expected['dependencies'].update(newdep)
    with runner.isolated_filesystem():
        with open('base.json', 'wt') as f:
            f.write(json.dumps({'dependencies': newdep}))

        result = runner.invoke(
            npm, ['-i', 'base.json', '-o', 'package.json'], obj=script_info)
        assert result.exit_code == 0

        filepath = os.path.join('package.json')
        assert os.path.exists(filepath)

        with open('package.json') as f:
            package_json = json.loads(f.read())
        assert package_json == expected
    del expected['dependencies']['font-awesome']

    # Test pinned file.
    pinned_deps = {'bootstrap': '2.9.9'}
    expected['dependencies'].update(pinned_deps)
    with runner.isolated_filesystem():
        with open('pinned.json', 'wt') as f:
            f.write(json.dumps({'dependencies': pinned_deps}))

        result = runner.invoke(
            npm, ['-p', 'pinned.json', '-o', 'package.json'], obj=script_info)
        assert result.exit_code == 0

        filepath = os.path.join('package.json')
        assert os.path.exists(filepath)

        with open('package.json') as f:
            package_json = json.loads(f.read())
        assert package_json == expected


def test_extract_deps():
    """Test bundles with conflicts."""
    bundle = Bundle(
        NpmBundle(npm={'jquery': '~2'}),
        NpmBundle(npm={'jquery': '~1.11'})
    )

    expected = {
        'jquery': '~2'
    }

    assert expected == extract_deps([bundle])


def test_lazy_bundle():
    """Test lazy bundle."""
    bundle = LazyNpmBundle(
        make_lazy_string(lambda: 'test{0}.js'.format(1)),
        'test2.js'
    )

    expected = ['test1.js', 'test2.js']
    assert expected == bundle.contents


def test_make_semver():
    """Test make semver."""
    tests = [
        ('1.0.dev456', '1.0.0-dev456'),
        ('1.0a1', '1.0.0-a1'),
        ('1.0a2.dev456', '1.0.0-a2.dev456'),
        ('1.0a12.dev456', '1.0.0-a12.dev456'),
        ('1.0a12', '1.0.0-a12'),
        ('1.0b1.dev456', '1.0.0-b1.dev456'),
        ('1.0b2', '1.0.0-b2'),
        ('1.0b2.post345.dev456', '1.0.0-b2.dev456'),
        ('1.0b2.post345', '1.0.0-b2'),
        ('1.0rc1.dev456', '1.0.0-rc1.dev456'),
        ('1.0rc1', '1.0.0-rc1'),
        ('1.0', '1.0.0'),
        ('1', '1.0.0'),
        ('1.0+abc.5', '1.0.0+abc.5'),
        ('1.0+abc.7', '1.0.0+abc.7'),
        ('1.0+5', '1.0.0+5'),
        ('1.0.post456.dev34', '1.0.0-dev34'),
        ('1.0.post456', '1.0.0'),
        ('1.1.dev1', '1.1.0-dev1'),
    ]
    for pyver, expected_semver in tests:
        assert make_semver(pyver) == expected_semver
