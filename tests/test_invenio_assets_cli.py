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


"""Test Invenio Assets module."""

from __future__ import absolute_import, print_function

import os

from click.testing import CliRunner
from flask_assets import assets

from invenio_assets.cli import collect


def test_invenio_assets_assets(script_info_assets):
    """Test assets command in assets CLI."""
    runner = CliRunner()
    result = runner.invoke(assets, ['build'], obj=script_info_assets)
    assert result.exit_code == 0

    result = runner.invoke(collect, [], obj=script_info_assets)

    path = os.path.join(
        os.path.join(os.path.dirname(__file__), 'static'), 'testbundle.css')
    assert result.exit_code == 0
    assert os.path.isfile(path)

    result = runner.invoke(assets, ['clean'], obj=script_info_assets)
    result.exit_code == 0
