# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Media asset management for Invenio."""


def collect_staticroot_removal(app, blueprints):
    """Remove collect's static root folder from list."""
    collect_root = app.extensions['collect'].static_root
    return [bp for bp in blueprints if (
        bp.has_static_folder and bp.static_folder != collect_root)]
