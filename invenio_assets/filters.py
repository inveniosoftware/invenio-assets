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

"""Filters for webassets."""

from __future__ import absolute_import, print_function

import json
import os

from babel.messages.pofile import read_po
from flask import current_app
from webassets.filter import ExternalTool, Filter
from webassets.filter.requirejs import RequireJSFilter as RequireJSFilterBase

__all__ = ('AngularGettextFilter', 'RequireJSFilter', 'CleanCSSFilter', )


class RequireJSFilter(RequireJSFilterBase):
    """Optimize AMD-style modularized JavaScript into a single asset.

    Adds support for exclusion of files already in defined in other bundles.
    """

    def __init__(self, *args, **kwargs):
        r"""Initialize filter.

        :param \*args: Arguments are forwarded to parent class.
        :param \**kwargs: Keyword arguments are forwarded to parent class
            except the *exclude* keyword.
        """
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
                'exclude={0}'.format(','.join(excluded_files))
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


class AngularGettextFilter(Filter):
    """Compile GNU gettext messages to angular-gettext module."""

    name = 'angular-gettext'

    options = {
        'catalog_name': None,
    }

    def output(self, _in, out, **kwargs):
        """Wrap translation in Angular module."""
        out.write(
            'angular.module("{0}", ["gettext"]).run('
            '["gettextCatalog", function (gettextCatalog) {{'.format(
                self.catalog_name
            )
        )
        out.write(_in.read())
        out.write('}]);')

    def input(self, _in, out, **kwargs):
        """Process individual translation file."""
        catalog = read_po(_in)
        out.write('gettextCatalog.setStrings("{0}", '.format(
            catalog.language_team.split(' ')[0]
        ))
        out.write(json.dumps({
            key: value.string for key, value in catalog._messages.items()
            if key
        }))
        out.write(');')
