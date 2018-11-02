# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for assets and collect.

For detailed information about installed command you can execute:

.. code-block:: console

    $ flask --help
    ...
    Commands:
    assets   Web assets commands.
    collect  Collect static files.
    npm      Generate a package.json file.
    run      Runs a development server.
    shell    Runs a shell in the app context.
"""

from __future__ import absolute_import, print_function

import json
import os
import warnings
from functools import partial

import click
from flask import current_app
from flask.cli import with_appcontext
from flask_assets import assets
from pkg_resources import DistributionNotFound, get_distribution

from .npm import extract_deps, make_semver
from .proxies import current_assets

__all__ = ('collect', 'npm', )


def amd_build_deprecation_warning():
    """Add deprecation warning for AMD assets build system."""
    warnings.warn('The AMD build system is deprecated, please use Webpack '
                  'with the webpack command.', PendingDeprecationWarning)
    click.secho('The AMD build system is deprecated, please use Webpack '
                'with the webpack command.', fg='yellow')


for _, assets_cmd in assets.commands.items():
    original_callback = assets_cmd.callback

    def add_deprecation_warning(cmd_callback, *args, **kwargs):
        amd_build_deprecation_warning()
        cmd_callback(*args, **kwargs)

    assets_cmd.callback = partial(add_deprecation_warning, original_callback)


#
# Assets commands
#
@click.command()
@click.option('-i', '--package-json', help='base input file', default=None,
              type=click.File('r'))
@click.option('-o', '--output-file', help='write package.json to output file',
              metavar='FILENAME', type=click.File('w'))
@click.option('-p', '--pinned-file', help='pinned versions package file',
              default=None, type=click.File('r'))
@with_appcontext
def npm(package_json, output_file, pinned_file):
    """Generate a package.json file."""
    amd_build_deprecation_warning()
    try:
        version = get_distribution(current_app.name).version
    except DistributionNotFound:
        version = ''

    output = {
        'name': current_app.name,
        'version': make_semver(version) if version else version,
        'dependencies': {},
    }

    # Load base file
    if package_json:
        output = dict(output, **json.load(package_json))

    # Iterate over bundles
    deps = extract_deps(current_app.extensions['invenio-assets'].env,
                        click.echo)
    output['dependencies'].update(deps)

    # Load pinned dependencies
    if pinned_file:
        output['dependencies'].update(
            json.load(pinned_file).get('dependencies', {}))

    # Write to static folder if output file is not specified
    if output_file is None:
        if not os.path.exists(current_app.static_folder):
            os.makedirs(current_app.static_folder)
        output_file = open(
            os.path.join(current_app.static_folder, 'package.json'),
            'w')

    click.echo('Writing {0}'.format(output_file.name))
    json.dump(output, output_file, indent=4)
    output_file.close()


#
# Collect commands
#
@click.command()
@click.option('-v', '--verbose', default=False, is_flag=True)
@with_appcontext
def collect(verbose=False):
    """Collect static files."""
    current_assets.collect.collect(verbose=verbose)
