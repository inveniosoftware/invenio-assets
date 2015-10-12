# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Filters for webassets."""

from __future__ import absolute_import, print_function

import os

from flask import current_app
from webassets.filter import ExternalTool
from webassets.filter.requirejs import RequireJSFilter as RequireJSFilterBase


class RequireJSFilter(RequireJSFilterBase):
    """Optimize AMD-style modularized JavaScript into a single asset.

    Adds support for exclusion of files already in defined in other bundles.
    """

    def __init__(self, *args, **kwargs):
        """Initialize filter."""
        self.excluded_bundles = kwargs.pop('exclude', [])
        super(RequireJSFilter, self).__init__(*args, **kwargs)

    def setup(self):
        """Setup filter (only called when filter is actually used)."""
        super(RequireJSFilter, self).setup()

        excluded_files = []
        for bundle in self.excluded_bundles:
            excluded_files.extend(
                map(lambda f: os.path.splitext(f)[0],
                    bundle.contents)
            )

        if excluded_files:
            self.argv.append(
                "exclude={0}".format(",".join(excluded_files))
            )


class CleanCSSFilter(ExternalTool):
    """Minify css using cleancss.

    Implements opener capable of rebasing relative CSS URLs against
    ``COLLECT_STATIC_ROOT``.
    """

    name = 'cleancssurl'
    method = 'open'
    options = {
        'binary': 'CLEANCSS_BIN',
    }

    def setup(self):
        """Initialize filter just before it will be used."""
        super(CleanCSSFilter, self).setup()
        self.root = current_app.config.get('COLLECT_STATIC_ROOT')

    def open(self, out, source_path, **kw):
        """Open source."""
        self.subprocess(
            [self.binary or 'cleancss', '--root', self.root, source_path],
            out
        )

    def output(self, _in, out, **kw):
        """Output filtering."""
        self.subprocess([self.binary or 'cleancss'], out, _in)

    def input(self, _in, out, **kw):
        """Input filtering."""
        self.subprocess([self.binary or 'cleancss'], out, _in)
