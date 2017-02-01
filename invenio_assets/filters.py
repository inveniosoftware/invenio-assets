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
import re
from subprocess import PIPE, Popen

from babel.messages.pofile import read_po
from flask import current_app
from webassets.filter import ExternalTool, Filter
from webassets.filter.requirejs import RequireJSFilter as RequireJSFilterBase

__all__ = ('AngularGettextFilter', 'RequireJSFilter', 'CleanCSSFilter',
           'CleanCSS3Filter', 'CleanCSS4Filter', )


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


class BaseCleanCSSFilter(ExternalTool):
    """Minify CSS using cleancss.

    Implements opener capable of rebasing relative CSS URLs against
    ``COLLECT_STATIC_ROOT``.

    If you want to use the version 4 of cleancss, please look at the class
    :class:`CleanCSS4Filter`.
    """

    name = None  #: Override in subclass
    rebase_opt = None  #: Override in subclass
    method = 'open'
    options = {
        'binary': 'CLEANCSS_BIN',
    }

    def setup(self):
        """Initialize filter just before it will be used."""
        super(BaseCleanCSSFilter, self).setup()
        self.root = current_app.config.get('COLLECT_STATIC_ROOT')

    def open(self, out, source_path, **kw):
        """Open source."""
        self.subprocess(
            [self.binary or 'cleancss', self.rebase_opt, self.root,
             source_path],
            out
        )

    def output(self, _in, out, **kw):
        """Output filtering."""
        self.subprocess([self.binary or 'cleancss'], out, _in)

    def input(self, _in, out, **kw):
        """Input filtering."""
        self.subprocess([self.binary or 'cleancss'], out, _in)


class CleanCSS3Filter(BaseCleanCSSFilter):
    """Minify CSS using cleancss version 3."""

    name = 'cleancss3url'
    rebase_opt = '--root'


class CleanCSS4Filter(BaseCleanCSSFilter):
    """Minify CSS using cleancss version 4."""

    name = 'cleancss4url'
    rebase_opt = '--rebaseTo'


class CleanCSSFilter(BaseCleanCSSFilter):
    """Minify CSS using cleancss (either version 3 or 4)."""

    name = 'cleancssurl'

    @property
    def rebase_opt(self):
        """Determine which option name to use."""
        # out = b"MAJOR.MINOR.REVISION" // b"3.4.19" or b"4.0.0"
        out, err = Popen(['cleancss', '--version'], stdout=PIPE).communicate()
        ver = int(out[:out.index(b'.')])
        return CleanCSS3Filter.rebase_opt if ver == 3 else \
            CleanCSS4Filter.rebase_opt


_re_language_code = re.compile(
    r'"Language: (?P<language_code>[A-Za-z_]{2,}(_[A-Za-z]{2,})?)\\n"'
)
"""Match language code group in PO file."""


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
        language_code = _re_language_code.search(_in.read()).group(
            'language_code'
        )
        _in.seek(0)  # move at the begining after matching the language
        catalog = read_po(_in)
        out.write('gettextCatalog.setStrings("{0}", '.format(language_code))
        out.write(json.dumps({
            key: value.string for key, value in catalog._messages.items()
            if key and value.string
        }))
        out.write(');')
