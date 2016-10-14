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

from flask import Flask
from webassets.test import TempEnvironmentHelper

from invenio_assets import InvenioAssets
from invenio_assets.filters import AngularGettextFilter, CleanCSSFilter, \
    RequireJSFilter


class TestInvenioAssetsRequireJSFilter(TempEnvironmentHelper):
    """"Test class checking the behaviour of JSRequire filter."""
    default_files = {
        'foo.js': """
        more();
        """,
        'bar.js': """
        function foo(bar) {
            document.write ( bar );
        }
        """,
    }

    def test_require_js(self):
        """Test method of RequireJS filter."""
        bundle_0 = self.mkbundle('bar.js',
                                 filters=RequireJSFilter(),
                                 output='out_0.js')
        bundle_0.build()

        bundle_1 = self.mkbundle('foo.js', 'bar.js',
                                 filters=RequireJSFilter(exclude=[bundle_0]),
                                 output='out_1.js')
        bundle_1.build()

        assert self.get('out_1.js') == 'more(),define("foo",function(){});\n'


class TestInvenioAssetsCleanCSSFilter(TempEnvironmentHelper):
    """"Test class checking the behaviour of CSS filter """
    default_files = {
        'foo.css': """
        /* A comment */
            h1  {
                font-family: "Verdana"  ;
                 color: #FFFFFF;
            }
        """
    }

    def test_clean_CSS(self, static_dir):
        """Test method of Clean CSS filter."""
        app = Flask(__name__)
        InvenioAssets(app)
        with app.app_context():
            bundle = self.mkbundle('foo.css',
                                   filters=CleanCSSFilter(),
                                   output='out.css')
            bundle.build()
            assert self.get('out.css') == 'h1{font-family:Verdana;color:#FFF}'


class TestInvenioAssetsAngularGettextFilter(TempEnvironmentHelper):
    """"Test class checking the behaviour of CSS filter """
    default_files = {
        'messages-js.po': """
# French translations for invenio-search-ui.
# Copyright (C) 2016 CERN
# This file is distributed under the same license as the invenio-assets
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2016.
#
msgid ""
msgstr ""
"Project-Id-Version: invenio-assets 1.0.0.dev20161014\n"
"Report-Msgid-Bugs-To: info@inveniosoftware.org\n"
"POT-Creation-Date: 2016-10-14 15:18+0200\n"
"PO-Revision-Date: 2016-10-14 15:37+0200\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language: fr\n"
"Language-Team: fr <LL@li.org>\n"
"Plural-Forms: nplurals=2; plural=(n > 1)\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.3.4\n"

msgid "Error:"
msgstr "Erreur:"
        """
    }

    def test_angular_gettext(self, static_dir):
        """Test method of Clean CSS filter."""
        app = Flask(__name__)
        InvenioAssets(app)
        with app.app_context():
            bundle = self.mkbundle('messages-js.po',
                                   filters=AngularGettextFilter(
                                       catalog_name='testInvenioAssets'
                                   ),
                                   output='catalog.js')
            bundle.build()
            catalog = self.get('catalog.js')
            assert 'testInvenioAssets' in catalog
            assert 'Erreur' in catalog
