# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxy for Invenio-Assets."""

from flask import current_app
from werkzeug.local import LocalProxy

current_assets = LocalProxy(lambda: current_app.extensions['invenio-assets'])
"""Proxy to current InvenioAssets."""
