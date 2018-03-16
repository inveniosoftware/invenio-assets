# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Bundle class with glob support."""

from __future__ import absolute_import

import glob

from flask_assets import Bundle


class GlobBundle(Bundle):
    """Magically expand globs as file names.

    Example usage:

    .. code-block:: python

        bundle = GlobBundle(
            'static/js/foo/*/*.js',
            output='bundle.js'
        )
    """

    def _get_contents(self):
        """Create strings from glob strings."""
        def files():
            for value in super(GlobBundle, self)._get_contents():
                for path in glob.glob(value):
                    yield path
        return list(files())

    contents = property(_get_contents, Bundle._set_contents)
