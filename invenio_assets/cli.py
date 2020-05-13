# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for assets and collect."""

import json
import os
import warnings
from functools import partial

import click
from flask import current_app
from flask.cli import with_appcontext

from .proxies import current_assets

__all__ = ('collect', )


@click.command()
@click.option('-v', '--verbose', default=False, is_flag=True)
@with_appcontext
def collect(verbose=False):
    """Collect static files."""
    current_assets.collect.collect(verbose=verbose)
