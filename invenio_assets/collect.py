# SPDX-FileCopyrightText: 2016-2020 CERN.
# SPDX-License-Identifier: MIT

"""Media asset management for Invenio."""


def collect_staticroot_removal(app, blueprints):
    """Remove collect's static root folder from list."""
    collect_root = app.extensions["collect"].static_root
    return [
        bp
        for bp in blueprints
        if (bp.has_static_folder and bp.static_folder != collect_root)
    ]
