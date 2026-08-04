# SPDX-FileCopyrightText: 2015-2026 CERN.
# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Test version consistency across all version files."""

import json
import re
from pathlib import Path


def test_version_consistency():
    """Test that all version files have the same version number."""
    # Paths to version files
    init_file = Path("invenio_assets/__init__.py")
    package_json = Path("invenio_assets/assets/package.json")
    rspack_json = Path("invenio_assets/assets/rspack-package.json")

    # Extract version from __init__.py
    init_content = init_file.read_text()
    py_match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', init_content, re.M)
    assert py_match, "Could not find __version__ in __init__.py"
    py_version = py_match.group(1)

    # Extract version from package.json
    pkg_content = json.loads(package_json.read_text())
    pkg_version = pkg_content["version"]

    # Extract version from rspack-package.json
    rspack_content = json.loads(rspack_json.read_text())
    rspack_version = rspack_content["version"]

    # All versions must match
    assert py_version == pkg_version == rspack_version, (
        f"Version mismatch: "
        f"__init__.py={py_version}, "
        f"package.json={pkg_version}, "
        f"rspack-package.json={rspack_version}"
    )
