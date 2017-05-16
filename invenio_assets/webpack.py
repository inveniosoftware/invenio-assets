# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default Webpack project for Invenio."""

from __future__ import absolute_import, print_function

from flask_webpackext import WebpackBundleProject
from pywebpack import bundles_from_entry_point

project = WebpackBundleProject(
    __name__,
    project_folder='assets',
    config_path='build/config.json',
    bundles=bundles_from_entry_point('invenio_assets.webpack'),
)
