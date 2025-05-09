..
    This file is part of Invenio.
    Copyright (C) 2015-2024 CERN.
    Copyright (C) 2024 Graz University of Technology.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version v4.2.0 (released 2025-04-24)

- webpack: unminimized assets in development mode

Version 4.1.0 (released 2025-03-28)

* webpack: add `invenio_assets.webpack:rspack_project`
* build: remove duplicate dependencies from the base `package.json` files
* build: add `avif` & `webp` to the list of image types in the build configs

Version 4.0.0 (released 2024-12-02)

* setup: bump invenio dependencies

Version 3.1.0 (released 2024-11-28)

* setup: pin dependencies
* webpack: use CopyWebpackPlugin to copy assets defined in config.json
* fix: resolve dependency warning

Version 3.0.3 (released 2024-03-04)

* remove `node-semver`
* add `pywebpack` as a direct dependency, as the list of JS deps versions
  depends on the merging algorithm provided by pywebpack

Version 3.0.2 (released 2024-01-11)

* add tinymce to dependencies list

Version 3.0.1 (released 2023-12-12)

* replace ckeditor with tinymce due to license issue

Version 3.0.0 (released 2023-06-08)

* upgrade to webpack 5
* upgrade js dependencies
* upgrade webpack plugins

Version 2.0.0 (released 2022-10-24)

* upgrade dependencies to node 18 compliance

Version 1.3.1 (released 2022-09-01)

* Upgrade eslint dependencies
* Add eslint-config-invenio for global linting

Version 1.3.0 (released 2022-06-19)

* Replaces the deprecated NPM dependency `node-sass` with `dart-sass`.
* Upgrades `sass-loader` NPM dependency
* Depends on minor releases for NPM dependencies
* Migrates setup.py to setup.cfg
* Increases minimal python version to 3.7
* Introduces `black`` as code formatter

Version 1.2.7 (released 2021-10-18)

* Changed Flask-Collect (unmaintained since 2016) to Flask-Collect-Invenio and
  fixed Flask v2 support. You may need to uninstall Flask-Collect manually.

Version 1.2.6 (released 2021-05-18)

* Fixes missing "manifest.json". The issue was caused by the
  webpack-bundle-tracker changing behavior of where to output the manifest.json
  file between version v1.0.0-alpha1 and v1.0.0 (released 4 days ago).

Version 1.2.5 (released 2020-06-24)

* Updates ``package.json`` dev dependencies.

Version 1.2.4 (released 2020-06-24)

* Pins less-loader to version 6.1.0.
  See https://github.com/inveniosoftware/invenio-assets/issues/130.

Version 1.2.3 (released 2020-05-27)

* Fixes an alias issue with jQuery.

Version 1.2.2 (released 2020-05-26)

* Fixes an issue with attribute access and application context errors.

Version 1.2.1 (released 2020-05-25)

* Adds support for adding Webpack aliases to theme bundles.

Version 1.2.0 (released 2020-05-13)

* Uses ``webpack-bundle-tracker`` for the generating the Webpack manifest.
* Disables the vendor chunk grouping in Webpack config. Since now the manifest
  exposes entry chunk dependencies, the newly added
  ``UniqueJinjaManifestLoader`` renders (only once) each chunk.
* Adds a ``WebpackThemeBundle`` which uses the ``APP_THEME`` variable to
  determine which bundle will be used.
* Removes support for Flask-Assets and Webassets which was deprecated with
  the release of Invenio v3.0.

Version 1.1.5 (released 2020-04-28)

* Webpack now uses by default in debug/development mode folder-level symlinking
* Enabled source maps for Webpack development builds.
* Patched the ``watchpack`` library to support symlink watching via using
  ``patch-package``.

Version 1.1.4 (released 2019-02-20)

- Webpack Live-reload plugin.
- Webpack `@templates` alias.
- Webpack fix symlinks issue.

Version 1.1.3 (released 2019-07-29)

- Turn off webpack warnings

Version 1.1.2 (released 2019-02-15)

- Removes NPM warnings.

Version 1.1.1 (released 2018-12-14)

Version 1.1.0 (released 2018-11-06)

- Introduces webpack support.

Version 1.0.0 (released 2018-03-23)

- Initial public release.
