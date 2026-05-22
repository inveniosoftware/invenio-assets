# SPDX-FileCopyrightText: 2015-2020 CERN.
# SPDX-License-Identifier: MIT

"""Click command-line interface for assets and collect."""

import click
from flask.cli import with_appcontext

from .proxies import current_assets

__all__ = ("collect",)


@click.command()
@click.option("-v", "--verbose", default=False, is_flag=True)
@with_appcontext
def collect(verbose=False):
    """Collect static files."""
    current_assets.collect.collect(verbose=verbose)
