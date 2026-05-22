# SPDX-FileCopyrightText: 2015-2020 CERN.
# SPDX-License-Identifier: MIT

"""Proxy for Invenio-Assets."""

from flask import current_app
from werkzeug.local import LocalProxy

current_assets = LocalProxy(lambda: current_app.extensions["invenio-assets"])
"""Proxy to current InvenioAssets."""
