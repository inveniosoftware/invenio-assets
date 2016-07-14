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

"""Click command-line interface for assets and collect."""

from __future__ import absolute_import, print_function

import json
import logging
import os

import click
from flask import current_app
from flask.cli import with_appcontext
from pkg_resources import DistributionNotFound, get_distribution

from .npm import extract_deps, make_semver
from .proxy import current_assets


#
# Assets commands
#
def _webassets_cmd(cmd):
    """Helper to run a webassets command."""
    from webassets.script import CommandLineEnvironment
    logger = logging.getLogger('webassets')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    cmdenv = CommandLineEnvironment(current_app.jinja_env.assets_environment,
                                    logger)
    getattr(cmdenv, cmd)()


@click.command()
@click.option("-i", "--package-json", help="base input file", default=None,
              type=click.File('r'))
@click.option("-o", "--output-file", help="write package.json to output file",
              metavar="FILENAME", type=click.File('w'))
@with_appcontext
def npm(package_json, output_file):
    """Generate a package.json file."""
    try:
        version = get_distribution(current_app.name).version
    except DistributionNotFound:
        version = ""

    output = {
        "name": current_app.name,
        "version": make_semver(version) if version else version,
        "dependencies": {},
    }

    # Load base file
    if package_json:
        output = dict(output, **json.load(package_json))

    # Iterate over bundles
    deps = extract_deps(current_app.extensions['invenio-assets'].env,
                        click.echo)
    output['dependencies'].update(deps)

    # Write to static folder if output file is not specified
    if output_file is None:
        if not os.path.exists(current_app.static_folder):
            os.makedirs(current_app.static_folder)
        output_file = open(
            os.path.join(current_app.static_folder, "package.json"),
            "w")

    click.echo("Writing {0}".format(output_file.name))
    json.dump(output, output_file, indent=4)
    output_file.close()


@click.group()
def assets():
    """Web assets commands."""


@assets.command()
@with_appcontext
def build():
    """Build bundles."""
    _webassets_cmd('build')


@assets.command()
@with_appcontext
def clean():
    """Clean bundles."""
    _webassets_cmd('clean')


@assets.command()
@with_appcontext
def watch():
    """Watch bundles for file changes."""
    _webassets_cmd('watch')


#
# Collect commands
#
@click.command()
@click.option('-v', '--verbose', default=False, is_flag=True)
@with_appcontext
def collect(verbose=False):
    """Collect static files."""
    current_assets.collect.collect(verbose=verbose)
