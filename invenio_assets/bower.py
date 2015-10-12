# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Bundle class with support for bower dependencies."""

from __future__ import absolute_import, print_function

from flask_assets import Bundle as BundleBase


class BowerBundle(BundleBase):
    """Bundle extension with a name and bower dependencies.

    The bower dependencies are used to generate a bower.json file.
    """

    def __init__(self, *contents, **options):
        """Initialize the named bundle.

        :param name: name of the bundle
        :type name: str
        :param bower: bower dependencies
        :type bower: dict
        """
        self.bower = options.pop("bower", {})
        super(BowerBundle, self).__init__(*contents, **options)
