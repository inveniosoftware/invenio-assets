# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test GlobBundle."""

from __future__ import absolute_import, print_function

import os

from invenio_assets import GlobBundle


def test_init(testcss):
    """Test glob search."""
    bundle = GlobBundle(
        os.path.join(os.path.dirname(testcss), '*.css')
    )
    assert bundle.contents == [testcss]
